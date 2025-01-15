# TO ACTIVATE VIRTUAL ENVIRONMENT: source venv/bin/activate
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout

class MyApp(App):
    def build(self):
        self.food_log = []  # List to store food entries
        self.custom_nutrients = []  # List to store custom nutrients for later use

        self.layout = BoxLayout(orientation='vertical')

        # Input for food name
        self.food_name_input = TextInput(hint_text='Enter food name', multiline=False)
        self.layout.add_widget(self.food_name_input)

        # Input for calories (per serving)
        self.calories_per_serving_input = TextInput(hint_text='Calories per serving', multiline=False, input_filter='int')
        self.layout.add_widget(self.calories_per_serving_input)

        # Input for protein (per serving)
        self.protein_per_serving_input = TextInput(hint_text='Protein per serving (g)', multiline=False, input_filter='int')
        self.layout.add_widget(self.protein_per_serving_input)

        # Input for fats (per serving)
        self.fat_per_serving_input = TextInput(hint_text='Fats per serving (g)', multiline=False, input_filter='int')
        self.layout.add_widget(self.fat_per_serving_input)

        # Input for carbs (per serving)
        self.carbs_per_serving_input = TextInput(hint_text='Carbs per serving (g)', multiline=False, input_filter='int')
        self.layout.add_widget(self.carbs_per_serving_input)

        # Input for serving size
        self.serving_size_input = TextInput(hint_text='Enter serving size (g)', multiline=False, input_filter='int')
        self.layout.add_widget(self.serving_size_input)

        # Custom nutrient section
        self.custom_nutrient_label = Label(text="Custom Nutrients", size_hint_y=None, height=30)
        self.layout.add_widget(self.custom_nutrient_label)

        self.custom_nutrient_name_input = TextInput(hint_text='Nutrient name (e.g. Vitamin B)', multiline=False)
        self.layout.add_widget(self.custom_nutrient_name_input)

        self.custom_nutrient_value_input = TextInput(hint_text='Nutrient value (e.g. 50 mg)', multiline=False)
        self.layout.add_widget(self.custom_nutrient_value_input)

        self.add_custom_nutrient_button = Button(text='Add Custom Nutrient', on_press=self.add_custom_nutrient)
        self.layout.add_widget(self.add_custom_nutrient_button)

        # Toggle button to show/hide custom nutrient list
        self.toggle_button = ToggleButton(text="Show Custom Nutrients", size_hint_y=None, height=40, state="down")
        self.toggle_button.bind(on_press=self.toggle_custom_nutrients)
        self.layout.add_widget(self.toggle_button)

        # Scrollable area for the custom nutrients
        self.scroll_view = ScrollView()
        self.scrollable_layout = GridLayout(cols=1, size_hint_y=None)
        self.scrollable_layout.bind(minimum_height=self.scrollable_layout.setter('height'))
        self.scroll_view.add_widget(self.scrollable_layout)
        self.layout.add_widget(self.scroll_view)

        # Button to add food
        self.add_button = Button(text='Add Food', on_press=self.add_food)
        self.layout.add_widget(self.add_button)

        # Label to display food log
        self.food_log_label = Label(text='Food log will appear here.', size_hint_y=None, height=200)
        self.layout.add_widget(self.food_log_label)

        return self.layout

    def toggle_custom_nutrients(self, instance):
        """ Toggle the visibility of custom nutrient list. """
        if self.toggle_button.state == 'down':
            self.scroll_view.height = 200  # Make the list visible
            self.toggle_button.text = "Hide Custom Nutrients"
        else:
            self.scroll_view.height = 0  # Hide the list
            self.toggle_button.text = "Show Custom Nutrients"

    def add_food(self, instance):
        food_name = self.food_name_input.text
        calories_per_serving = self.calories_per_serving_input.text
        protein_per_serving = self.protein_per_serving_input.text
        fat_per_serving = self.fat_per_serving_input.text
        carbs_per_serving = self.carbs_per_serving_input.text
        serving_size = self.serving_size_input.text

        # Get custom nutrients (if any)
        custom_nutrients = '\n'.join(self.custom_nutrients)

        if not food_name or not calories_per_serving or not protein_per_serving or not fat_per_serving or not carbs_per_serving or not serving_size:
            self.food_log_label.text = 'Please fill in all fields!'
            return

        # Calculate nutrition based on serving size
        try:
            calories = int(calories_per_serving) * int(serving_size) / 100
            protein = int(protein_per_serving) * int(serving_size) / 100
            fat = int(fat_per_serving) * int(serving_size) / 100
            carbs = int(carbs_per_serving) * int(serving_size) / 100
        except ValueError:
            self.food_log_label.text = 'Invalid input for nutrition facts or serving size!'
            return

        # Add food entry to the log
        food_entry = f"{food_name} - {calories} cal\nProtein: {protein}g, Fats: {fat}g, Carbs: {carbs}g"
        if custom_nutrients:
            food_entry += f"\nCustom Nutrients: {custom_nutrients}"

        self.food_log.append(food_entry)
        self.update_food_log()

        # Clear inputs
        self.food_name_input.text = ''
        self.calories_per_serving_input.text = ''
        self.protein_per_serving_input.text = ''
        self.fat_per_serving_input.text = ''
        self.carbs_per_serving_input.text = ''
        self.serving_size_input.text = ''

        # Clear custom nutrients input fields
        self.custom_nutrient_name_input.text = ''
        self.custom_nutrient_value_input.text = ''

    def add_custom_nutrient(self, instance):
        nutrient_name = self.custom_nutrient_name_input.text
        nutrient_value = self.custom_nutrient_value_input.text

        if not nutrient_name or not nutrient_value:
            return

        # Store the custom nutrient
        self.custom_nutrients.append(f"{nutrient_name}: {nutrient_value}")

        # Create a button for each custom nutrient to add it quickly
        custom_nutrient_button = Button(text=f"{nutrient_name}: {nutrient_value}", size_hint_y=None, height=40)
        custom_nutrient_button.bind(on_press=lambda btn, name=nutrient_name, value=nutrient_value: self.quick_add_nutrient(name, value))

        # Add the button to the scrollable area
        self.scrollable_layout.add_widget(custom_nutrient_button)

        # Clear the inputs for custom nutrient
        self.custom_nutrient_name_input.text = ''
        self.custom_nutrient_value_input.text = ''

    def quick_add_nutrient(self, name, value):
        """ Automatically fills in the nutrient values into the main form. """
        self.custom_nutrient_name_input.text = name
        self.custom_nutrient_value_input.text = value

    def update_food_log(self):
        # Update the label with the food log
        self.food_log_label.text = '\n\n'.join(self.food_log)


if __name__ == "__main__":
    MyApp().run()
