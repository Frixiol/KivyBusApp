import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.screenmanager import NoTransition
import json


# ouverture des fichier json et creation d'un dict pour classer les données
json_rawbus = open("data.json")
json_rawstop = open("marker.json", encoding='utf-8')
data_bus = json.load(json_rawbus)
data_stop = json.load(json_rawstop)
Window.size = (270, 585)


# Une classe permettant l'affichage d'un écran
# qui affichera les information du bus selectionné
class MainScreen(Screen):


    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.information_bus = "Choisiser un bus pour plus d'information"
        self.fl = FloatLayout()
        with self.fl.canvas:
            Color(1, 1, 1, .8, mode='rgba')
            Rectangle(size=Window.size)
        self.button_menu = Button(height=40, width=40, size_hint=(None, None), pos=(20, 0), pos_hint={'top': 0.97})
        self.button_tr_info = Button(size_hint=(1/3, .1), pos=(0, 0), pos_hint={'top': 0.1}, text="Menu")
        self.button_tr_info.bind(on_press=self.pressMenu)
        self.button_tr_map = Button(size_hint=(1 / 3, .1), pos=(Window.size[0]/3, 0), pos_hint={'top': 0.1}, text="Map")
        self.button_tr_map.bind(on_press=self.pressMap)
        self.button_tr_bus = Button(size_hint=(1 / 3, .1), pos=(Window.size[0]/1.5, 0), pos_hint={'top': 0.1}, text="Bus")
        self.button_tr_bus.bind(on_press=self.pressBus)
        self.label_information = Label(font_size=15,text_size=(Window.size[0]-40, None), halign="left", size_hint=(None,None), height=36,
                                  width=Window.size[0]-40,pos=(20,0),pos_hint={"top":0.85},text=self.information_bus, color=(0,0,0,1))
        self.fl.add_widget(self.button_menu)
        self.fl.add_widget(self.button_tr_info)
        self.fl.add_widget(self.button_tr_map)
        self.fl.add_widget(self.button_tr_bus)
        self.fl.add_widget(self.label_information)
        self.add_widget(self.fl)

    def bus_choice(self, bus_taken):
        info = data_bus[bus_taken]
        self.information_bus = "Bus selectionné: " + bus_taken + "\nligne: " + info["ligne"] + "\nd'attente: " \
                               + info["attente"] + "\nNombre de passager: " + info["passager"]
        self.label_information.text = self.information_bus
        print(self.information_bus)
        busapp.mapscreen.addBusMarker(bus_taken)

    def pressMenu(self, *args):
        busapp.screenmanager.current = "Menu principal"

    def pressMap(self, *args):
        busapp.screenmanager.current = "Menu map"

    def pressBus(self, *args):
        busapp.screenmanager.current = "Menu bus"


# Une classe permettant l'affichage d'un écran
# qui affichera la carte avec lequelle des interaction seront possible
class MapScreen(Screen):

    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.fl = FloatLayout()
        with self.fl.canvas:
            Color(1, 1, 1, .8, mode='rgba')
            Rectangle(size=Window.size)

        self.mapview = MapView(zoom=13, lat=48.35, lon=-1.2, pos_hint={"top":0.9}, size_hint=(1, .7))
        for arret in data_stop:
            arret_marker = MapMarkerPopup(lat=data_stop[arret]["latitude"], lon=data_stop[arret]["longitude"], source="bus_stop.png")
            arret_marker.add_widget(Label(pos=(0, -30), text=data_stop[arret]["name"], color=(0, 0, 0, 1)))
            self.mapview.add_marker(arret_marker)
        self.mapview.remove_marker(arret_marker)
        self.button_menu = Button(height=40, width=40, size_hint=(None, None), pos=(20, 0), pos_hint={'top': 0.97})
        self.button_menu.bind(on_press=lambda x: self.get_coo())
        self.button_tr_info = Button(size_hint=(1 / 3, .1), pos=(0, 0), pos_hint={'top': 0.1}, text="Menu")
        self.button_tr_info.bind(on_press=self.pressMenu)
        self.button_tr_map = Button(size_hint=(1 / 3, .1), pos=(Window.size[0] / 3, 0), pos_hint={'top': 0.1}, text="Map")
        self.button_tr_map.bind(on_press=self.pressMap)
        self.button_tr_bus = Button(size_hint=(1 / 3, .1), pos=(Window.size[0] / 1.5, 0), pos_hint={'top': 0.1}, text="Bus")
        self.button_tr_bus.bind(on_press=self.pressBus)
        self.fl.add_widget(self.button_menu)
        self.fl.add_widget(self.button_tr_info)
        self.fl.add_widget(self.button_tr_map)
        self.fl.add_widget(self.button_tr_bus)

        self.fl.add_widget(self.mapview)
        self.add_widget(self.fl)

    def pressMenu(self, *args):
        busapp.screenmanager.current = "Menu principal"

    def pressMap(self, *args):
        busapp.screenmanager.current = "Menu map"

    def pressBus(self, *args):
        busapp.screenmanager.current = "Menu bus"

    def addBusMarker(self, bus_taken):
        info = data_bus[bus_taken]
        try:
            self.mapview.remove_marker(self.bus_marker)
        except:
            pass
        self.bus_marker = MapMarkerPopup(lat=info["latitude"], lon=info["longitude"], source="bus_marker2.png", size=(20, 20))

        self.bus_marker.add_widget(Label(pos=(0,-30), text=bus_taken, color=(0,0,0,1)))
        self.mapview.add_marker(self.bus_marker)

        self.mapview.get_latlon_at(Window.size[0]/2, Window.size[1]/2, zoom=None)

    def get_coo(self):
        print("oui")
        print(str(self.mapview.get_latlon_at(Window.size[0] / 2, Window.size[1] / 2, zoom=None)))


