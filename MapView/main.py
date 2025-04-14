import asyncio
import os
import csv
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer
from datasource import Datasource


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapview = None
        self.datasource = Datasource(user_id=1)
        self.line_layer = LineMapLayer(color=[0, 0.6, 0.9, 1], width=2)
        self.car_marker = None

        base_dir = os.path.dirname(__file__)
        image_path = lambda name: os.path.join(base_dir, "images", name)
        self.car_icon = image_path("car.png")
        self.pothole_icon = image_path("pothole.png")
        self.bump_icon = image_path("bump.png")

    def load_from_csv(self, filename="data.csv"):
        try:
            with open(filename, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        lat = float(row["y"])
                        lon = float(row["x"])
                        point = (lat, lon)

                        self.line_layer.add_point(point)
                        self.set_generic_marker(point)  # Для прикладу позначимо "невідомий" стан
                    except (ValueError, KeyError):
                        continue
            print("CSV loaded successfully.")
        except FileNotFoundError:
            print(f"CSV файл {filename} не знайдено.")

    def set_generic_marker(self, point):
        lat, lon = point
        marker = MapMarker(lat=lat, lon=lon, source=self.bump_icon)  # або можна зробити окремий значок
        self.mapview.add_marker(marker)

    def build(self):
        self.mapview = MapView(zoom=15, lat=50.4501, lon=30.5234)
        self.mapview.add_layer(self.line_layer, mode="scatter")
        return self.mapview

    def on_start(self):
        self.load_from_csv()
        Clock.schedule_interval(self.update, 2) 

    def update(self, *args):
        new_points = self.datasource.get_new_points()
        for lat, lon, road_state in new_points:
            self.line_layer.add_point((lat, lon))
            self.update_car_marker((lat, lon))

            if road_state == "hole":
                self.set_pothole_marker((lat, lon))
            elif road_state == "bump":
                self.set_bump_marker((lat, lon))

    def update_car_marker(self, point):
        lat, lon = point
        if self.car_marker is None:
            self.car_marker = MapMarker(lat=lat, lon=lon, source=self.car_icon)
            self.mapview.add_marker(self.car_marker)
        else:
            self.car_marker.lat = lat
            self.car_marker.lon = lon

    def set_pothole_marker(self, point):
        lat, lon = point
        marker = MapMarker(lat=lat, lon=lon, source=self.pothole_icon)
        self.mapview.add_marker(marker)

    def set_bump_marker(self, point):
        lat, lon = point
        marker = MapMarker(lat=lat, lon=lon, source=self.bump_icon)
        self.mapview.add_marker(marker)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
