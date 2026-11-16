# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "msme"
app_title = "Erpnext Msme Section43B Compliance Tracker"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Msme Section43B Compliance Tracker for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/msme/css/msme.bundle.css"
app_include_js = "/assets/msme/js/msme.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "msme.engine.on_document_submit",
        "on_cancel": "msme.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "msme.engine.daily_scheduled_sync"
    ]
}
