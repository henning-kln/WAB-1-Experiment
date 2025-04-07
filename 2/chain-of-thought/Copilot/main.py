#Zu testen selber erstellt.
#Nicht generiert und nicht in die Bewertung einbezogen.

from netzwerk import Netzwerk as Network
from verbindung import Verbindung as Connection
from station import Station

def main() -> None:
    # Erzeugen des Netzwerks
    network = Network()
    
    # Erstellen einiger Stationen
    network.station_hinzufuegen("A")
    network.station_hinzufuegen("B")
    network.station_hinzufuegen("C")
    network.station_hinzufuegen("D")
    
    # Hinzufügen von Verbindungen zwischen den Stationen
    network.verbindung_hinzufuegen("A", "B", 5)
    network.verbindung_hinzufuegen("B", "C", 10)
    network.verbindung_hinzufuegen("A", "C", 15)
    network.verbindung_hinzufuegen("C", "D", 20)
    
    # Berechnung des kürzesten Pfads von Station A nach D
    result = network.shortest_path("A", "D")
    if result:
        path, duration = result
        print(f"Der kürzeste Pfad von A nach D hat eine Dauer von {duration} Minuten.")
        print("Pfad:", " -> ".join(station.name for station in path))
    else:
        print(f"Es wurde kein Pfad von A nach D gefunden.")

if __name__ == "__main__":
    main()
