from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.popup import Popup
from datetime import datetime

class DateFoodMenu(Screen):
    totalCalCounter = NumericProperty(0)
    dfDate = datetime.today().strftime('%Y-%m-%d')
    selectedDate = StringProperty(dfDate)

    def openDatePicker(self):
        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

    def on_save(self, instance, value, date_range):
        self.selectedDate = str(value)
        self.ids.dateLabelID.text = self.selectedDate

    def on_cancel(self, instance, value):
        self.ids.dateLabelID.text = "You Clicked Cancel"

    def addFoodPress(self):
        try:
            c = int(self.ids.calInputID.text)
        except ValueError:
            popup = Popup(title='Error', content=Label(text='Calories must be a number'), auto_dismiss=False)
            popup.open()
            return

        self.totalCalCounter += c
        self.ids.calCounterID.text = f'Total Cals: {self.totalCalCounter}'

        food_data = {
            "name": self.ids.foodInputID.text,
            "cals": self.ids.calInputID.text,
            "proteins": self.ids.proteinInputID.text,
            "fats": self.ids.fatInputID.text,
            "carbs": self.ids.carbInputID.text
        }

        app_data = microMacros.get_running_app().AllData
        if self.selectedDate in app_data:
            app_data[self.selectedDate].append(food_data)
        else:
            app_data[self.selectedDate] = [food_data]

    def save(self):
        try:
            with open("data/saved_data.txt", "w") as f:
                f.write(str(microMacros.get_running_app().AllData))
        except Exception as e:
            print(f"Error saving data: {e}")
