from kivy.garden.mapview import MapView
from kivy.app import App
from controlmarker import ControlMarker

class DefMapView(MapView):
    map_marked = False
    controls = []

    def get_controls_on_lat(self):
        if self.map_marked: return
        self.get_controls()

    def get_controls_on_zoom(self):
        print(self.zoom)
        if self.zoom < 15: self.zoom = 15
        self.remove_controls()
        self.get_controls()

    def get_controls(self):
        app = App.get_running_app()
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        for control in app.activity_json["controls"]:
            self.add_cmarker(control)
        self.map_marked = True

    def add_cmarker(self, control):
        marker = ControlMarker(lat=control["lat"], lon=control["lon"], anchor_y = 0.5, anchor_x = 0.5)
        if control["type"] == "start": marker.source = "./start_control_marker.png"
        if control["type"] == "finish": marker.source = "./finish_control_marker.png"
        if control["type"] == "control": marker.source = "./def_control_marker.png"
        marker.id = control["id"]
        if self.zoom > 18:
            marker.size = [50/(0.018*self.zoom), 50/(0.018*self.zoom)]
        elif self.zoom < 16:
            marker.size = [30,30]
        else:
            marker.size = [50, 50]
        if not marker in self.controls: self.controls.append(marker)
        self.add_marker(marker)

    def remove_controls(self):
        for marker in self.controls:
            self.remove_marker(marker)
        self.controls.clear()