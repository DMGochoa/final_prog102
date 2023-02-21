import os
import json
import random
import requests

data_dir= os.path.join(os.path.dirname(__file__), '..', 'data')
user_json = os.path.join(data_dir, 'new_us.json')
list_login = list()
print(os.path.dirname(__file__))
print(data_dir)
with open(user_json) as f_json:
    new_users = json.load(f_json)

for user in new_users:
    # Create new users
    response = requests.post('http://127.0.0.1:9000/users', json=user)
    # Load the response info for login
    login_data = json.loads(response.text)
    
    # Dictionary to login
    login = {"username": login_data["username"], 
             "password": login_data["password"], 
             "code": login_data["code"]}

    token = requests.post('http://127.0.0.1:9000/login', json=login)
    cbu = login_data['account_cbu']
    login_data['account_cbu'] = [cbu]
    if user['type'] == 'User':
        the_token = json.loads(token.text)['access_token']
        # new account
        if random.randint(0, 1) == 1:
            new_account = requests.post('http://127.0.0.1:9000/accounts', headers={'Authorization':the_token})
            account = json.loads(new_account.text)
            login_data['account_cbu'].append(account['account']['cbu'])
        if random.randint(0, 1) == 1:
            new_account = requests.post('http://127.0.0.1:9000/accounts', headers={'Authorization':the_token})
            account = json.loads(new_account.text)
            login_data['account_cbu'].append(account['account']['cbu'])
        list_login.append(login_data)
        
    # Save the info for login
    with open(os.path.join(data_dir, 'new_us.txt'), "a") as f:
        f.write('\n ' + user['type'] + json.dumps(login_data))


for i in range(len(list_login)):
    for account in list_login[i]['account_cbu']:
        # Dictionary to login
        login = {"username": list_login[i]["username"], 
                "password": list_login[i]["password"], 
                "code": list_login[i]["code"]}

        token = requests.post('http://127.0.0.1:9000/login', json=login)
        the_token = json.loads(token.text)['access_token']
            
        new_account = requests.get('http://127.0.0.1:9000/home', headers={'Authorization':the_token})
        user_info = json.loads(new_account.text)['user'][0]

        deposit_info = {
                    "transaction_type": "deposit",
                    "cbu_origin": user_info['document_id'],
                    "cbu_destiny": account,
                    "description": "test deposit",
                    "amount": 5000.0
                }
        requests.post('http://127.0.0.1:9000/transaction', json=deposit_info)
        
        copy_list = list_login.copy()
        copy_list.pop(i)

        for _ in range(50):
            choice_account = random.choice(random.choice(copy_list)['account_cbu'])
            
            transac_info = {
                    "transaction_type": "transaction",
                    "cbu_origin": account,
                    "cbu_destiny": choice_account,
                    "description": "test deposit",
                    "amount": round(25 * random.random(), 2)
                }
            
            requests.post('http://127.0.0.1:9000/transaction', json=transac_info)
            
#print(list_login)
    