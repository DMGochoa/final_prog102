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
        self.send()
        # print(f"USER {self.root.ids.user.text} PASS {self.root.ids.password.text}")
        # Mandar User y Pass y esperar respuesta del back
        # Validacion a modo de ejemplo. 
        if self.root.ids.user.text == 'admin' and self.root.ids.password.text == '12345':
            if not self.dialog:
                self.dialog = MDDialog(
                    title = 'Login',
                    text = f"Bienvenido {self.root.ids.user.text}",
                    buttons = [
                        MDFlatButton(
                            text = "OK", text_color = self.theme_cls.accent_color,
                            on_release = self.close
                        ),
                    ],
                )
                self.dialog.open()

    def send(self):
        print(f"USER: {self.root.ids.user.text} PASS: {self.root.ids.password.text} Access Code: {self.root.ids.code.text}")
    

    def close(self):
        self.dialog.dismiss()


if __name__ == "__main__":
    MainApp().run()            
