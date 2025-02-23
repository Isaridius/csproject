from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

import kivy.properties

class microMacros(App):
    def build(self):

        self.food_list = [] #save this to .csv
        self.totalCals = 0
        self.nutrients = [] 

        self.sumCalStr = StringProperty('0')

        self.app_window = BoxLayout(orientation='vertical')

        self.appLogoImg = Image(source="logo.png")
        self.app_window.add_widget(self.appLogoImg)

        self.sumCalLabel = Label(text="Total Cals:" + str(self.totalCals))
        self.app_window.add_widget(self.sumCalLabel)

        self.FoodNameInput = TextInput(hint_text='Enter food name', multiline=False)
        self.app_window.add_widget(self.FoodNameInput)

        self.CalorieInput = TextInput(hint_text='Enter calories',input_filter="float")
        self.app_window.add_widget(self.CalorieInput)

        self.CarbsInput = TextInput(hint_text='Enter carbs',input_filter="float")
        self.app_window.add_widget(self.CarbsInput)
        
        self.ProteinsInput = TextInput(hint_text='Enter protein amount',input_filter="float")
        self.app_window.add_widget(self.ProteinsInput)

        self.FatsInput = TextInput(hint_text='Enter fats total',input_filter="float")
        self.app_window.add_widget(self.FatsInput)

        self.AddFoodBtn = Button(text="Add Food")
        self.AddFoodBtn.bind(on_press=self.addFoodCallback)
        self.app_window.add_widget(self.AddFoodBtn)

        return self.app_window

    def addFoodCallback(self, instance):
        self.totalCals = self.totalCals + float(self.CalorieInput.text)
        self.sumCalLabel.text = "Total Cals: " + str(self.totalCals)
        #do nothing

if __name__ == "__main__":
    microMacros().run()