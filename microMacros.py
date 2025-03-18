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

# iPhone 15 Pro Max aspect ratio (19.5:9)
target_height = 900  # Adjust as needed
target_width = int(target_height * (9 / 19.5))

Window.size = (target_width, target_height)
# Window.fullscreen = 'auto'


class microMacros(MDApp):
    def build(self):
        #Dark Mode
        self.theme_cls.theme_style = "Dark"  # Enables dark mode
        self.theme_cls.primary_palette = "Teal"  # Change primary color if needed

        self.load_food_log()  # Load food log from JSON

        #Initialize the counters
        self.total_cals = 0
        self.total_carbs = 0
        self.total_fats = 0
        self.total_protein = 0

        #Initalize the window
        self.window = GridLayout(
            cols=1, 
            pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
        
        #Create Logo
        self.window.add_widget(
            Image(source="logo.png")
            )

        #Make the greeting and the updated text
        self.greeting = Label(
            text="Insert data for this session", 
            font_size=30, 
            color='AAAAAA'
            )

        #Add the greeting (It's separate)
        self.window.add_widget(self.greeting)

        #Input Food Name
        self.foodname = TextInput(multiline=False, hint_text="Enter food name")
        self.window.add_widget(self.foodname)

        #Input cals
        self.cals = TextInput(multiline=False, input_filter="float", hint_text="Enter calories (kcal)")
        self.window.add_widget(self.cals)

        #Input carbs
        self.carbs = TextInput(multiline=False, input_filter="float", hint_text="Enter carbohydrates (g)")
        self.window.add_widget(self.carbs)

        #Input fats
        self.fats = TextInput(multiline=False, input_filter="float", hint_text="Enter fats (g)")
        self.window.add_widget(self.fats)

        #Input protein
        self.protein = TextInput(multiline=False, input_filter="float", hint_text="Enter protein (g)")
        self.window.add_widget(self.protein)

        #Create calendar button & Redirect to Calendar function
        self.calendar_btn = Button(text="Open Calendar")
        self.calendar_btn.bind(on_press=self.show_date_picker)
        self.window.add_widget(self.calendar_btn)

        # Date label with today's date as default
        self.currentDate = Label(
            text=str(datetime.today().date()),  # Automatically sets today's date
            font_size=25,
            color='AAAAAA'
            )
        self.window.add_widget(self.currentDate)

        #Create log button & Redirect to LOG function
        self.logbutton = Button(text="LOG", bold=True, background_color='00FFCE')
        self.logbutton.bind(on_press=self.display_nutrient_tally)
        self.window.add_widget(self.logbutton)

        #Create Scrollable Food Log Display
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.log_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter("height"))
        self.scroll_view.add_widget(self.log_layout)
        self.window.add_widget(self.scroll_view)

        self.update_displayed_log()  # Populate scroll view with existing data

        return self.window

    #Save the date
    def on_save(self, instance, value, date_range):
        self.currentDate.text = str(value)

    #Either say canceled or just return to previous date
    def on_cancel(self, instance, value):
        # self.currentDate.text = "Canceled"
        return

    #The actual function for picking the date
    def show_date_picker(self, instance):

        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

    #Displaying nutrition log in the scroll wheel
        #This is where a lot of stuff happens, and is the functionality of the LOG button
    def display_nutrient_tally(self, instance):
        #Try this
        try:
            #Convert input text to float values (default to 0 if empty)
            cals = float(self.cals.text) if self.cals.text else 0
            carbs = float(self.carbs.text) if self.carbs.text else 0
            fats = float(self.fats.text) if self.fats.text else 0
            protein = float(self.protein.text) if self.protein.text else 0
            food_name = self.foodname.text.strip()

            #Ensures food name is provided
            if not food_name:
                self.greeting.text = "Food name cannot be empty!"
                return

            #gets selected or default date
            current_date = self.currentDate.text if self.currentDate.text != "Remember to put the date" else str(datetime.today().date())

            #Edits existing entry
            if hasattr(self, "editing_food") and self.editing_food:
                old_date, old_food_name = self.editing_food

                # Delete old entry if food name changed
                if old_food_name != food_name and old_date in self.food_log and old_food_name in self.food_log[old_date]:
                    del self.food_log[old_date][old_food_name]

                # Remove editing mode safely
                del self.editing_food
            else:
                old_date, old_food_name = None, None  # Avoid using uninitialized variables

            #Add entry to the food log
            if current_date not in self.food_log:
                self.food_log[current_date] = {}

            self.food_log[current_date][food_name] = {
                "cals": cals,
                "carbs": carbs,
                "fats": fats,
                "protein": protein
            }

            #Update total values
            self.total_cals += cals
            self.total_carbs += carbs
            self.total_fats += fats
            self.total_protein += protein

            #Update UI with new totals in greeting text
            self.greeting.text = f"Cals: {self.total_cals}, Carbs: {self.total_carbs}, Fats: {self.total_fats}, Protein: {self.total_protein}"

            #Save log and update the display
            self.save_food_log()
            self.update_displayed_log()

            #Clear input fields
            self.foodname.text = ""
            self.cals.text = ""
            self.carbs.text = ""
            self.fats.text = ""
            self.protein.text = ""

        except ValueError:
            self.greeting.text = "Invalid input, enter numbers only!"

    #Saves self.food_log into a JSON file
    def save_food_log(self):
        try:
            with open("food_log.json", "w") as file:
                json.dump(self.food_log, file)
        except Exception as e:
            print(f"Error saving food log: {e}")

    #Loads food_log.json into the scroll widget
    def load_food_log(self):
        try:
            with open("food_log.json", "r") as file:
                self.food_log = json.load(file)

            #Initalizes the total stuff
            self.total_cals = 0
            self.total_carbs = 0
            self.total_fats = 0
            self.total_protein = 0

            #Tallies up all the food in JSON
            for date in self.food_log:
                for food in self.food_log[date].values():
                    self.total_cals += food["cals"]
                    self.total_carbs += food["carbs"]
                    self.total_fats += food["fats"]
                    self.total_protein += food["protein"]

            #Puts in greeting text
            self.greeting.text = f"(Cals: {self.total_cals}, Carbs: {self.total_carbs}, Fats: {self.total_fats}, Protein: {self.total_protein})"

        except FileNotFoundError:
            self.food_log = {}
        except Exception as e:
            print(f"Error loading food log: {e}")

    #Updates displayed scroll food log in UI
    def update_displayed_log(self):
        #Dynamically updates the displayed food log in the UI with daily totals, double spacing, and left alignment.
        self.log_layout.clear_widgets()  # Clear previous data

        for date, foods in sorted(self.food_log.items(), reverse=True):  # Sort dates in descending order
            # Calculate daily totals
            total_cals = sum(details['cals'] for details in foods.values())
            total_carbs = sum(details['carbs'] for details in foods.values())
            total_fats = sum(details['fats'] for details in foods.values())
            total_protein = sum(details['protein'] for details in foods.values())

            # Add the date as a header
            date_label = Label(
                text=f"[b]{date}[/b]",
                markup=True,
                size_hint_y=None,
                height=50,  # Add extra spacing
                halign="left"
            )
            self.log_layout.add_widget(Label(size_hint_y=None, height=10))  # Empty space for padding
            self.log_layout.add_widget(date_label)

            # Add daily total summary
            total_label = Label(
                text=f"[b]Total:[/b] {total_cals} kcal | [b]Carbs:[/b] {total_carbs}g | [b]Fats:[/b] {total_fats}g | [b]Protein:[/b] {total_protein}g",
                markup=True,
                size_hint_y=None,
                height=50,
                halign="left"
            )
            self.log_layout.add_widget(total_label)
            self.log_layout.add_widget(Label(size_hint_y=None, height=10))  # Extra space

            for food, details in foods.items():
                # Add food name and kcal
                food_label = Label(
                    text=f"{food}: {details['cals']} kcal",
                    size_hint_y=None,
                    height=40,  # Double space
                    halign="left"
                )
                self.log_layout.add_widget(food_label)

                # Add macronutrient breakdown
                nutrients_label = Label(
                    text=f"Carbs: {details['carbs']}g  |  Fats: {details['fats']}g  |  Protein: {details['protein']}g",
                    size_hint_y=None,
                    height=40,  # Double space
                    halign="left"
                )
                self.log_layout.add_widget(nutrients_label)


                edit_button = Button(
                    text="Edit",
                    size_hint_y=None,
                    height=40
                )
                edit_button.bind(on_press=lambda instance, d=date, f=food: self.edit_food_entry(d, f))

                delete_button = Button(
                    text="Delete (CAUTION)",
                    size_hint_y=None,
                    height=40,
                    background_color=(1, 0, 0, 1)  # Red button
                )
                delete_button.bind(on_press=lambda instance, d=date, f=food: self.delete_food_entry(d, f))

                button_layout = BoxLayout(size_hint_y=None, height=40)
                button_layout.add_widget(edit_button)
                button_layout.add_widget(delete_button)

                self.log_layout.add_widget(button_layout)

    def edit_food_entry(self, date, food_name):
    #Loads selected food entry into input fields for editing.
        if date in self.food_log and food_name in self.food_log[date]:
            entry = self.food_log[date][food_name]

            # Prefill input fields with existing values
            self.foodname.text = food_name
            self.cals.text = str(entry["cals"])
            self.carbs.text = str(entry["carbs"])
            self.fats.text = str(entry["fats"])
            self.protein.text = str(entry["protein"])
            self.currentDate.text = date  # Set date to selected entry

            # Temporary store the food being edited
            self.editing_food = (date, food_name)


    def delete_food_entry(self, date, food_name):
        #Removes a food entry and updates the UI.
        if date in self.food_log and food_name in self.food_log[date]:
            del self.food_log[date][food_name]

            # Remove the date entry if empty
            if not self.food_log[date]:
                del self.food_log[date]

            self.save_food_log()
            self.update_displayed_log()


#run app
if __name__ == "__main__":
    microMacros().run()