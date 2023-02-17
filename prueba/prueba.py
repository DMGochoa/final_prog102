import requests
import json

new_users = [{
	"first_name": "pedrito",
	"last_name": "mendoza",
	"document_id": 1234545678,
	"type": "Employee",
	"birthday": "1997-01-01",
	"country": "peru",
	"city": "lima",
	"address": "av siempreviva",
	"email": "jm@texample.com",
	"phone_number": 999555999
},
{
	"first_name": "pedrito",
	"last_name": "mendoza",
	"document_id": 9678547365,
	"type": "User",
	"birthday": "1997-01-01",
	"country": "peru",
	"city": "lima",
	"address": "av siempreviva",
	"email": "jm@texample.com",
	"phone_number": 999555999
}]

for user in new_users:
    response = requests.post('http://127.0.0.1:9000/users', json=user)
    json_response = json.loads(response.text)
    with open("user_credentials.txt", "a") as f:
        f.write(json.dumps(json_response))
