import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button





class MyGridLayout(GridLayout):

    #initizlize infinite keywords
    def __init__(self, **kwargs):

        # Call grid layout construcotr
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 2

        # add widget
        self.add_widget(Label(text="Food: "))
        #add input
        self.food = TextInput(multiline=False)
        self.add_widget(self.food)

        # add widget
        self.add_widget(Label(text="Calories: "))
        #add input
        self.calories = TextInput(multiline=False)
        self.add_widget(self.calories)

        # add widget
        self.add_widget(Label(text="Carbs: "))
        #add input
        self.carbs = TextInput(multiline=False)
        self.add_widget(self.carbs)

        # add widget
        self.add_widget(Label(text="Fats: "))
        #add input
        self.fats = TextInput(multiline=False)
        self.add_widget(self.fats)

        # add widget
        self.add_widget(Label(text="Protein: "))
        #add input
        self.protein = TextInput(multiline=False)
        self.add_widget(self.protein)

        #submit
        self.submit = Button(text="submit", font_size=32)

        #bind
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)
    def press(self, instance):
        food = self.food.text
        calories = self.calories.text
        carbs = self.carbs.text
        fats = self.fats.text
        protein = self.protein.text

        print(f'''
        Food: {food}
        Calories: {calories}
        Carbs: {carbs}
        Fats: {fats}
        Protein {protein}
        ''')

        self.add_widget(Label(text=(f'''
        Food: {food}
        Calories: {calories}
        Carbs: {carbs}
        Fats: {fats}
        Protein {protein}
        ''')))

class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()