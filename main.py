from kivymd.app import MDApp
from defmapview import DefMapView
import json

class MainApp(MDApp):
    with open("./controls.json", "r") as activity:
        activity_json = json.load(activity)
    def on_start(self):
        pass

MainApp().run()