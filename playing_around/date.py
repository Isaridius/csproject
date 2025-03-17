from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_sytle = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        return Builder.load_file('date.kv')

    #ok
    def on_save(self, instance, value, date_range):
        #print(instance, value, date_range)
        self.root.ids.date_label.text = str(value)

    #cancel
    def on_cancel(self, instance, value):
        self.root.ids.date_label.text = "Canceled"
        return

    def show_date_picker(self):
        date_dialogue = MDDatePicker()
        date_dialogue.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialogue.open()

MainApp().run()