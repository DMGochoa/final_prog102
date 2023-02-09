from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager


class Ui(ScreenManager):
    pass


class MainApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')

        return Ui()

    def login(self):
        validate_access = self.validate(self.root.ids.user.text, self.root.ids.password.text, self.root.ids.code.text )
        self.send()
        if validate_access > 0:
            self.root.current = 'main_menu'
        elif validate_access == 0:
            self.show_warning_dialog(0)
            self.clear_fields()
        else:    
            self.show_warning_dialog()
            self.clear_fields()
            
    def show_warning_dialog(self, mode=1):
        if mode:
            content = "Please, fill all the text fields."
        else:
            content = "Access code invalid format."    
        dialog = MDDialog(  text = content,
                            size_hint=(0.5, 1),
                            type="simple",
                            buttons=[
                                MDFlatButton(text="OK", 
                                             on_release = lambda x: dialog.dismiss()
                                             )
                            ])
        dialog.open()

    def send(self):
        print(
            f"USER: {self.root.ids.user.text} PASS: {self.root.ids.password.text} Access Code: {self.root.ids.code.text}")
  
    def show(self):
        pass
   
    def validate(self, user, password, code):
        res = -1
        if (user != '' and password != '' and code != ''):
            if code.isdigit():
                res = 1
            else:
                res = 0
        return res    
        

    def clear_fields(self):
        self.root.ids.user.text = ''
        self.root.ids.password.text = ''
        self.root.ids.code.text = ''


if __name__ == "__main__":
    MainApp().run()
