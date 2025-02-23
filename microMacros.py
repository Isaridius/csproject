from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import ScreenManager, Screen

import kivy.properties

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

# class DatePicker(Screen):
#     pass

class DateFoodMenu(Screen):
    totalCalCounter = 0

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

    
mm = Builder.load_file('microMacros.kv')

class microMacros(App):

    def build(self):
        # self.food_list = [] #save this to .csv
        # self.totalCals = NumericProperty(10)
        # self.totalCalsTestStr = "TESTHERE"
        # self.nutrients = []
        # self.sumCalStr = StringProperty('0')
        #sm = ScreenManager()
        #sm.add_widget(LoadScreen(name="LoadScreen"))

        self.AllData = {} # load from .csv

        return mm # self.app_window
    def addFoodUpdate(self):
        print(self)
        self.AllData['23/02/25'] = [
            {
                'name': self.ids.FoodScreenID.ids.LayoutID.ids.foodInputID.text
            },
            
        ]

        print("Yes")
        print(self.AllData)
 

if __name__ == "__main__":
    microMacros().run()