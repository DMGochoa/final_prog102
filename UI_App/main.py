import requests
import log_config
import json

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from token_singleton import token

logger = log_config.logger
URL = 'http://127.0.0.1:9000/'


class Ui(ScreenManager):
    pass


class MainApp(MDApp):

    def build(self):
        logger.debug('Starting to build the aplication')
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        return Ui()

    # Log the user
    def login(self):
        logger.debug('Called login method')
        # Validations see function definitions for more details
        validate = self.validate(
            self.root.ids.user.text, self.root.ids.password.text, self.root.ids.code.text)
        if validate:
            self.show_user_data()
            self.show_account()
            self.root.current = 'main_menu'

    # Execute the transaction, ckecking just for the amount (wich in fact does the backend )
    def transaction(self, *args):
        logger.debug(f'Transaction starting...')
        try:
            logger.debug(
                f'Transaction: try statement. reading transfer fields and preparing request')
            origin_cbu = int(self.root.ids.origin_cbu.text)
            destiny_cbu = int(self.root.ids.destiny_cbu.text)
            amount = float(self.root.ids.amount.text)
            body = {
                "transaction_type": "transaction",
                "cbu_origin": origin_cbu,
                "cbu_destiny": destiny_cbu,
                "description": "test transaction",
                "amount": amount
            }
            response = requests.post(
                'http://127.0.0.1:9000/transaction', json=body)
            if response.status_code == 200:
                logger.debug("Transaction: transaccion succesfully")
                self.show_account()
                self.show_warning_dialog(-1, "succesful transaction")
                self.clear_transaction_fields()
            else:
                logger.debug(
                    "Transaction: insuficient balance to make the transaction")
                self.show_warning_dialog(-1,
                                         response.text.strip()[1:-1].strip())
                self.clear_transaction_fields()
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Transaction: Trow HTTPError in request /transaction {http_err}')
            self.show_warning_dialog(-1, str(http_err))
            self.clear_transaction_fields()
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Transaction: Trow Connection Error in request /transaction {conn_err}')
            self.show_warning_dialog(-1, str(conn_err))
            self.clear_transaction_fields()
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Transaction: Trow Timeout in request /transaction {timeout_err}')
            self.show_warning_dialog(-1, str(timeout_err))
            self.clear_transaction_fields()
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Transaction: Trow UNKNOWN Error in request /transaction {req_err}')
            self.show_warning_dialog(-1, str(req_err))
            self.clear_transaction_fields()

    # Validate if the destiny cbu exists, and the "CONFIRM" action. Amount is processed in transaction function
    # And origin cbu is desired to be a dropdown list, so no validation needed, for the moment text field
    def validate_transaction(self):
        logger.debug(f'Validate Transaction starting...')
        try:
            logger.debug(
                f'Validate Transaction: try statement. reading transfer fields and preparing request')
            origin_cbu = int(self.root.ids.origin_cbu.text)
            destiny_cbu = int(self.root.ids.destiny_cbu.text)
            amount = float(self.root.ids.amount.text)
            response = requests.get(
                f'http://127.0.0.1:9000/account/{destiny_cbu}')
            if response.status_code == 200:
                logger.debug(f'Validate Transaction: destiny account found')
                user_data = json.loads(response.text)
                content = f"You are about to send from your account n° {origin_cbu} the amount of {amount} to the account {destiny_cbu} belonging to {user_data['first_name'].strip().upper()} {user_data['last_name'].strip().upper()} "
                self.show_transaction_dialog(content)
            else:
                logger.debug(f'Validate Transaction: CBU not found')
                self.show_warning_dialog(-1,
                                         response.text.strip()[1:-1].strip('\n').strip())
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Validate Transaction: Trow HTTPError in request /account {http_err}')
            self.show_warning_dialog(-1, str(http_err))
            self.clear_transaction_fields()
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Validate Transaction: Trow Connection Error in request /account {conn_err}')
            self.show_warning_dialog(-1, str(conn_err))
            self.clear_transaction_fields()
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Validate Transaction: Trow Timeout in request /account {timeout_err}')
            self.show_warning_dialog(-1, str(timeout_err))
            self.clear_transaction_fields()
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Validate Transaction: Trow UNKNOWN Error in request /account {req_err}')
            self.show_warning_dialog(-1, str(req_err))
            self.clear_transaction_fields()

    # Validate text fields and user credentials
    def validate(self, user, password, code):
        res = 0
        # Check for text fields
        fields = self.validate_fields(user, password, code)
        # No empty and correct access code format (numerical)
        if fields > 0:
            msg_req = self.validate_user(user, password, code)
            if msg_req == "OK":
                res = 1
            else:
                self.show_warning_dialog(-1, msg_req)
                self.clear_login_fields()
        # Invalid access code format
        elif fields == 0:
            self.show_warning_dialog(0)
            self.clear_login_fields()
        else:
            logger.debug('Validate: Some text fields are empty')
            self.show_warning_dialog(1)
            self.clear_login_fields()
        return res

    # Request to a DB and validate credentials
    def validate_user(self, user, password, code):
        logger.debug('Validate user starting...')
        res = ""
        user = {
            "username": user,
            "password": password,
            "code": int(code)
        }
        try:
            logger.debug('Validate User: try statement')
            response = requests.post('http://127.0.0.1:9000/login', json=user)
            # User
            if response.status_code == 200:
                logger.debug('Validate user: user found')
                resp = response.text.strip().split(':')
                # Final "}" char, after that blank spaces, lastly quotes
                token.set_token(resp[1][:-1].strip()[1:-1])
                res = "OK"
            else:
                res = response.text.strip()[1:-1]
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Validate User: Trow HTTPError in request login {http_err}')
            res = str(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Validate User: Trow Connection Error in request login {conn_err}')
            res = str(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Validate User: Trow Timeout in request login {timeout_err}')
            res = str(timeout_err)
        except requests.exceptions.RequestException as req_err:
            logger.error(f'Validate User: Trow UNKNOWN Error {req_err}')
            res = str(req_err)

        return res

    # Validate text fields Not empty and access code format
    def validate_fields(self, user, password, code):
        logger.debug('Validate login text fields starting...')
        res = -1
        if (user != '' and password != '' and code != ''):
            logger.debug(
                'In Validate log text fields: the fields are not empty')
            if code.isdigit():
                logger.debug(
                    'In Validate log text fields: Access code is numerical, succesful validation')
                res = 1
            else:
                logger.debug(
                    'In Validate log text fields: Access code invalid format')
                res = 0
        return res

    def show_report(self):
        # add loggers

        try:
            year = int(self.root.ids.report_year.text)
            month = int(self.root.ids.report_month.text)
            cbu = int(self.root.ids.report_cbu.text)
            body = {
                "year": year,
                "month": month,
                "cbu": cbu
            }
            response = requests.get(
                'http://127.0.0.1:9000/report_transactions', json=body)

            reports = json.loads(response.text)
            if response.status_code == 200:
                final_account = 'Final Account: \n'
                origin_account = 'Original Account: \n'
                amount = 'Amount: \n'
                desc = 'Description: \n'
                date_acc = 'Date : \n'
                for report in reports['transactions']:
                    final_account = final_account + \
                        str(report['final_account']).strip() + "\n"
                    origin_account = origin_account + \
                        str(report['origin_account']).strip() + "\n"
                    amount = amount + str(report['amount']).strip() + "\n"
                    desc = desc + report['description'].strip() + "\n"
                    date_acc = date_acc + report['date'].strip() + "\n"

                self.root.ids.rep_final_account_lbl.text = final_account
                self.root.ids.rep_origin_account_lbl.text = origin_account
                self.root.ids.rep_report_amount_lbl.text = amount
                self.root.ids.rep_description_lbl.text = desc
                self.root.ids.rep_date_lbl.text = date_acc
            else:
                self.show_warning_dialog(-1, response.text.strip()
                                         [1:-1].strip('\n').strip())
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Report: Trow HTTPError in request /transaction {http_err}')
            self.show_warning_dialog(-1, str(http_err))
            self.clear_report_fields()
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Report: Trow Connection Error in request /transaction {conn_err}')
            self.show_warning_dialog(-1, str(conn_err))
            self.clear_report_fields()
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Report: Trow Timeout in request /transaction {timeout_err}')
            self.show_warning_dialog(-1, str(timeout_err))
            self.clear_report_fields()
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Report: Trow UNKNOWN Error in request /transaction {req_err}')
            self.show_warning_dialog(-1, str(req_err))
            self.clear_report_fields()
        except:
            self.show_warning_dialog(-1, "Something went wrong")
            self.clear_report_fields()

    # print the user data (First and last name)
    def show_user_data(self):
        logger.debug('Show user data starting...')
        user_data = {}
        try:
            logger.debug('Show user data try conforming headers')
            head = {'Authorization': f'{token.get_token()}'}
            logger.debug('Show user data trying to request')
            response = requests.get(
                'http://127.0.0.1:9000/home', headers=head)
            user_data = json.loads(response.text)
            self.root.ids.user_data_lbl.text = f"WELCOME! \n {user_data['user'][0]['first_name'].title()} {user_data['user'][0]['last_name'].title()}"
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Show User: Trow HTTPError in request home {http_err}')
            # DIALOG MESSAGE HERE!! Cuidado, xq el que debería redireccionarme debería ser le dialogo
            self.root.current = 'login'
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Show User: Trow Connection Error in request home {conn_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Show User: Trow Timeout in request home {timeout_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Show User: Trow UNKNOWN Error in request home {req_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        return user_data

    # Print the account/s of an user
    def show_account(self):
        logger.debug('Show accounts starting...')
        acc_data = {}
        try:
            logger.debug('Show accounts data try conforming headers')
            head = {'Authorization': f'{token.get_token()}'}
            logger.debug('Show accounts data trying to request')
            response = requests.get(
                'http://127.0.0.1:9000/accounts', headers=head)
            acc_data = json.loads(response.text)
            # Printing the main account
            self.root.ids.acc_data_lbl.text = f"Account N°: {acc_data['accounts'][0]['cbu']} \n Balance: {acc_data['accounts'][0]['balance']}"
            # More accounts if exists
            accounts = "MORE ACCOUNTS \n"
            for i in range(len(acc_data['accounts'])):
                if i != 0:
                    accounts = accounts + \
                        f"Account N°: {acc_data['accounts'][i]['cbu']} - Balance: {acc_data['accounts'][i]['balance']} \n"
            self.root.ids.more_acc_lbl.text = accounts
            # Setting in transaction screen origin cbu as default
            self.root.ids.origin_cbu.text = f"{acc_data['accounts'][0]['cbu']}"
            # Setting in reports screen default cbu
            self.root.ids.report_cbu.text = f"{acc_data['accounts'][0]['cbu']}"
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Show User: Trow HTTPError in request home {http_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Show User: Trow Connection Error in request home {conn_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Show User: Trow Timeout in request home {timeout_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Show User: Trow UNKNOWN Error in request home {req_err}')
            # DIALOG MESSAGE HERE!!
            self.root.current = 'login'
        return acc_data

    # Display a dialog with 'cont' text (generally cbu's data, amount, and destination person )
    # with twe options to confirm the transaction or cancel
    def show_transaction_dialog(self, cont):

        dialog = MDDialog(text=cont,
                          size_hint=(0.5, 1),
                          type="simple",
                          buttons=[
                              MDFlatButton(text="Cancel",
                                           on_release=lambda x: dialog.dismiss(),
                                           ),
                              MDFlatButton(text="Confirm",
                                           on_press=self.transaction,
                                           on_release=lambda x: dialog.dismiss()
                                           )
                          ])
        dialog.open()

    # Warning dialog, originally to aware the user for troubles in login, later modified to use in a wide way
    def show_warning_dialog(self, mode, cont=""):
        if mode == 1:
            content = "Please, fill all the text fields."
        elif mode == 0:
            content = "Access code invalid format."
        else:
            content = cont

        dialog = MDDialog(text=content,
                          size_hint=(0.5, 1),
                          type="simple",
                          buttons=[
                              MDFlatButton(text="OK",
                                           on_release=lambda x: dialog.dismiss()
                                           )
                          ])
        dialog.open()

    # Clear the text fields on login screen
    def clear_login_fields(self):
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''
        self.root.ids.code.text = ''

    # Clear the text fields on transaction screen
    def clear_transaction_fields(self):
        # self.root.ids.origin_cbu.text = ''
        self.root.ids.destiny_cbu.text = ''
        self.root.ids.amount.text = ''

    def clear_report_fields(self):
        self.root.ids.rep_final_account_lbl.text = ''
        self.root.ids.rep_origin_account_lbl.text = ''
        self.root.ids.rep_report_amount_lbl.text = ''
        self.root.ids.rep_description_lbl.text = ''
        self.root.ids.rep_date_lbl.text = ''
        self.root.ids.report_year.text = ''
        self.root.ids.report_month.text = ''
        # self.root.ids.report_cbu.text = ''


if __name__ == "__main__":
    MainApp().run()
