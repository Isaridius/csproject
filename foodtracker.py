from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog

import cv2
import pytesseract
from kivy.clock import mainthread

import requests


print(pytesseract.get_tesseract_version())

class FoodTrackerApp(MDApp):
    def build(self):
        self.food_log = []  # List to store food entries
        self.custom_nutrients = []  # List to store custom nutrients

        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input for food name
        self.food_name_input = MDTextField(hint_text='Enter food name')
        self.layout.add_widget(self.food_name_input)

        # Input for calories (per serving)
        self.calories_per_serving_input = MDTextField(hint_text='Calories per serving', input_filter='int')
        self.layout.add_widget(self.calories_per_serving_input)

        # Input for protein (per serving)
        self.protein_per_serving_input = MDTextField(hint_text='Protein per serving (g)', input_filter='int')
        self.layout.add_widget(self.protein_per_serving_input)

        # Input for fats (per serving)
        self.fat_per_serving_input = MDTextField(hint_text='Fats per serving (g)', input_filter='int')
        self.layout.add_widget(self.fat_per_serving_input)

        # Input for carbs (per serving)
        self.carbs_per_serving_input = MDTextField(hint_text='Carbs per serving (g)', input_filter='int')
        self.layout.add_widget(self.carbs_per_serving_input)

        # Input for serving size
        self.serving_size_input = MDTextField(hint_text='Enter serving size (g)', input_filter='int')
        self.layout.add_widget(self.serving_size_input)

        # Input for amount eaten
        self.amount_eaten_input = MDTextField(hint_text='Enter amount eaten (g)', input_filter='int')
        self.layout.add_widget(self.amount_eaten_input)

        # Custom nutrient inputs
        self.custom_nutrient_name_input = MDTextField(hint_text='Nutrient name (e.g. Vitamin B)')
        self.layout.add_widget(self.custom_nutrient_name_input)

        self.custom_nutrient_value_input = MDTextField(hint_text='Nutrient value (e.g. 50 mg)')
        self.layout.add_widget(self.custom_nutrient_value_input)

        self.add_custom_nutrient_button = MDRaisedButton(text='Add Custom Nutrient', on_release=self.add_custom_nutrient)
        self.layout.add_widget(self.add_custom_nutrient_button)

        # Scrollable custom nutrient list
        self.scroll_view = MDScrollView()
        self.custom_nutrient_list = MDList()
        self.scroll_view.add_widget(self.custom_nutrient_list)
        self.layout.add_widget(self.scroll_view)

        # Button to add food
        self.add_button = MDRaisedButton(text='Add Food', on_release=self.add_food)
        self.layout.add_widget(self.add_button)

        # Label to display food log
        self.food_log_label = MDLabel(text='Food log will appear here.', halign='center', size_hint_y=None, height=100)
        self.layout.add_widget(self.food_log_label)

        # Button to scan barcodes
        self.scan_barcode_button = MDRaisedButton(text="Scan Barcode", on_release=self.scan_barcode)
        self.layout.add_widget(self.scan_barcode_button)


        return self.layout

    def add_food(self, instance):
        food_name = self.food_name_input.text
        calories_per_serving = self.calories_per_serving_input.text
        protein_per_serving = self.protein_per_serving_input.text
        fat_per_serving = self.fat_per_serving_input.text
        carbs_per_serving = self.carbs_per_serving_input.text
        serving_size = self.serving_size_input.text
        amount_eaten = self.amount_eaten_input.text

        if not food_name or not calories_per_serving or not protein_per_serving or not fat_per_serving or not carbs_per_serving or not serving_size or not amount_eaten:
            self.show_dialog('Error', 'Please fill in all fields!')
            return

        try:
            scaling_factor = int(amount_eaten) / int(serving_size)
            calories = int(calories_per_serving) * scaling_factor
            protein = int(protein_per_serving) * scaling_factor
            fat = int(fat_per_serving) * scaling_factor
            carbs = int(carbs_per_serving) * scaling_factor
        except ValueError:
            self.show_dialog('Error', 'Invalid input for nutrition facts, serving size, or amount eaten!')
            return

        custom_nutrients = '\n'.join(self.custom_nutrients)

        food_entry = f"{food_name} - {calories:.2f} cal\nProtein: {protein:.2f}g, Fats: {fat:.2f}g, Carbs: {carbs:.2f}g"
        if custom_nutrients:
            food_entry += f"\nCustom Nutrients:\n{custom_nutrients}"

        self.food_log.append(food_entry)
        self.update_food_log()

        # Clear inputs
        self.food_name_input.text = ''
        self.calories_per_serving_input.text = ''
        self.protein_per_serving_input.text = ''
        self.fat_per_serving_input.text = ''
        self.carbs_per_serving_input.text = ''
        self.serving_size_input.text = ''
        self.amount_eaten_input.text = ''
        self.custom_nutrient_name_input.text = ''
        self.custom_nutrient_value_input.text = ''

    def add_custom_nutrient(self, instance):
        nutrient_name = self.custom_nutrient_name_input.text
        nutrient_value = self.custom_nutrient_value_input.text

        if not nutrient_name or not nutrient_value:
            self.show_dialog('Error', 'Please fill in custom nutrient fields!')
            return

        nutrient_entry = f"{nutrient_name}: {nutrient_value}"
        self.custom_nutrients.append(nutrient_entry)

        self.custom_nutrient_list.add_widget(OneLineListItem(text=nutrient_entry))

        self.custom_nutrient_name_input.text = ''
        self.custom_nutrient_value_input.text = ''

    def update_food_log(self):
        self.food_log_label.text = '\n\n'.join(self.food_log)

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()

    def scan_barcode(self, instance):
        # Open a webcam video feed or an image file
        cap = cv2.VideoCapture(0)  # 0 is the default webcam
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Display the frame (optional for debugging)
            cv2.imshow("Barcode Scanner", frame)

            # Detect text using Tesseract OCR
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            barcode_text = pytesseract.image_to_string(gray, config="--psm 6")
            
            # If barcode detected, stop scanning
            if barcode_text.strip():
                cap.release()
                cv2.destroyAllWindows()
                self.lookup_nutrition(barcode_text.strip())
                break

            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def lookup_nutrition(self, barcode):
        # Use Nutritionix API to fetch nutritional information
        url = "https://trackapi.nutritionix.com/v2/search/item"
        headers = {
            "x-app-id": "192b5559",
            "x-app-key": "177e6ebe5ab4fbf84b2b9644b9efdb24",
        }
        params = {"upc": barcode}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            item = response.json().get("foods", [{}])[0]
            food_name = item.get("food_name", "Unknown Food")
            calories = item.get("nf_calories", 0)
            protein = item.get("nf_protein", 0)
            fat = item.get("nf_total_fat", 0)
            carbs = item.get("nf_total_carbohydrate", 0)

            self.food_name_input.text = food_name
            self.calories_per_serving_input.text = str(calories)
            self.protein_per_serving_input.text = str(protein)
            self.fat_per_serving_input.text = str(fat)
            self.carbs_per_serving_input.text = str(carbs)
        else:
            self.show_dialog("Error", "Failed to fetch nutrition data for this barcode.")

if __name__ == "__main__":
    FoodTrackerApp().run()
