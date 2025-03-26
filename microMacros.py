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
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock

# iPhone 15 Pro Max aspect ratio (19.5:9)
target_height = 900  # Adjust as needed
target_width = int(target_height * (9 / 19.5))
Window.size = (target_width, target_height)
# Window.fullscreen = 'auto'

class SummaryScreen(Screen):
    def refresh_summary(self):
        app = App.get_running_app()

        # Clear existing widgets and display updated summary
        summary_layout = self.ids.summary_layout
        summary_layout.clear_widgets()

        if app.current_date in app.food_log:
            foods = app.food_log[app.current_date]

            # Display a daily summary
            total_cals = sum(food["cals"] for food in foods.values())
            summary_label = Label(text=f"Total Calories for {app.current_date}: {total_cals}")
            summary_layout.add_widget(summary_label)

            # List food items
            for food, details in foods.items():
                food_label = Label(text=f"{food}: {details['cals']} kcal")
                summary_layout.add_widget(food_label)
    #Save the date
    def on_save(self, instance, value, date_range):
        mm =  microMacros.get_running_app()
        mm.current_date = str(value)
        self.ids.currentDate.text = mm.current_date
        mm.update_displayed_log(mm.current_date)

    #Either say canceled or just return to previous date
    def on_cancel(self, instance, value):
        # self.currentDate.text = "Canceled"
        # self.root.ids.currentDate.text = str(self.current_date)
        # self.update_displayed_log(self.current_date)
        return

    #The actual function for picking the date
    def show_date_picker(self, instance):
        print("Should be opening date picker")
        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

class LogScreen(Screen):
    #Saves self.food_log into a JSON file
    def save_food_log(self):
        mm= microMacros.get_running_app()
        fl = mm.food_log
        if mm.current_date not in fl:
            fl[mm.current_date] = {}
        fl[mm.current_date][self.ids.foodname.text] = { # cannot add 2 foods of the same name on the same day - dict error
            "cals": float(self.ids.cals.text),
            "carbs": float(self.ids.carbs.text),
            "fats": float(self.ids.fats.text),
            "protein": float(self.ids.protein.text)
        }
        
        try:
            with open("food_log.json", "w") as file:
                json.dump(microMacros.get_running_app().food_log, file)
        except Exception as e:
            print(f"Error saving food log: {e}")
        mm.update_displayed_log(mm.current_date)

class GoalsScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class microMacros(MDApp):
    #Initialize the existence 
    food_log = None
    with open("food_log.json", "r") as file:
        food_log = json.load(file)
    #Initialize the counters (IDK if I will need this)
    total_cals = 0
    total_carbs = 0
    total_fats = 0
    total_protein = 0
    # today = datetime.today().strftime('%Y-%m-%d')
    current_date = str(datetime.today().date())  

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        self.load_food_log()  # Load saved log on startup
        
        # Load .kv file (which defines the WindowManager and all screens)
        build = Builder.load_file('microMacros.kv')

        # Update the displayed log for today's date AFTER building the UI
        self.update_displayed_log(self.current_date)
    #Displaying nutrition log in the scroll wheel. This is where a lot of stuff happens, and is the functionality of the LOG button
    def display_nutrient_tally(self, instance): #this might be deleted perhaps...
        #Try this
        try:
            #Convert input text to float values (default to 0 if empty)
            cals = float(self.ids.cals.text) if self.ids.cals.text else 0
            carbs = float(self.ids.carbs.text) if self.ids.carbs.text else 0
            fats = float(self.ids.fats.text) if self.ids.fats.text else 0
            protein = float(self.root.ids.protein.text) if self.ids.protein.text else 0
            food_name = self.root.ids.foodname.text.strip()

            #Ensures food name is provided
            if not food_name:
                self.root.ids.greeting.text = "Food name cannot be empty!"
                return

            #gets selected or default date
            current_date = self.root.ids.currentDate.text if self.root.ids.currentDate.text != "Remember to put the date" else str(datetime.today().date())

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
            self.root.ids.greeting.text = f"Cals: {self.total_cals}, Carbs: {self.total_carbs}, Fats: {self.total_fats}, Protein: {self.total_protein}"

            #Save log and update the display
            self.save_food_log()
            self.update_displayed_log(self.today)

            #Clear input fields
            self.root.ids.foodname.text = ""
            self.root.ids.cals.text = ""
            self.root.ids.carbs.text = ""
            self.root.ids.fats.text = ""
            self.root.ids.protein.text = ""

        except Exception as e:
            self.root.ids.greeting.text = "Invalid input, enter numbers only!"

    def load_food_log(self):
        """
        Loads the food log from a JSON file and calculates totals for calories, carbs, fats, and protein.
        Updates the greeting label to display these totals.
        """
        try:
            with open("food_log.json", "r") as file:
                self.food_log = json.load(file)

            # Initialize totals
            self.total_cals = 0
            self.total_carbs = 0
            self.total_fats = 0
            self.total_protein = 0

            # Tally up totals from the JSON
            for date, foods in self.food_log.items():
                for food_details in foods.values():
                    self.total_cals += food_details["cals"]
                    self.total_carbs += food_details["carbs"]
                    self.total_fats += food_details["fats"]
                    self.total_protein += food_details["protein"]

            # Update the greeting label in the UI
            self.root.ids.greeting.text = (
                f"(Cals: {self.total_cals}, Carbs: {self.total_carbs}, "
                f"Fats: {self.total_fats}, Protein: {self.total_protein})"
            )
            print("Food log loaded successfully!")

        except FileNotFoundError:
            print("No food log found. Initializing an empty log.")
            self.food_log = {}
        except Exception as e:
            print(f"Error loading food log: {e}")

    def update_displayed_log(self, date=None):
        try:
            print(self)
            print(self.root)
            print(self.root.get_screen("SummaryScreen"))
            print(self.root.get_screen("SummaryScreen").ids.log_layout)
            self.root.get_screen("SummaryScreen").ids.log_layout.clear_widgets()
            s =  self.root.get_screen("SummaryScreen")
            ll = s.ids.log_layout
            ll.clear_widgets()

        except Exception:
            print(Exception)
    
        print("Cleared previous data")

        if date:  # Show data for a specific date
            foods = self.food_log.get(date, {})
            if not foods:
                s = self.root.get_screen("SummaryScreen")
                ll = s.ids.log_layout
                ll.add_widget(
                    Label(text="No food logged for this date.", size_hint_y=None, height=40)
                )
            else:
                self._add_date_header(date)
                self._add_daily_summary(foods)
                self._add_food_entries(date, foods)
        else:  # Show data for all dates
            for log_date, foods in sorted(self.food_log.items(), reverse=True):
                self._add_date_header(log_date)
                self._add_daily_summary(foods)
                self._add_food_entries(log_date, foods)

    def _add_date_header(self, date):
        """
        Adds a header for the given date to the log layout.
        """
        date_label = Label(
            text=f"[b]{date}[/b]",
            markup=True,
            size_hint_y=None,
            height=50
        )
        
        s = self.root.get_screen("SummaryScreen")
        ll = s.ids.log_layout

        ll.add_widget(date_label)
        ll.add_widget(Label(size_hint_y=None, height=10))  # Spacer

    def _add_daily_summary(self, foods):
        """
        Calculates and adds a daily summary of totals to the log layout.
        """
        total_cals = sum(food["cals"] for food in foods.values())
        total_carbs = sum(food["carbs"] for food in foods.values())
        total_fats = sum(food["fats"] for food in foods.values())
        total_protein = sum(food["protein"] for food in foods.values())

        total_label = Label(
            text=(
                f"[b]Total:[/b] {total_cals} kcal | [b]Carbs:[/b] {total_carbs}g | "
                f"[b]Fats:[/b] {total_fats}g | [b]Protein:[/b] {total_protein}g"
            ),
            markup=True,
            size_hint_y=None,
            height=50
        )
        s = self.root.get_screen("SummaryScreen")
        ll = s.ids.log_layout
        ll.add_widget(Label(size_hint_y=None, height=10))  # Spacer

    def _add_food_entries(self, date, foods):
        """
        Adds individual food entries with Edit and Delete buttons.
        """
        for food, details in foods.items():
            # Food name and macronutrient info
            food_label = Label(
                text=f"{food}: {details['cals']} kcal",
                size_hint_y=None,
                height=40
            )
            s = self.root.get_screen("SummaryScreen")
            ll = s.ids.log_layout
            ll.add_widget(food_label)

            nutrients_label = Label(
                text=f"Carbs: {details['carbs']}g | Fats: {details['fats']}g | Protein: {details['protein']}g",
                size_hint_y=None,
                height=40
            )
            ll.add_widget(nutrients_label)

            # Buttons for Edit and Delete
            edit_button = Button(text="Edit", size_hint_y=None, height=40)
            edit_button.bind(on_press=lambda instance, d=date, f=food: self.edit_food_entry(d, f))

            delete_button = Button(
                text="Delete (CAUTION)",
                size_hint_y=None,
                height=40,
                background_color=(1, 0, 0, 1)
            )
            delete_button.bind(on_press=lambda instance, d=date, f=food: self.delete_food_entry(d, f))

            # Add buttons in a horizontal layout
            button_layout = BoxLayout(size_hint_y=None, height=40)
            button_layout.add_widget(edit_button)
            button_layout.add_widget(delete_button)
            ll.add_widget(button_layout)

    def edit_food_entry(self, date, food_name):
        #Loads selected food entry into input fields for editing.
        if date in self.food_log and food_name in self.food_log[date]:
            entry = self.food_log[date][food_name] # JSON object
            mm = microMacros.get_running_app()
            s =  self.root.get_screen("logscreen")
            mm.root.current = "logscreen"

            # Prefill input fields with existing values
            print(s.ids)

            s.ids.foodname.text = food_name
            s.ids.cals.text = str(entry["cals"])
            s.ids.carbs.text = str(entry["carbs"])
            s.ids.fats.text = str(entry["fats"])
            s.ids.protein.text = str(entry["protein"])

            # Temporary store the food being edited
            self.editing_food = (date, food_name)

    def delete_food_entry(self, date, food_name):
        del self.food_log[date][food_name]
        json.dump(self.food_log,open('food_log.json','w'))
        self.update_displayed_log(date)
        # # Removes a food entry and updates the UI.
        # if date in self.food_log and food_name in self.food_log[date]:
        #     del self.food_log[date][food_name]

        #     # Remove the date entry if empty
        #     if not self.food_log[date]:
        #         del self.food_log[date]
            
        #     ls = microMacros.get_running_app().root.get_screen("logscreen")
        #     ls.save_food_log()  # Save the updated log

        #     # **Pass the current date to refresh the UI**
        #     self.update_displayed_log(date)

        # return build
        # # return self.window

    def on_start(self):
        # Call this after the UI is fully initialized
        self.update_displayed_log(self.current_date)

    def change_goals(self, instance):
        return

if __name__ == "__main__":
    microMacros().run()
