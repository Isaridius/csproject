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

DatePickerObjectSrcString = """
#:import Calendar calendar.Calendar
<Day@Button>:
    datepicker: self.parent.datepicker
    color: [1,1,1,1]
    background_color: root.color if self.text != "" else [0,0,0,0]
    disabled: True if self.text == "" else False
    on_release:
        root.datepicker.picked = [int(self.text), root.datepicker.month, root.datepicker.year]
<Week@BoxLayout>:
    datepicker: root.parent
    weekdays: ["","","","","","",""]
    Day:
        text: str(root.weekdays[0])
    Day:
        text: str(root.weekdays[1])
    Day:
        text: str(root.weekdays[2])
    Day:
        text: str(root.weekdays[3])
    Day:
        text: str(root.weekdays[4])
    Day:
        text: str(root.weekdays[5])
    Day:
        text: str(root.weekdays[6])
<WeekDays@BoxLayout>:
    Label:
        text: "Mon"
    Label:
        text: "Tue"
    Label:
        text: "Wed"
    Label:
        text: "Thu"
    Label:
        text: "Fri"
    Label:
        text: "Sat"
    Label:
        text: "Sun"
<NavBar@BoxLayout>:
    datepicker: self.parent
    Spinner:
        values: root.datepicker.months
        text: root.datepicker.months[root.datepicker.month-1]
        on_text:
            root.datepicker.month = root.datepicker.months.index(self.text)+1
    Spinner:
        values: [str(i) for i in range(1970,2100)]
        text: str(root.datepicker.year)
        on_text:
            root.datepicker.year = int(self.text)
    Widget:
    Button:
        text: "<"
        on_release:
            if root.datepicker.month == 1 and spin.text == "Month": root.datepicker.year -= 1
            if spin.text == "Month": root.datepicker.month = 12 if root.datepicker.month == 1 else root.datepicker.month - 1
            if spin.text == "Year": root.datepicker.year -= 1
    Spinner:
        id: spin
        values: ["Month","Year"]
        text: "Month"
    Button:
        text: ">"
        on_release:
            if root.datepicker.month == 12 and spin.text == "Month": root.datepicker.year += 1
            if spin.text == "Month": root.datepicker.month = 1 if root.datepicker.month == 12 else root.datepicker.month + 1
            if spin.text == "Year": root.datepicker.year += 1
<DatePicker@BoxLayout>:
    year: 2020
    month: 1
    picked: ["","",""]
    months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    calendar: Calendar()
    days: [(i if i > 0 else "") for i in self.calendar.itermonthdays(self.year, self.month)] + [""] * 14
    orientation: "vertical"
    NavBar:
    WeekDays:
    Week:
        weekdays: root.days[0:7]
    Week:
        weekdays: root.days[7:14]
    Week:
        weekdays: root.days[14:21]
    Week:
        weekdays: root.days[21:28]
    Week:
        weekdays: root.days[28:35]
    Week:
        weekdays: root.days[35:]
    Label:
        text: "" if root.picked == ["","",""] else "{}/{}-{}".format(root.picked[0], root.picked[1], root.picked[2])
"""

class DatePicker(BoxLayout):
    pass

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

mm = Builder.load_file('microMacros.kv') # mm = MicroMacro Screen Manager (short for sm)
dt = Builder.load_string(DatePickerObjectSrcString)

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
        self.app_mm = mm
        return dt
        #return mm # self.app_window
    
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