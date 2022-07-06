from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

class CreateAccountWindow(Screen):
    uname=ObjectProperty(None)
    email=ObjectProperty(None)
    password=ObjectProperty(None)
    # add user to database if email and password input is validated
    def submit(self):
        if self.uname.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".")>0:
            if self.password != "":
                db.add_user(self.email.text,self.password.text,self.uname.text)
                self.reset()
                sm.current="login"
            else:
                invalidForm()
        else:
            invalidForm()

    # go to login page
    def login(self):
        self.reset()
        sm.current="login"

    def reset(self):
        self.email.text=""
        self.password.text = ""
        self.uname.text = ""

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    # log in to main window if email and password match
    def loginBtn(self):
        if db.validate(self.email.text,self.password.text):
            MainWindow.currentEmail = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    # go to create account page
    def createBtn(self):
        self.reset()
        sm.current="create"

    def reset(self):
        self.email.text=""
        self.password.text=""

class MainWindow(Screen):
    accountName = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    currentEmail=""

    # get user information display on the window
    def on_enter(self):
        password,name,created = db.get_user(self.currentEmail)
        self.accountName.text = "Account Name: "+name
        self.email.text="Email: "+self.currentEmail
        self.created.text = "Created On: "+created

# manage windows
class WindowManager(ScreenManager):
    pass

# pop up window for invalid login
def invalidLogin():
    pop=Popup(title='Invalid Login',content=Label(text='Invalid username or password.'),size_hint=(None,None),size=(600,600))
    pop.open()
# pop up window for invalid form
def invalidForm():
    pop=Popup(title='Invalid Form',content=Label(text='Please fill in all inputs with valid information.'),size_hint=(None,None),size=(400,400))
    pop.open()

kv = Builder.load_file("my.kv")
sm=WindowManager()
db = DataBase("users.txt")
# add widget to each window
screens=[LoginWindow(name="login"),CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)
sm.current="login"

# create application
class MyMainApp(App):
    def build(self):
        return sm

# run app
if __name__ == '__main__':
    MyMainApp().run()
