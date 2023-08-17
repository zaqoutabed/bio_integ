import json,requests
import frappe
from datetime import datetime
from frappe.utils import date_diff
from bio_integ.token import get_token
from frappe.utils import now_datetime




settings = frappe.get_doc("Biometric Settings")
headers = {
   	"Content-Type": "application/json",
   	"Authorization": settings.key,
}

payload = {
	"page_size": settings.size
}

param = "?start_time={}".format(settings.start_time)

@frappe.whitelist()
def execute():
	response = requests.get(settings.url+param,headers=headers,
									params=payload,
									timeout=settings.timeout)
	data = response.json()
	checkinout = data['data']
	log_type = ""
	for c in range(len(checkinout)):
		if checkinout[c]['punch_state_display'] == "Check In":
			log_type = 'IN'
		elif checkinout[c]['punch_state_display'] == "Check Out":
			log_type = 'OUT'
		employee = frappe.db.get_value("Employee",{"attendance_device_id":checkinout[c]["emp_code"]},"name")
		if not frappe.db.exists("Employee",{"attendance_device_id":checkinout[c]["emp_code"]}):
			if not frappe.db.exists("Bio logs",{"code":checkinout[c]["emp_code"]}):
				log = frappe.new_doc("Bio logs")
				log.code = checkinout[c]["emp_code"]
				log.log = "code {} is not attached to any employee".format(checkinout[c]["emp_code"])
				log.save()
		else:
			time = checkinout[c]['punch_time']
			location = checkinout[c]['terminal_alias']
			create_checkin(employee,time,location,log_type)
			shift_list = frappe.get_all('Shift Type', 'name', {'enable_auto_attendance':'1'}, as_list=True)
		    for row in shift_list:
		        frappe.set_value('Shift Type', row[0], 'last_sync_of_checkin', now_datetime())
		        frappe.db.commit()
	return data


def create_checkin(employee,time,location,log_type):
	echeck = frappe.new_doc("Employee Checkin")
	if frappe.db.exists("Employee Checkin",{"time":time,"employee":employee}):
		pass
	else:
		echeck.employee = employee
		echeck.time = time
		echeck.log_type = log_type
		echeck.device_id = location
		echeck.save()
		frappe.db.commit()


def update_start_time():
	start = datetime.strptime(settings.start_time, "%Y-%m-%d %H:%M:%S")
	if date_diff(datetime.today(),start) ==32:
		settings.start_time = frappe.utils.add_months(start, 1)
		settings.save()

@frappe.whitelist()
def update_key():
	settings.key = get_token()
	settings.save()
	return get_token()
		

