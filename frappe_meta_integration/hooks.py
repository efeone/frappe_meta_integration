from . import __version__ as app_version

app_name = "frappe_meta_integration"
app_title = "Frappe Meta Integration"
app_publisher = "efeone Pvt. Ltd."
app_description = "Meta Cloud API Integration for frappe framework"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@efeone.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_meta_integration/css/frappe_meta_integration.css"
app_include_js = "/assets/frappe_meta_integration/js/toolbar.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_meta_integration/css/frappe_meta_integration.css"
# web_include_js = "/assets/frappe_meta_integration/js/frappe_meta_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_meta_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Notification" : "whatsapp/public/js/notification.js",
	"User" : "whatsapp/public/js/user.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "frappe_meta_integration.install.before_install"
# after_install = "frappe_meta_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_meta_integration.uninstall.before_uninstall"
# after_uninstall = "frappe_meta_integration.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_meta_integration.notifications.get_notification_config"

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

override_doctype_class = {
	"Notification": "frappe_meta_integration.whatsapp.overrides.notification.SendNotification"
}

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
	"Contact": {
		"validate": "frappe_meta_integration.whatsapp.docevents.contact_validate",
	},
	"User": {
		"after_insert" : "frappe_meta_integration.whatsapp.docevents.user_after_insert"
	}
}


fixtures = ["Property Setter"]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_meta_integration.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_meta_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_meta_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_meta_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"frappe_meta_integration.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "frappe_meta_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_meta_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_meta_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_meta_integration.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
