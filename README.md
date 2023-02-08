# Endpoints
## Create user
POST '/users'

```json
input
{
	"first_name": "pedrito",
	"last_name": "mendoza",
	"document_id": "1234545678",
	"type": "client-person",
	"birthday": "1997-01-01",
	"country": "peru",
	"city": "lima",
	"address": "av siempreviva",
	"email": "jm@texample.com",
	"phone_number": "999555999"
}
output
{
	"username": "pramirez",
	"password": "pe4819",
	"code": 54802436
}
```
## Login
POST /login
```json
input
{
	"username" : "jmendoza",
	"password" : "ju9254",
	"code" : 28184139
}
output
{
	"access_token": "Bearer eyJhbGciOi..."
}
```
## Home
GET /home
```json
input
# Header        Value
Authorization   "Bearer eyJhbGciOi...."
output
{
	"user": [
		{
			"address": "av siempreviva",
			"birthday": "1997-01-01",
			"city": "lima",
			...
		}
	]
}
```
