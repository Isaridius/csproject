from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen


#Define screens

class SummaryScreen(Screen):
    pass


class LogScreen(Screen):

    pass


class GoalsScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass




# Designate Our .kv design file
build = Builder.load_file('screentest.kv')



class screenTest(App):
    def build(self):
        return build


    def change_date(self, instance):
        print("please work")
        pass



if __name__ == '__main__':
    screenTest().run()