
import frappe
import requests
import json
from frappe.utils import get_datetime, now

def fetch_dynamic_api_details():

    settings_doc = frappe.get_doc("Intellitech Device Settings")
    if not settings_doc:
        frappe.throw("No Intellitech Device Setting found. Please configure API details.")

    api_url = settings_doc.api
    host_ip = settings_doc.host_ip
    from_date = settings_doc.start_date

    if not api_url or not host_ip:
        frappe.throw("Missing API URL or Host IP in Intellitech Device Setting.")

    if not from_date:
        frappe.throw("From Date (start_date) is missing in Intellitech Device Setting.")

    formatted_from_date = get_datetime(from_date).strftime("%Y/%m/%d")
    end_date = get_datetime(now()).strftime("%Y/%m/%d")
    full_api_url = f"http://{host_ip}{api_url}"

    return full_api_url, formatted_from_date, end_date, settings_doc









def fetch_checkins():

    api_url, from_date, end_date, settings_doc = fetch_dynamic_api_details()
    print(str(from_date) + "  " + str(end_date))
    headers = {"Content-Type": "application/json"}
    payload = {
        "Dates": from_date,
        "DatesTo": end_date
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        data = response.json()

        if "data" in data and isinstance(data["data"], list):
            return data["data"], end_date,settings_doc
        else:
            frappe.throw(f"Unexpected API response format: {json.dumps(data, indent=2)}")

    except requests.exceptions.Timeout:
        frappe.throw("API request timed out. Try increasing the timeout or check API server.")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Failed to fetch data: {str(e)}")
    except json.JSONDecodeError:
        frappe.throw("Failed to decode API response. Check if the API is returning valid JSON.")

    return None, None  







@frappe.whitelist()
def process_checkins():

    checkins, end_date,settings_doc = fetch_checkins()

    if not checkins:
        frappe.throw("No check-in records found from API.")

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
            emp_list = frappe.get_list("Employee", filters={"attendance_device_id": enroll_id})
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

        except Exception as e:
            print(f"Error processing check-in: {str(e)}")

    for shift_type in frappe.get_list("Shift Type"):
        shift_doc = frappe.get_doc("Shift Type", shift_type.name)
        shift_doc.last_sync_of_checkin = now()
        shift_doc.save()

    if settings_doc:
        settings_doc.start_date = end_date
        settings_doc.last_sync = now()
        settings_doc.save()
        print(f"Updated Intellitech start_date to: {end_date}")

    print("Check-in processing complete.")


















































# import frappe
# import requests
# import json
# from frappe.utils import get_datetime, add_to_date, now, formatdate

# def fetch_dynamic_api_details():
#     """Fetch API URL and start date from Intellitech Device Setting doctype."""
#     settings_doc = frappe.get_doc("Intellitech Device Setting")  # Get full document

#     if not settings_doc:
#         frappe.throw("No Intellitech Device Setting found. Please configure API details.")


#     api_url = settings_doc.api
#     host_ip = settings_doc.host_ip
#     start_date = settings_doc.start_date
    

#     if not api_url or not host_ip:
#         frappe.throw("Missing API URL or Host IP in Intellitech Device Setting.")

#     # ✅ Ensure correct date format (YYYY/MM/DD)
#     if start_date:
#         start_date_dt = get_datetime(start_date)  # Convert string to datetime
#         formatted_start_date = start_date_dt.strftime("%Y/%m/%d")  # Convert to required format
#     else:
#         frappe.throw("Start Date is missing in Intellitech Device Setting.")

#     full_api_url = f"http://{host_ip}{api_url}"

#     return full_api_url, formatted_start_date


# def fetch_checkins():
#     """Fetch check-in data from the API using a POST request and return as a list."""
#     api_url, start_date = fetch_dynamic_api_details()

#     end_date = start_date  # Assuming the same start and end date
#     print(start_date , "     " , end_date)
#     print(api_url)
#     payload = {
#         "Dates": start_date,
#         "DatesTo": end_date
#     }

#     headers = {
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(api_url, json=payload, headers=headers, timeout=300)  
#         response.raise_for_status()  

#         data = response.json()

#         if "data" in data and isinstance(data["data"], list):
#             return data["data"]
#         else:
#             frappe.throw(f"Unexpected API response format: {json.dumps(data, indent=2)}")
    
#     except requests.exceptions.Timeout:
#         frappe.throw("API request timed out. Try increasing the timeout or check API server.")
#     except requests.exceptions.RequestException as e:
#         frappe.throw(f"Failed to fetch data: {str(e)}")
#     except json.JSONDecodeError:
#         frappe.throw("Failed to decode API response. Check if the API is returning valid JSON.")

#     return None  







# @frappe.whitelist()
# def process_checkins():
#     """Process fetched check-in data and insert into ERPNext with latitude & longitude handling."""
#     checkins = fetch_checkins()

#     if not checkins:
#         frappe.throw("No check-in records found from API.")

#     latest_log_time = None  # Track the latest check-in timestamp

#     for checkin in checkins:
#         try:
#             enroll_id = checkin.get("enrollid")
#             log_time = checkin.get("arrive_time")

#             # ✅ Handle missing latitude & longitude
#             latitude = checkin.get("latitude") or 0.0
#             longitude = checkin.get("longitude") or 0.0  

#             if not enroll_id or not log_time:
#                 print(f"Skipping invalid check-in record: {checkin}")
#                 continue

#             event_datetime = get_datetime(log_time)
#             event_datetime_naive = event_datetime.replace(tzinfo=None)
#             event_datetime_naive = add_to_date(event_datetime_naive, hours=0)

#             # ✅ Update latest log time
#             if not latest_log_time or event_datetime_naive > latest_log_time:
#                 latest_log_time = event_datetime_naive

#             # Find employee by attendance_device_id
#             emp_list = frappe.get_list("Employee", filters={"attendance_device_id": enroll_id})
#             if not emp_list:
#                 print(f"Skipping unknown Employee ID: {enroll_id}")
#                 continue

#             emp_doc = frappe.get_doc("Employee", emp_list[0].name)

#             # Check if check-in already exists
#             existing_checkin = frappe.db.exists(
#                 "Employee Checkin",
#                 {"employee": emp_doc.name, "time": event_datetime_naive}
#             )

#             if not existing_checkin:
#                 # Insert check-in record
#                 checkin_doc = frappe.get_doc({
#                     "doctype": "Employee Checkin",
#                     "employee": emp_doc.name,
#                     "time": event_datetime_naive,
#                     "latitude": latitude,
#                     "longitude": longitude
#                 })
#                 checkin_doc.insert()
#                 frappe.db.commit()
#                 print(f"Inserted check-in for {emp_doc.name} at {event_datetime_naive} with Lat: {latitude}, Long: {longitude}")

#         except Exception as e:
#             print(f"Error processing check-in: {str(e)}")  

#     # ✅ Update last sync time in Shift Type
#     for shift_type in frappe.get_list("Shift Type"):
#         shift_doc = frappe.get_doc("Shift Type", shift_type.name)
#         shift_doc.last_sync_of_checkin = now()
#         shift_doc.save()

#     # ✅ Update `start_date` in "Intellitech Device Setting"
#     if latest_log_time:
#         formatted_latest_log_time = latest_log_time.strftime("%Y/%m/%d")  # Convert to YYYY/MM/DD format
#         settings_list = frappe.get_list("Intellitech Device Setting", pluck="name", limit_page_length=1)

#         if settings_list:
#             settings_doc = frappe.get_doc("Intellitech Device Setting", settings_list[0])
#             settings_doc.start_date = formatted_latest_log_time
#             settings_doc.save()
#             print(f"Updated Intellitech start_date to: {formatted_latest_log_time}")

#     print("Check-in processing complete.")












# # @frappe.whitelist()
# # def process_checkins():
# #     """Process fetched check-in data and insert into ERPNext with latitude & longitude handling."""
# #     checkins = fetch_checkins()

# #     if not checkins:
# #         frappe.throw("No check-in records found from API.")

# #     for checkin in checkins:
# #         try:
# #             enroll_id = checkin.get("enrollid")
# #             log_time = checkin.get("arrive_time")

# #             # Handle missing latitude & longitude
# #             latitude = checkin.get("latitude") or 0.0
# #             longitude = checkin.get("longitude") or 0.0  

# #             if not enroll_id or not log_time:
# #                 print(f"Skipping invalid check-in record: {checkin}")
# #                 continue

# #             event_datetime = get_datetime(log_time)
# #             event_datetime_naive = event_datetime.replace(tzinfo=None)
# #             event_datetime_naive = add_to_date(event_datetime_naive, hours=0)

# #             # Find employee by attendance_device_id
# #             emp_list = frappe.get_list("Employee", filters={"attendance_device_id": enroll_id})
# #             if not emp_list:
# #                 print(f"Skipping unknown Employee ID: {enroll_id}")
# #                 continue

# #             emp_doc = frappe.get_doc("Employee", emp_list[0].name)

# #             # Check if check-in already exists
# #             existing_checkin = frappe.db.exists(
# #                 "Employee Checkin",
# #                 {"employee": emp_doc.name, "time": event_datetime_naive}
# #             )

# #             if not existing_checkin:
# #                 # Insert check-in record
# #                 checkin_doc = frappe.get_doc({
# #                     "doctype": "Employee Checkin",
# #                     "employee": emp_doc.name,
# #                     "time": event_datetime_naive,
# #                     "latitude": latitude,
# #                     "longitude": longitude
# #                 })
# #                 checkin_doc.insert()
# #                 frappe.db.commit()
# #                 print(f"Inserted check-in for {emp_doc.name} at {event_datetime_naive} with Lat: {latitude}, Long: {longitude}")

# #         except Exception as e:
# #             print(f"Error processing check-in: {str(e)}")  

# #     # ✅ Update last sync time
# #     for shift_type in frappe.get_list("Shift Type"):
# #         shift_doc = frappe.get_doc("Shift Type", shift_type.name)
# #         shift_doc.last_sync_of_checkin = now()
# #         shift_doc.save()

# #     print("Check-in processing complete.")
