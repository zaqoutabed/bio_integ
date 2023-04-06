import json
import requests



def get_token():
	headers = {
		"Content-Type": "application/json",
	}

	data = {
		"username":"admin",
		"password":"Admin123"
	}
	response = requests.post("http://deco.dyndns.biz:8400/jwt-api-token-auth/",data=json.dumps(data), headers=headers)
	token = json.loads(response.text)
	return "JWT " + token['token']



