import json,requests
import frappe

authorization = frappe.db.get_single_value("Biometric Settings", "key")
url = frappe.db.get_single_value("Biometric Settings", "url")
headers = {
   	"Content-Type": "application/json",
   	"Authorization": authorization
}


def execute():
	response = requests.request('GET',url,headers=headers)
	data = response.json()
	checkinout = data['data']
	log_type = ""
	for c in range(len(checkinout)):
		if checkinout[c]['punch_state_display'] == "Check In":
			log_type = 'IN'
		if checkinout[c]['punch_state_display'] == "Check Out":
			log_type = 'OUT'
		employee = frappe.db.get_value("Employee",{"code":checkinout[c]["emp_code"]},"name")
		if not frappe.db.exists("Employee",{"code":checkinout[c]["emp_code"]}):
			log = frappe.new_doc("Bio logs")
			log.log = "code {} is not attached to any employee".format(checkinout[c]["emp_code"])
			log.save()
			frappe.db.commit()
		else:
			time = checkinout[c]['punch_time']
			location = checkinout[c]['area_alias']
			create_checkin(employee,time,location,log_type)






def create_checkin(employee,time,location,log_type):
	echeck = frappe.new_doc("Employee Checkin")
	if not frappe.db.exists("Employee Checkin",{"time":time,"log_type":log_type,"employee":employee}):
		echeck.employee = employee
		echeck.time = time
		echeck.log_type = log_type
		echeck.device_id = location
		echeck.save()
		frappe.db.commit()