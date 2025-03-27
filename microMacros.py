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
        try:
            with open('food_log.json', 'r') as file:
                food_log = json.load(file)
                total_cals = sum(food["cals"] for food in food_log[cd].values())
                total_carbs = sum(food["carbs"] for food in food_log[cd].values())
                total_fats = sum(food["fats"] for food in food_log[cd].values())
                total_protein = sum(food["protein"] for food in food_log[cd].values())
        except (FileNotFoundError, json.JSONDecodeError):
            total_cals = 0  # Default value if the file doesn't exist or is empty
            total_carbs = 0
            total_fats = 0 
            total_protein = 0
        except Exception:
            total_cals = 0  # Default value if the file doesn't exist or is empty
            total_carbs = 0
            total_fats = 0 
            total_protein = 0

        # Load nutrition_goals.json
        try:
            with open('nutrition_goals.json', 'r') as file:
                goals_data = json.load(file)
                calorie_goal = goals_data.get("calorie_goal", 0.0)
                carb_goal = goals_data.get("carb_goal", 0.0)
                fat_goal = goals_data.get("fat_goal", 0.0)
                protein_goal = goals_data.get("protein_goal", 0.0)
        except (FileNotFoundError, json.JSONDecodeError):
            calorie_goal = 0.0  # Default value if the file doesn't exist or is empty
            carb_goal = 0.0
            fat_goal = 0.0
            protein_goal = 0.0

        self.ids.greetings.markup = True

        def get_colored_text(total, goal):
            return f"[color=#AAAAFF]{total}[/color]" if total <= goal else f"[color=#FF4444]{total}[/color]"

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
        mm= microMacros.get_running_app()
        fl = mm.food_log
        if mm.current_date not in fl:
            fl[mm.current_date] = {}
        fl[mm.current_date][self.ids.foodname.text] = { # cannot add 2 foods of the same name on the same day - dict error
            "cals": float(self.ids.cals.text) if self.ids.cals.text else 0,
            "carbs": float(self.ids.carbs.text) if self.ids.carbs.text else 0,
            "fats": float(self.ids.fats.text) if self.ids.fats.text else 0,
            "protein": float(self.ids.protein.text) if self.ids.protein.text else 0,
        }
        
        self.ids.foodname.text = ""  
        self.ids.cals.text = ""      
        self.ids.carbs.text = ""     
        self.ids.fats.text = ""      
        self.ids.protein.text = ""   

        try:
            with open("food_log.json", "w") as file:
                json.dump(microMacros.get_running_app().food_log, file)
        except Exception as e:
            print(f"Error saving food log: {e}")
        mm.update_displayed_log(mm.current_date)

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
            carb_goal = float(self.ids.carb_goal.text) if self.ids.carb_goal.text else 0.0
            fat_goal = float(self.ids.fat_goal.text) if self.ids.fat_goal.text else 0.0
            protein_goal = float(self.ids.protein_goal.text) if self.ids.protein_goal.text else 0.0
            cal_goal = float(self.ids.calorie_goal.text) if self.ids.calorie_goal.text else 0.0
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
        for food, details in foods.items():
            # Food name and macronutrient info
            food_label = Label(
                text=f"{food}: {details['cals']} kcal",
                size_hint_y=None,
                height=40,
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
            edit_button = Button(text="Edit", size_hint_x = 0.75, size_hint_y=None, height=40)
            edit_button.bind(on_press=lambda instance, d=date, f=food: self.edit_food_entry(d, f))
            

            delete_button = Button(
                text="Delete",
                size_hint_x = 0.75,
                size_hint_y=None,
                height=40,
                background_color=(1, 0, 0, 1)
            )
            delete_button.bind(on_press=lambda instance, d=date, f=food: self.delete_food_entry(d, f))

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

            mm.root.transition = SlideTransition(direction='left')
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
        
        mm = microMacros.get_running_app()
        ss = mm.root.get_screen("SummaryScreen")
        ss.nutrition_comparison()

    def on_start(self):
        # Call this after the UI is fully initialized
        self.update_displayed_log(self.current_date)
        self.root.get_screen('SummaryScreen').nutrition_comparison()

if __name__ == "__main__":
    microMacros().run()