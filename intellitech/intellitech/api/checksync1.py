
import frappe
import requests
import json
from frappe.utils import get_datetime, now

def fetch_dynamic_api_details():
    all_settings = frappe.get_all("Intellitech Setting")
    api_details_list = []

    for setting in all_settings:
        settings_doc = frappe.get_doc("Intellitech Setting", setting.name)
        api_url = settings_doc.api
        host_ip = settings_doc.host_ip
        from_date = settings_doc.start_date

        if not api_url or not host_ip or not from_date:
            print(f"Skipping {setting.name}: Missing required fields.")
            continue

        formatted_from_date = get_datetime(from_date).strftime("%Y/%m/%d")
        end_date = get_datetime(now()).strftime("%Y/%m/%d")
        full_api_url = f"http://{host_ip}{api_url}"

        api_details_list.append({
            "url": full_api_url,
            "from_date": formatted_from_date,
            "end_date": end_date,
            "doc": settings_doc
        })

    return api_details_list

def fetch_checkins():
    all_checkin_data = []

    api_configs = fetch_dynamic_api_details()

    for config in api_configs:
        api_url = config["url"]
        from_date = config["from_date"]
        end_date = config["end_date"]
        settings_doc = config["doc"]

        print(f"Fetching from {api_url} | From: {from_date} To: {end_date}")

        headers = {"Content-Type": "application/json"}
        payload = {
            "Dates": from_date,
            "DatesTo": end_date
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            data = response.json()

            checkins = data["data"] if isinstance(data.get("data"), list) else []
            if not isinstance(data.get("data"), list):
                frappe.log_error(f"Unexpected response from {api_url}", json.dumps(data, indent=2))

            all_checkin_data.append({
                "checkins": checkins,
                "end_date": end_date,
                "settings_doc": settings_doc
            })

        except requests.exceptions.Timeout:
            frappe.log_error(f"Timeout from {api_url}", "Try increasing the timeout or check API server.")
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"Request failed for {api_url}", str(e))
        except json.JSONDecodeError:
            frappe.log_error(f"Invalid JSON from {api_url}", "Check the API response format.")

    return all_checkin_data

@frappe.whitelist()
def process_checkins(doc=None, method=None):
    all_checkin_sets = fetch_checkins()

    if not all_checkin_sets:
        frappe.throw("No check-in records found from any API.")

    shift_types_with_checkins = set()
    has_checkins_for_setting = False
    for checkin_set in all_checkin_sets:
        checkins = checkin_set["checkins"]
        end_date = checkin_set["end_date"]
        settings_doc = checkin_set["settings_doc"]

        for checkin in checkins:
            try:
                enroll_id = checkin.get("enrollid")
                log_time = checkin.get("arrive_time")
                latitude = checkin.get("latitude") or 0.0
                longitude = checkin.get("longitude") or 0.0  

                if not enroll_id or not log_time:
                    print(f"Skipping invalid check-in record: {checkin}")
                    continue

                event_datetime = get_datetime(log_time).replace(tzinfo=None)

                emp_list = frappe.get_list("Employee", 
                    filters={"attendance_device_id": enroll_id, "company": settings_doc.company},
                    fields=["name", "default_shift"]
                )
                
                if not emp_list:
                    print(f"Skipping unknown Employee ID: {enroll_id}")
                    continue

                emp_doc = frappe.get_doc("Employee", emp_list[0].name)
                existing_checkin = frappe.db.exists(
                    "Employee Checkin",
                    {"employee": emp_doc.name, "time": event_datetime}
                )

                if not existing_checkin:
                    checkin_doc = frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": emp_doc.name,
                        "time": event_datetime,
                        "latitude": latitude,
                        "longitude": longitude
                    })
                    checkin_doc.insert()
                    frappe.db.commit()
                    
                    print(f"Inserted check-in for {emp_doc.name} at {event_datetime} with Lat: {latitude}, Long: {longitude}")
                    has_checkins_for_setting = True
                    if emp_list[0].default_shift:
                        shift_types_with_checkins.add(emp_list[0].default_shift)

            except Exception as e:
                print(f"Error processing check-in: {str(e)}")
        latest_checkin_time = frappe.db.sql("""
            SELECT MAX(ec.time)
            FROM `tabEmployee Checkin` ec
            JOIN `tabEmployee` e ON ec.employee = e.name
            WHERE e.company = %s
        """, settings_doc.company)[0][0]

        if latest_checkin_time:
            settings_doc.last_sync_of_employee_check_in = latest_checkin_time
            print(f"Set last_sync_of_employee_check_in to: {latest_checkin_time}")
        settings_doc.start_date = end_date
        settings_doc.last_sync = now()
        settings_doc.save()
        print(f"Updated Intellitech start_date for {settings_doc.name} to: {end_date}")

    all_shifts = frappe.get_all("Shift Type", pluck="name")

    for shift_name in all_shifts:
        try:
            shift_doc = frappe.get_doc("Shift Type", shift_name)
            shift_doc.last_sync_of_checkin = now()
            shift_doc.save()
            print(f"Updated last_sync_of_checkin for Shift Type: {shift_name}")
        except Exception as e:
            print(f"Error updating Shift Type {shift_name}: {str(e)}")

    print("Check-in processing complete.")


