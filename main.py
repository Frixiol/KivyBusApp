import kivy
from kivy.app import App
from kivy.uix.screenmanager import  Screen

class MainScreen(Screen):

    def btn(self):
        pass

class MyApp(App):

    def build(self):
        return MainScreen()

if __name__ ==  "__main__":
    MyApp().run()
