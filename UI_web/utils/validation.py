import datetime
from utils.logging_web import log_web

# Setup logger
logger = log_web()

def form_val(user_data):
    validation = False
    selected_date = datetime.date.fromisoformat(user_data['birthday'])
    today = datetime.date.today()
    diff_date = today - selected_date
    logger.debug('Initiate the form validation')
    
    try:
        if len(user_data['first_name']) == 1:
            issue = 'First name empty'  
        elif len(user_data['last_name']) == 1:
            issue = 'Last name empty'
        elif user_data['document_id'] == None:
            issue = 'Document ID empty'
        elif user_data['type'] == None:
            issue = 'Type empty'
        elif 360*8 > diff_date.days:
            issue = "User or Employee must be at least 18 years old to be registered"
        elif len(user_data['country']) == 1:
            issue = 'Country is empty'
        elif len(user_data['city']) == 1:
            issue = 'City is empty'
        elif len(user_data['address']) == 1:
            issue = 'Address is empty'
        elif len(user_data['email']) == 1:
            issue = 'Email is empty' 
        elif user_data['phone_number'] == None:
            issue = 'Phone_number ID empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    except:  
        if user_data['first_name'] == None:
            issue = 'First name empty'  
        elif user_data['last_name'] == None:
            issue = 'Last name empty'
        elif user_data['document_id'] == None:
            issue = 'Document ID empty'
        elif user_data['type'] == None:
            issue = 'Type empty'
        elif 360*8 > diff_date.days:
            issue = "User or Employee must be at least 18 years old to be registered"
        elif user_data['country'] == None:
            issue = 'Country is empty'
        elif user_data['city'] == None:
            issue = 'City is empty'
        elif user_data['address'] == None:
            issue = 'Address is empty'
        elif user_data['email'] == None:
            issue = 'Email is empty' 
        elif user_data['phone_number'] == None:
            issue = 'Phone_number ID empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    return validation, issue 

def deposit_val(deposit_data):
    validation = False
    logger.debug('Initiate the deposit validation')
    
    try:
        if len(deposit_data['cbu_origin']) == None:
            issue = 'DNI is empty'  
        elif len(deposit_data['cbu_destiny']) == None:
            issue = 'CBU destiny is empty'
        elif deposit_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    except:  
        if deposit_data['cbu_origin'] == None:
            issue = 'DNI is empty'  
        elif deposit_data['cbu_destiny'] == None:
            issue = 'CBU destiny is empty'
        elif deposit_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    return validation, issue


def withdraw_val(withdraw_data):
    validation = False
    logger.debug('Initiate the withdraw validation')
    
    try:
        if len(withdraw_data['cbu_origin']) == None:
            issue = 'DNI is empty'  
        elif len(withdraw_data['cbu_destiny']) == None:
            issue = 'CBU destiny is empty'
        elif withdraw_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    except:  
        if withdraw_data['cbu_origin'] == None:
            issue = 'DNI is empty'  
        elif withdraw_data['cbu_destiny'] == None:
            issue = 'CBU destiny is empty'
        elif withdraw_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    return validation, issue

def transaction_val(transaction_data):
    validation = False
    logger.debug('Initiate the transaction validation')
    
    try:
        if len(transaction_data['cbu_origin']) == None:
            issue = 'DNI is empty'  
        elif len(transaction_data['cbu_destiny']) == None:
            issue = 'CBU destiny is empty'
        elif transaction_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    except:  
        if transaction_data['cbu_origin'] == None:
            issue = 'DNI is empty'  
        elif transaction_data['cbu_destiny'] == None:
            issue = 'CBU destiny is empty'
        elif transaction_data['amount'] == None:
            issue = 'Amount is empty'
        else:
            logger.debug('Successfull validation')
            validation = True
            issue = ''
    return validation, issue
