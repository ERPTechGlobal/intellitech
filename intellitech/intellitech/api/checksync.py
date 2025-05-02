
# import frappe
# import requests
# import json
# from frappe.utils import get_datetime, now

# def fetch_dynamic_api_details():

#     settings_doc = frappe.get_doc("Intellitech Device Settings")
#     if not settings_doc:
#         frappe.throw("No Intellitech Device Setting found. Please configure API details.")

#     api_url = settings_doc.api
#     host_ip = settings_doc.host_ip
#     from_date = settings_doc.start_date

#     if not api_url or not host_ip:
#         frappe.throw("Missing API URL or Host IP in Intellitech Device Setting.")

#     if not from_date:
#         frappe.throw("From Date (start_date) is missing in Intellitech Device Setting.")

#     formatted_from_date = get_datetime(from_date).strftime("%Y/%m/%d")
#     end_date = get_datetime(now()).strftime("%Y/%m/%d")
#     full_api_url = f"http://{host_ip}{api_url}"

#     return full_api_url, formatted_from_date, end_date, settings_doc









# def fetch_checkins():

#     api_url, from_date, end_date, settings_doc = fetch_dynamic_api_details()
#     print(str(from_date) + "  " + str(end_date))
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "Dates": from_date,
#         "DatesTo": end_date
#     }

#     try:
#         response = requests.post(api_url, json=payload, headers=headers, timeout=300)
#         response.raise_for_status()
#         data = response.json()

#         if "data" in data and isinstance(data["data"], list):
#             return data["data"], end_date,settings_doc
#         else:
#             frappe.throw(f"Unexpected API response format: {json.dumps(data, indent=2)}")

#     except requests.exceptions.Timeout:
#         frappe.throw("API request timed out. Try increasing the timeout or check API server.")
#     except requests.exceptions.RequestException as e:
#         frappe.throw(f"Failed to fetch data: {str(e)}")
#     except json.JSONDecodeError:
#         frappe.throw("Failed to decode API response. Check if the API is returning valid JSON.")

#     return None, None  







# @frappe.whitelist()
# def process_checkins():

#     checkins, end_date,settings_doc = fetch_checkins()

#     if not checkins:
#         frappe.throw("No check-in records found from API.")

#     for checkin in checkins:
#         try:
#             enroll_id = checkin.get("enrollid")
#             log_time = checkin.get("arrive_time")

#             latitude = checkin.get("latitude") or 0.0
#             longitude = checkin.get("longitude") or 0.0  

#             if not enroll_id or not log_time:
#                 print(f"Skipping invalid check-in record: {checkin}")
#                 continue

#             event_datetime = get_datetime(log_time).replace(tzinfo=None)
#             emp_list = frappe.get_list("Employee", filters={"attendance_device_id": enroll_id})
#             if not emp_list:
#                 print(f"Skipping unknown Employee ID: {enroll_id}")
#                 continue

#             emp_doc = frappe.get_doc("Employee", emp_list[0].name)
#             existing_checkin = frappe.db.exists(
#                 "Employee Checkin",
#                 {"employee": emp_doc.name, "time": event_datetime}
#             )

#             if not existing_checkin:
#                 checkin_doc = frappe.get_doc({
#                     "doctype": "Employee Checkin",
#                     "employee": emp_doc.name,
#                     "time": event_datetime,
#                     "latitude": latitude,
#                     "longitude": longitude
#                 })
#                 checkin_doc.insert()
#                 frappe.db.commit()
#                 print(f"Inserted check-in for {emp_doc.name} at {event_datetime} with Lat: {latitude}, Long: {longitude}")

#         except Exception as e:
#             print(f"Error processing check-in: {str(e)}")

#     for shift_type in frappe.get_list("Shift Type"):
#         shift_doc = frappe.get_doc("Shift Type", shift_type.name)
#         shift_doc.last_sync_of_checkin = now()
#         shift_doc.save()

#     if settings_doc:
#         settings_doc.start_date = end_date
#         settings_doc.last_sync = now()
#         settings_doc.save()
#         print(f"Updated Intellitech start_date to: {end_date}")

#     print("Check-in processing complete.")
