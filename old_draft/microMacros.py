# Import necessary modules
import kivy
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivymd.uix.pickers import MDDatePicker

from datetime import datetime
from pprint import pprint
from kivy.uix.screenmanager import ScreenManager, Screen

# Define the first screen: LoadScreen
class LoadScreen(Screen):
    def loadData(self):
        try:
            # Attempt to load saved data from a file
            with open("saved_data.txt", "r") as f:
                contents = f.read()
            microMacros.get_running_app().AllData = eval(contents)  # Safely converting string to dictionary
            pprint(microMacros.get_running_app().AllData)
        except Exception as e:
            print(f"Error loading data: {e}")

# Define the screen to manage food and dates
class DateFoodMenu(Screen):
    totalCalCounter = NumericProperty(0)  # Total calorie counter
    dfDate = datetime.today().strftime('%Y-%m-%d')  # Default date (current date)
    selectedDate = StringProperty(dfDate)  # Date property to keep track of user selection

    def openDatePicker(self):
        # Open date picker dialog
        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

    def on_save(self, instance, value, date_range):
        # Update selected date after saving
        newDate = str(value)
        self.selectedDate = newDate
        self.ids.dateLabelID.text = self.selectedDate

    def on_cancel(self, instance, value):
        # Handle cancel action in date picker
        self.ids.dateLabelID.text = "You Clicked Cancel"

    def addFoodPress(self):
        # Check if calorie input is valid
        try:
            c = int(self.ids.calInputID.text)  # Ensure input is a number
        except ValueError:
            popup = Popup(title='Error', content=Label(text='Calories must be a number'), auto_dismiss=False)
            popup.open()
            return

        # Update total calorie counter
        self.totalCalCounter += c
        self.ids.calCounterID.text = f'Total Cals: {self.totalCalCounter}'

        # Collect food input data
        food_data = {
            "name": self.ids.foodInputID.text,
            "cals": self.ids.calInputID.text,
            "proteins": self.ids.proteinInputID.text,
            "fats": self.ids.fatInputID.text,
            "carbs": self.ids.carbInputID.text
        }

        # Add food data to the global data structure
        app_data = microMacros.get_running_app().AllData
        if self.selectedDate in app_data:
            app_data[self.selectedDate].append(food_data)
        else:
            app_data[self.selectedDate] = [food_data]

    def save(self):
        # Save current data to file
        try:
            with open("saved_data.txt", "w") as f:
                f.write(str(microMacros.get_running_app().AllData))
        except Exception as e:
            print(f"Error saving data: {e}")

# Define a screen manager for navigation
class WindowManager(ScreenManager):
    pass

# Define the summary screen
class Summary(Screen):
    pass

# Main App class
class microMacros(MDApp):
    def build(self):
        # Initialize app theme and data
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.AllData = {}  # Store app data
        return Builder.load_file('microMacros.kv')  # Load UI from the .kv file

    def addFoodUpdate(self):
        # Debugging method to print current app data
        pprint(self.AllData)

if __name__ == "__main__":
    microMacros().run()
