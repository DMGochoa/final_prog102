
import requests
import log_config
import json

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

logger = log_config.logger


class Ui(ScreenManager):
    pass


class MainApp(MDApp):
    dialog = None  # Maybe not more usefull since self.validate_fields() construc his own dialog

    def build(self):
        logger.debug('Starting to build the aplication')
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')

        return Ui()

    # Log the user
    def login(self):
        logger.debug('Called login method')
        validate = self.validate(
            self.root.ids.user.text, self.root.ids.password.text, self.root.ids.code.text)
        if validate:
            # Hacer request.post(http://127.0.0.1:9000/account)
            # Class client account, balance, username, first name, last name,
            # client = new_client(first_name, last_name, account, balance) entre otras cosas
            #
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
        fields = self.validate_fields(user, password, code)

        if fields > 0:
            logger.debug(
                'Validate: the text fields are not empty and Acces Code is numeric')
            msg_req = self.validate_user(user, password, code)
            if msg_req == "OK":
                res = 1
            else:
                self.show_warning_dialog(-1, msg_req)

        elif fields == 0:
            logger.debug('Validate: Acces Code invalid format')
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
            # if "access_token" in response.text:
            if response.status_code == 200:
                logger.debug('Validate user: user found')
                res = "OK"
            else:
                res = response.text.strip()[1:-1]
        except requests.exceptions.HTTPError as http_err:
            logger.debug('Validate User: try statement')
            print(f"HTTP ERROR: {http_err}")
            res = str(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.debug('Validate User: try statement')
            print(f"CONNECTION ERROR: {conn_err}")
            res = str(conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logger.debug('Validate User: try statement')
            print(f"TIMEOUT ERROR: {timeout_err}")
            res = str(timeout_err)
        except requests.exceptions.RequestException as req_err:
            logger.debug('Validate User: try statement')
            print(f"UNKNOWN ERROR: {req_err}")
            res = str(req_err)

        return res

    # Validate text fields Not empty and access code format
    def validate_fields(self, user, password, code):
        logger.debug('Validating the login text fields')
        res = -1
        if (user != '' and password != '' and code != ''):
            logger.debug('In validating: the fields are not empty')
            if code.isdigit():
                logger.debug(
                    'In validating: Access code is numerical, succesful validation')
                res = 1
            else:
                logger.debug('In validating: Access code invalid format')
                res = 0
        return res

    # Clear the text fields
    def clear_fields(self):
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''
        self.root.ids.code.text = ''


if __name__ == "__main__":
    MainApp().run()
