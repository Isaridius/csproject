from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

class LoadScreen(Screen):
    def loadData(self):
        try:
            with open("data/saved_data.txt", "r") as f:
                contents = f.read()
            microMacros.get_running_app().AllData = eval(contents)
            print("Loaded Data:", microMacros.get_running_app().AllData)
        except Exception as e:
            print(f"Error loading data: {e}")
