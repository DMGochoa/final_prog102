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
                self.clear_fields()
        # Invalid access code format
        elif fields == 0:
            self.show_warning_dialog(0)
            self.clear_fields()
        else:
            logger.debug('Validate: Some text fields are empty')
            self.show_warning_dialog(1)
            self.clear_fields()
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
                # PROVISORIO
                resp = response.text.strip().split(':')
                # Final "}" char, after that blank spaces, lastly quotes
                token.set_token(resp[1][:-1].strip()[1:-1])
                # PROVISORIO
                res = "OK"
            else:
                res = response.text.strip()[1:-1]
        except requests.exceptions.HTTPError as http_err:
            logger.error('Validate User: Trow HTTPError in request login')
            res = str(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                'Validate User: Trow Connection Error in request login')
            res = str(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.error('Validate User: Trow Timeout in request login')
            res = str(timeout_err)
        except requests.exceptions.RequestException as req_err:
            logger.error('Validate User: Trow UNKNOWN Error')
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

    # Clear the text fields
    def clear_fields(self):
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''
        self.root.ids.code.text = ''

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
            self.root.ids.user_data_lbl.text = f"WELCOME! \n {user_data['user'][0]['first_name']} {user_data['user'][0]['last_name']}"
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Show User: Trow HTTPError in request home {http_err}')
            self.root.current = 'login'
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Show User: Trow Connection Error in request home {conn_err}')
            self.root.current = 'login'
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Show User: Trow Timeout in request home {timeout_err}')
            self.root.current = 'login'
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Show User: Trow UNKNOWN Error in request home {req_err}')
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
        except requests.exceptions.HTTPError as http_err:
            logger.error(
                f'Show User: Trow HTTPError in request home {http_err}')
            self.root.current = 'login'
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(
                f'Show User: Trow Connection Error in request home {conn_err}')
            self.root.current = 'login'
        except requests.exceptions.Timeout as timeout_err:
            logger.error(
                f'Show User: Trow Timeout in request home {timeout_err}')
            self.root.current = 'login'
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f'Show User: Trow UNKNOWN Error in request home {req_err}')
            self.root.current = 'login'
        return acc_data


if __name__ == "__main__":
    MainApp().run()
