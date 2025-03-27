#Imports libaries
import kivy
from kivy.app import App
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

target_height = Window.height  # Adjust as needed
target_width = int(target_height * (9 / 19.5))
Window.size = (target_width, target_height)

# Window.fullscreen = 'manual'

class SummaryScreen(Screen):
    def nutrition_comparison(self):
        mm = microMacros.get_running_app()
        cd = mm.current_date
        print("Starting comparison...")
        
        # Initialize total values to 0
        total_cals = total_carbs = total_fats = total_protein = 0

        try:
            # Read the food_log from the JSON file
            with open('food_log.json', 'r') as file:
                food_log = json.load(file)

                # Ensure the current date exists in the food log
                if cd in food_log:
                    # Sum up the values for the current date
                    for food in food_log[cd]:
                        total_cals += food.get("cals", 0)
                        total_carbs += food.get("carbs", 0)
                        total_fats += food.get("fats", 0)
                        total_protein += food.get("protein", 0)

        except (FileNotFoundError, json.JSONDecodeError):
            print("Food log file is missing or invalid.")
        
        # Load nutrition_goals.json
        try:
            with open('nutrition_goals.json', 'r') as file:
                goals_data = json.load(file)
                calorie_goal = goals_data.get("calorie_goal", 0)
                carb_goal = goals_data.get("carb_goal", 0)
                fat_goal = goals_data.get("fat_goal", 0)
                protein_goal = goals_data.get("protein_goal", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            calorie_goal = carb_goal = fat_goal = protein_goal = 0
            # i was lazy
        
        self.ids.greetings.markup = True

        # Function to return colored text based on comparison
        def get_colored_text(total, goal):
            return f"[color=#AAAAFF]{total}[/color]" if total <= goal else f"[color=#FF4444]{total}[/color]"

        # Set the greetings text with comparison
        self.ids.greetings.text = f'''
        kcals: {get_colored_text(total_cals, calorie_goal)}/{calorie_goal}kcal
        carbs: {get_colored_text(total_carbs, carb_goal)}/{carb_goal}g
        fats: {get_colored_text(total_fats, fat_goal)}/{fat_goal}g
        protein: {get_colored_text(total_protein, protein_goal)}/{protein_goal}g
        '''

    #Save the date
    def on_save(self, instance, value, date_range):
        mm =  microMacros.get_running_app()
        mm.current_date = str(value)
        self.ids.currentDate.text = mm.current_date
        mm.update_displayed_log(mm.current_date)

        self.nutrition_comparison()

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
        mm = microMacros.get_running_app()
        fl = mm.food_log

        # Initialize list for current date if not present
        if mm.current_date not in fl:
            fl[mm.current_date] = []

        food_name = self.ids.foodname.text
        try:
            calories = float(self.ids.cals.text) if self.ids.cals.text else 0.0
            carbs = float(self.ids.carbs.text) if self.ids.carbs.text else 0.0
            fats = float(self.ids.fats.text) if self.ids.fats.text else 0.0
            protein = float(self.ids.protein.text) if self.ids.protein.text else 0.0

            macronutrients = [calories, carbs, fats, protein]
            if any(value < 0 for value in macronutrients):
                print("Negative values are not allowed.")
                return
        except ValueError:
            print("Invalid input for macronutrients. Please enter valid numbers.")
            return

        if food_name:
            # Check if we're editing an existing food entry
            if hasattr(self, 'editing_food'):
                date, old_food_name = self.editing_food
                food_list = fl.get(date, [])

                for entry in food_list:
                    if entry["food_id"] == old_food_name:
                        entry["food_id"] = food_name  # Allow renaming
                        entry["cals"] = calories
                        entry["carbs"] = carbs
                        entry["fats"] = fats
                        entry["protein"] = protein
                        break  # Stop once edited
                
                # If the date changed, move entry
                if date != mm.current_date:
                    fl[mm.current_date].append(entry)
                    food_list.remove(entry)

                del self.editing_food  # Remove editing state
            else:
                # Create a new food entry if we're not editing
                food_entry = {
                    "food_id": food_name,
                    "cals": calories,
                    "carbs": carbs,
                    "fats": fats,
                    "protein": protein
                }
                fl[mm.current_date].append(food_entry)

            # Clear input fields
            self.ids.foodname.text = ""
            self.ids.cals.text = ""
            self.ids.carbs.text = ""
            self.ids.fats.text = ""
            self.ids.protein.text = ""

            # Save updated food log
            try:
                with open("food_log.json", "w") as file:
                    json.dump(mm.food_log, file)
            except Exception as e:
                print(f"Error saving food log: {e}")

            mm.update_displayed_log(mm.current_date)

            # Navigate back
            app = microMacros.get_running_app()
            app.root.current = "SummaryScreen"
            self.manager.transition.direction = "right"

class GoalsScreen(Screen):
    def on_enter(self):
        """ Load saved goals when the screen is entered """
        self.load_goals()

    def load_goals(self):
        try:
            with open("nutrition_goals.json", "r") as f:
                goals_data = json.load(f)
            
            # Populate text fields with loaded values
            self.ids.carb_goal.text = str(goals_data.get("carb_goal", ""))
            self.ids.fat_goal.text = str(goals_data.get("fat_goal", ""))
            self.ids.protein_goal.text = str(goals_data.get("protein_goal", ""))
            self.ids.calorie_goal.text = str(goals_data.get("calorie_goal", ""))
        
        except (FileNotFoundError, json.JSONDecodeError):
            print("No saved goals found or invalid JSON format.")

    def save_goals(self):
        app = App.get_running_app()
        
        try:
            carb_goal = int(self.ids.carb_goal.text) if self.ids.carb_goal.text else 0
            fat_goal = int(self.ids.fat_goal.text) if self.ids.fat_goal.text else 0
            protein_goal = int(self.ids.protein_goal.text) if self.ids.protein_goal.text else 0
            cal_goal = int(self.ids.calorie_goal.text) if self.ids.calorie_goal.text else 0
        except ValueError:
            carb_goal = 0
            fat_goal = 0
            protein_goal = 0
            cal_goal = 0
            print("Invalid input, setting goals to 0.0.")

        goals_data = {
            "carb_goal": carb_goal,
            "fat_goal": fat_goal,
            "protein_goal": protein_goal,
            "calorie_goal": cal_goal
        }

        with open("nutrition_goals.json", "w") as f:
            json.dump(goals_data, f)

        print("Goals saved successfully.")

    def on_save_button_pressed(self):
        self.save_goals()

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
    
    def load_food_log(self):
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
                self._add_food_entries(date, foods)
        else:  # Show data for all dates
            for log_date, foods in sorted(self.food_log.items(), reverse=True):
                self._add_date_header(log_date)
                self._add_daily_summary(foods)
                self._add_food_entries(log_date, foods)

    def _add_daily_summary(self, foods):
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
        for entry in foods:  # Loop directly over the list of food entries
            # Assuming each `entry` is a dictionary with 'food_id', 'cals', etc.
            food_name = entry['food_id']
            food_label = Label(
                text=f"{food_name}: {entry['cals']} kcal",
                size_hint_y=None,
                height=40,
            )
            s = self.root.get_screen("SummaryScreen")
            ll = s.ids.log_layout
            ll.add_widget(food_label)

            nutrients_label = Label(
                text=f"Carbs: {entry['carbs']}g | Fats: {entry['fats']}g | Protein: {entry['protein']}g",
                size_hint_y=None,
                height=40
            )
            ll.add_widget(nutrients_label)

            # Buttons for Edit and Delete
            edit_button = Button(text="Edit", size_hint_x = 0.75, size_hint_y=None, height=40)
            edit_button.bind(on_press=lambda instance, d=date, f=food_name: self.edit_food_entry(d, f))

            delete_button = Button(
                text="Delete",
                size_hint_x = 0.75,
                size_hint_y=None,
                height=40,
                background_color=(1, 0, 0, 1)
            )
            delete_button.bind(on_press=lambda instance, d=date, f=food_name: self.delete_food_entry(d, f))

            button_layout = BoxLayout(size_hint_y=None, height=40)
            button_layout.add_widget(edit_button)
            button_layout.add_widget(delete_button)
            ll.add_widget(button_layout)


    def edit_food_entry(self, date, food_name):
        # Find the food entry in the list for the given date
        food_list = self.food_log.get(date, [])
        for food_entry in food_list:
            if food_entry["food_id"] == food_name:
                entry = food_entry
                break
        else:
            return  # Exit if food not found

        s = self.root.get_screen("logscreen")

        self.root.transition = SlideTransition(direction='left')
        self.root.current = "logscreen"

        # Prefill input fields with existing values
        s.ids.foodname.text = food_name
        s.ids.cals.text = str(entry["cals"])
        s.ids.carbs.text = str(entry["carbs"])
        s.ids.fats.text = str(entry["fats"])
        s.ids.protein.text = str(entry["protein"])

        # Store editing state in LogScreen instead
        s.editing_food = (date, food_name)  
        app = microMacros.get_running_app()
        app.root.get_screen("SummaryScreen").nutrition_comparison()



    def delete_food_entry(self, date, food_name):
        food_list = self.food_log.get(date, [])
        
        # Find and remove the food entry from the list
        food_list = [entry for entry in food_list if entry["food_id"] != food_name]
        
        # Update the food log with the new list
        self.food_log[date] = food_list

        # Save the updated food log to the JSON file
        try:
            with open("food_log.json", "w") as file:
                json.dump(self.food_log, file)
        except Exception as e:
            print(f"Error saving food log: {e}")

        # Update the display
        self.update_displayed_log(date)
        app = microMacros.get_running_app()
        app.root.get_screen("SummaryScreen").nutrition_comparison()

    def on_start(self):
        # Call this after the UI is fully initialized
        self.update_displayed_log(self.current_date)
        self.root.get_screen('SummaryScreen').nutrition_comparison()

if __name__ == "__main__":
    microMacros().run()