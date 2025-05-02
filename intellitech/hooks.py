app_name = "intellitech"
app_title = "Intellitech"
app_publisher = "Fariz Khanzada"
app_description = "Smart Attendance Machine Integration with ERP"
app_email = "khanzadafariz@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "intellitech",
# 		"logo": "/assets/intellitech/logo.png",
# 		"title": "Intellitech",
# 		"route": "/intellitech",
# 		"has_permission": "intellitech.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/intellitech/css/intellitech.css"
# app_include_js = "/assets/intellitech/js/intellitech.js"

# include js, css files in header of web template
# web_include_css = "/assets/intellitech/css/intellitech.css"
# web_include_js = "/assets/intellitech/js/intellitech.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "intellitech/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "intellitech/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "intellitech.utils.jinja_methods",
# 	"filters": "intellitech.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "intellitech.install.before_install"
# after_install = "intellitech.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "intellitech.uninstall.before_uninstall"
# after_uninstall = "intellitech.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "intellitech.utils.before_app_install"
# after_app_install = "intellitech.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "intellitech.utils.before_app_uninstall"
# after_app_uninstall = "intellitech.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "intellitech.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }


# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"intellitech.tasks.all"
	# ],
	# "daily": [
	# 	"intellitech.tasks.daily"
	# ],
	"hourly": [
		  "intellitech.intellitech.api.checksync1.process_checkins"
	],
	# "weekly": [
	# 	"intellitech.tasks.weekly"
	# ],
	# "monthly": [
	# 	"intellitech.tasks.monthly"
	# ],
}


# scheduler_events = {
#     "cron": {
#         "*/10 * * * *": [  # Runs every 10 minutes
#             "intellitech.intellitech.api.checksync.process_checkins"
#         ]
#     }
# }




# Testing
# -------

# before_tests = "intellitech.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "intellitech.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "intellitech.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["intellitech.utils.before_request"]
# after_request = ["intellitech.utils.after_request"]

# Job Events
# ----------
# before_job = ["intellitech.utils.before_job"]
# after_job = ["intellitech.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"intellitech.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
