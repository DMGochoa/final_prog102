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
## Create other account (for future sprint)
POST /accounts
```json
input
# Header        Value
Authorization   "Bearer eyJhbGciOi...."
output
{
	"account": {
		"balance": 0,
		"cbu": 10200040002,
		"user_id": 4
	}
}
```
## See all acounts
GET /accounts
```json
input
# Header        Value
Authorization   "Bearer eyJhbGciOi...."
output
{
	"accounts": [
		{
			"balance": 195,
			"cbu": 10200020001,
			"id": 2,
			"user_id": 2
		},
		{
			"balance": 0,
			"cbu": 10200020002,
			"id": 3,
			"user_id": 2
		}
	]
}
```
## See info one account (to verify before transaction)
GET /account/<int:cbu>
```json
input 
/account/<int:cbu>
output
{
	"cbu": 10200020012,
	"creation_date": "2023-10-02",
	"first_name": "pedrito",
	"last_name": "ramirez",
	"username": "pramirez2"
}
```
# Transactions
POST /transaction
## Deposit
```json
# input
{
	"transaction_type": "deposit",
	"cbu_origin": 1234567, # can be a DNI
	"cbu_destiny": 10200010001, # account to be updated
	"description": "test deposit",
	"amount": 10.0
}
```
## Withdraw
```json
# input
{
	"transaction_type": "withdraw",
	"cbu_origin": 1234567, # can be a DNI
	"cbu_destiny": 10200010001,  # account to be updated
	"description": "test withdraw",
	"amount": 10.0
}
```
## Transaction
```json
# input
{
	"transaction_type": "transaction",
	"cbu_origin": 10200010001,
	"cbu_destiny": 10200020001,
	"description": "test transaction",
	"amount": 10.0
}
```
```json
output
{
	"amount": 10.0,
	"cbu_destiny": 10200020001,
	"cbu_origin": 10200010001,
	"description": "test transaction",
	"origin_new_balance": 130.0
}
```
## Report transactions
GET /report_transactions
```json
# input
# month incorrect '01', correct '1' 
{
	"year": 2023,
	"month": 2,
	"cbu": 10200010001
}
# output
{
	"cbu": 10200010001,
	"period": "2023-02",
	"transactions": [
		{
			"amount": 190.0,
			"date": "2023-02-15",
			"description": "test deposit",
			"final_account": 10200010001,
			"origin_account": 1234567,
			"status": "True",
			"type": "deposit"
		},
		{
			"amount": 50.0,
			"date": "2023-02-15",
			"description": "test withdraw",
			"final_account": 10200010001,
			"origin_account": 1234567,
			"status": "True",
			"type": "withdraw"
		}
	]
}
```