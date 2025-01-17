from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton

KV = """
ScreenManager:
    HomeScreen:
    LogFoodScreen:

<HomeScreen>:
    name: 'home'

    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: "Nutrition Tracker"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "Welcome to the Nutrition Tracker!"
            halign: "center"
            font_style: "H5"

        MDRaisedButton:
            text: "Log Food"
            pos_hint: {"center_x": 0.5}
            on_release: app.change_screen('log_food')

        ScrollView:
            MDList:
                id: food_log_list

<LogFoodScreen>:
    name: 'log_food'

    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: "Log Food"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.change_screen('home')]]

        MDTextField:
            id: food_name
            hint_text: "Enter food name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}

        MDTextField:
            id: calories
            hint_text: "Enter calories"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            input_filter: "int"

        MDRaisedButton:
            text: "Add Food"
            pos_hint: {"center_x": 0.5}
            on_release: app.add_food()
"""

class HomeScreen(Screen):
    pass

class LogFoodScreen(Screen):
    pass

class NutritionTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.food_log = []  # Store logged food entries
        self.dialog = None
        return Builder.load_string(KV)

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def add_food(self):
        food_name = self.root.get_screen('log_food').ids.food_name.text
        calories = self.root.get_screen('log_food').ids.calories.text

        if not food_name or not calories:
            self.show_dialog("Error", "Please fill in all fields.")
            return

        # Add food to log
        self.food_log.append((food_name, calories))
        self.update_food_log()

        # Clear fields
        self.root.get_screen('log_food').ids.food_name.text = ""
        self.root.get_screen('log_food').ids.calories.text = ""

        self.show_dialog("Success", f"Added {food_name} with {calories} calories!")

    def update_food_log(self):
        food_log_list = self.root.get_screen('home').ids.food_log_list
        food_log_list.clear_widgets()

        for food_name, calories in self.food_log:
            food_log_list.add_widget(OneLineListItem(text=f"{food_name} - {calories} cal"))

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

if __name__ == "__main__":
    NutritionTrackerApp().run()