# Une classe permettant l'affichage d'un écran
# qui permettra à l'utilisateur de selectionné un bus
# pour lequel il veut connaitre les information
class BusScreen(Screen):
    def __init__(self, **kwargs):
        super(BusScreen, self).__init__(**kwargs)
        self.fl = FloatLayout()
        with self.fl.canvas:
            Color(1, 1, 1, .8, mode='rgba')
            Rectangle(size=Window.size)
        self.button_menu = Button(height=40, width=40, size_hint=(None, None), pos=(20, 0), pos_hint={'top': 0.97})
        self.button_tr_info = Button(size_hint=(1 / 3, .1), pos=(0, 0), pos_hint={'top': 0.1}, text="Menu")
        self.button_tr_info.bind(on_press=self.pressMenu)
        self.button_tr_map = Button(size_hint=(1 / 3, .1), pos=(Window.size[0] / 3, 0), pos_hint={'top': 0.1}, text="Map")
        self.button_tr_map.bind(on_press=self.pressMap)
        self.button_tr_bus = Button(size_hint=(1 / 3, .1), pos=(Window.size[0] / 1.5, 0), pos_hint={'top': 0.1}, text="Bus")
        self.button_tr_bus.bind(on_press=self.pressBus)
        self.button_bus1 = Button(size_hint=(.3, .1), pos=(20, 0), pos_hint={'top': 0.85}, text="Bus-1")
        self.button_bus1.bind(on_press=lambda x:busapp.mainscreen.bus_choice("Bus-1"))
        self.button_bus2 = Button(size_hint=(.3, .1), pos=(20, 0), pos_hint={'top': 0.75}, text="Bus-2")
        self.button_bus2.bind(on_press=lambda x:busapp.mainscreen.bus_choice("Bus-2"))
        self.fl.add_widget(self.button_menu)
        self.fl.add_widget(self.button_tr_info)
        self.fl.add_widget(self.button_tr_map)
        self.fl.add_widget(self.button_tr_bus)
        self.fl.add_widget(self.button_bus1)
        self.fl.add_widget(self.button_bus2)

        self.add_widget(self.fl)

    def pressMenu(self, *args):
        busapp.screenmanager.current = "Menu principal"

    def pressMap(self, *args):
        busapp.screenmanager.current = "Menu map"

    def pressBus(self, *args):
        busapp.screenmanager.current = "Menu bus"


# classe principale permettant de lancer l'application et de gerer chaque un des écran
class MyApp(App):
    def build(self):
        self.screenmanager = ScreenManager()
        self.screenmanager.transition = NoTransition()

        self.mainscreen = MainScreen(name="Menu principal")
        self.screenmanager.add_widget(self.mainscreen)

        self.mapscreen = MapScreen(name="Menu map")
        self.screenmanager.add_widget(self.mapscreen)

        self.busscreen = BusScreen(name="Menu bus")
        self.screenmanager.add_widget(self.busscreen)

        return self.screenmanager


# lancement de l'application
if __name__ == "__main__":
    busapp = MyApp()
    busapp.run()
