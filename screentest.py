#Imports libaries
import kivy
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
import json
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen


#Define screens

class SummaryScreen(Screen):
    pass


class LogScreen(Screen):

    pass


class GoalsScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass




# Designate Our .kv design file
build = Builder.load_file('screentest.kv')



class screenTest(App):
    def build(self):
        return build


    def change_date(self, instance):
        print("please work")
        pass

    def change_text(self, instance):
        print(f"{instance.text} button pressed")  # Example: Display the button's text
        print("SHOULD GET HERE")

        summary_screen = self.root.get_screen('SummaryScreen')

        summary_screen.ids.greetings.text = "HELP PLEASE I BEG OF YOU"
        print("Are we cooked?")


    def change_text_two(self, instance):
        print(f"{instance.text} button pressed")  # Example: Display the button's text
        print("SHOULD GET HERE")

        summary_screen = self.root.get_screen('SummaryScreen')

        summary_screen.ids.greetings.text = "PLEASE PLEASE PLEASE PLEASE HELP"
        print("Are we cooked?")


if __name__ == '__main__':
    screenTest().run()