from kivy.garden.mapview import MapView
from kivy.app import App
from controlmarker import ControlMarker

class DefMapView(MapView):
    app = None
    map_marked = False
    controls = []

    # A function that runs once when the map is initialized
    def on_start(self):
        # Prevent from running more than once
        if self.map_marked: return
        self.map_marked = True
        # Defining properties based on the JSON file
        self.app = App.get_running_app()
        self.lat = self.app.activity_json["controls"][0]["lat"]
        self.lon = self.app.activity_json["controls"][0]["lon"]
        #Mark controls on map
        self.get_controls()

    # A function that runs when the zoom is changed
    def get_controls_on_zoom(self):
        # Minimum zoom
        if self.zoom < 15: self.zoom = 15
        # Removes old markers and replaces them with different sizes
        self.remove_controls()
        self.get_controls()

    # Get available controls from the JSON file
    def get_controls(self):  
        for control in self.app.activity_json["controls"]:
            self.add_cmarker(control)

    # Marks the control on the map
    def add_cmarker(self, control):
        marker = ControlMarker(lat=control["lat"], lon=control["lon"], anchor_y = 0.5, anchor_x = 0.5)
        # Chooses the symbol based on its type
        if control["type"] == "start": marker.source = "./markers/start_control_marker.png"
        if control["type"] == "finish": marker.source = "./markers/finish_control_marker.png"
        if control["type"] == "control":
            marker.source = f'./markers/{control["id"]}_control_marker.png'
        # Chooses the size based on zoom levels
        if self.zoom > 18:
            marker.size = [50/(0.018*self.zoom), 50/(0.018*self.zoom)]
        elif self.zoom < 16:
            marker.size = [20,20]
        else:
            marker.size = [40, 40]
        # Adds the marker object to a list to keep track for removal
        if not marker in self.controls: self.controls.append(marker)
        self.add_marker(marker)

    # Removes marker objects stored on a list
    def remove_controls(self):
        for marker in self.controls:
            self.remove_marker(marker)
        self.controls.clear()