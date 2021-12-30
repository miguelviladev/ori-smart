from kivy.garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
from controlmarker import ControlMarker

class DefMapView(MapView):
    control_ids = []

    def start_getting_controls_in_fov(self):
        print(self.zoom)
        try:
            self.getting_controls_timer.cancel()
        except:
            pass
        self.getting_controls_timer = Clock.schedule_once(self.get_controls_in_fov, 0.1)
    
    def get_controls_in_fov(self, *args):
        app = App.get_running_app()
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        for control in app.activity_json["controls"]:
            if min_lat <= control["lat"] <= max_lat and min_lon <= control["lon"] <= max_lon:
                if not control["id"] in self.control_ids:
                    self.add_control_marker(control)
    def add_control_marker(self, control):
        lat, lon = control["lat"], control["lon"]
        control_marker = ControlMarker(lat=lat, lon=lon, source="./def_control_marker.png")
        self.add_marker(control_marker)
        #self.control_ids.append(control["id"])