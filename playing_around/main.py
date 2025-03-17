from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


# Step 2: Define Stats Screen
class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.stats_label = Label(text="Stats: Total Calories: 0")
        self.layout.add_widget(self.stats_label)

        self.go_to_log_button = Button(text="Go to Log Page")
        self.go_to_log_button.bind(on_press=self.go_to_log_screen)
        self.layout.add_widget(self.go_to_log_button)

        self.add_widget(self.layout)

    def go_to_log_screen(self, instance):
        self.manager.current = "log"

    def update_stats(self, total_calories):
        self.stats_label.text = f"Stats: Total Calories: {total_calories}"


# Step 3: Define Log Screen
class LogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.food_name_input = TextInput(hint_text="Enter Food Name")
        self.calories_input = TextInput(hint_text="Enter Calories")
        self.layout.add_widget(self.food_name_input)
        self.layout.add_widget(self.calories_input)

        self.save_button = Button(text="Save Food and Go Back")
        self.save_button.bind(on_press=self.save_food_data)
        self.layout.add_widget(self.save_button)

        self.add_widget(self.layout)

    def save_food_data(self, instance):
        food_name = self.food_name_input.text
        try:
            calories = int(self.calories_input.text)
        except ValueError:
            calories = 0

        # Save the data and update the stats
        app = App.get_running_app()
        app.logged_foods.append((food_name, calories))
        app.update_stats()

        # Clear input fields
        self.food_name_input.text = ""
        self.calories_input.text = ""

        # Go back to the stats screen
        self.manager.current = "stats"


# Step 4: Set up the App
class MicroMacrosApp(App):
    def build(self):
        # Step 5: Set up ScreenManager
        self.screen_manager = ScreenManager()

        # Add screens to ScreenManager
        self.stats_screen = StatsScreen(name="stats")
        self.log_screen = LogScreen(name="log")
        self.screen_manager.add_widget(self.stats_screen)
        self.screen_manager.add_widget(self.log_screen)

        # Initialize the logged foods list and update the stats
        self.logged_foods = []
        self.update_stats()

        return self.screen_manager

    def update_stats(self):
        total_calories = sum(calories for _, calories in self.logged_foods)
        self.stats_screen.update_stats(total_calories)


if __name__ == "__main__":
    MicroMacrosApp().run()
