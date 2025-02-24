from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivymd.uix.pickers import MDDatePicker
#from kivymd.uix.picker import MDDatePicker

from kivy.uix.screenmanager import ScreenManager, Screen

import kivy.properties

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

# class DatePicker(Screen):
#     pass

class DateFoodMenu(Screen):
    totalCalCounter = 0
    
    def openDatePicker(self):
        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

    #Click Ok
    def on_save(self, instance, value, date_range):
        #print(instance, value, date_range)
        self.root.ids.date_label.text = str(value)


    #Click Cancel
    def on_cancel(self, instance, value):
        self.root.ids.date_label.text = "You Clicked Cancel"

    def addFoodPress(self):
        #print(self.ids, self.name)
        cf = self.ids.calInputID.text #check field
        #print(cf)
        # if not cf:
        #     popup = Popup(title='Error', content=Label(text='Fill all fields'),auto_dismiss=False)
        #     popup.open()
        c = int(self.ids.calInputID.text)
        #print(str(c))
        self.totalCalCounter = self.totalCalCounter + c
        self.ids.calCounterID.text = f'Total Cals: {str(self.totalCalCounter)}'
        #self.ids.calCounterID.text = 'Total Cals: ' + str(self.totalCalCounter)

class WindowManager(ScreenManager):
    pass
class LoadScreen(Screen):
    pass
class Summary(Screen):
    pass


class microMacros(MDApp):
    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Orange"
        # self.food_list = [] #save this to .csv
        # self.totalCals = NumericProperty(10)
        # self.totalCalsTestStr = "TESTHERE"
        # self.nutrients = []
        # self.sumCalStr = StringProperty('0')
        #sm = ScreenManager()
        #sm.add_widget(LoadScreen(name="LoadScreen"))
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.AllData = {} # load from .csv
        #self.app_mm = mm
        return Builder.load_file('microMacros.kv')  # self.app_window
        #Click Ok


    def addFoodUpdate(self):
        print(self)
        print(self.app_mm)
        print(self.app_mm.ids)

        print(self.app_mm.ids.DateFoodMenuID.ids)
        print(self.app_mm.ids.DateFoodMenuID.ids.LayoutID.ids)

        self.AllData['23/02/25'] = [
            {
                'name': str(self.app_mm.ids.DateFoodMenuID.ids.foodInputID.text)
            },
            
        ]
        print("Yes")
        print(self.AllData)
 

if __name__ == "__main__":
    microMacros().run()