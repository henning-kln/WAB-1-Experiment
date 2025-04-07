#Zu testen selber erstellt.
#Nicht generiert und nicht in die Bewertung einbezogen.

from chatgpt import Netzwerk as Network
from chatgpt import Verbindung as Connection
from chatgpt import Station

def main() -> None:
    # Erzeugen des Netzwerks
    network = Network()
    
    # Erstellen einiger Stationen
    s1 = Station("A")
    s2 = Station("B")
    s3 = Station("C")
    s4 = Station("D")
    network.add_station(s1)
    network.add_station(s2)
    network.add_station(s3)
    network.add_station(s4)
    
    # Hinzufügen von Verbindungen zwischen den Stationen
    c1 = Connection(s1, s2, 5)
    c2 = Connection(s2, s3, 10)
    c3 = Connection(s1, s3, 15)
    c4 = Connection(s3, s4, 20)
    network.add_verbindung(c1)
    network.add_verbindung(c2)
    network.add_verbindung(c3)
    network.add_verbindung(c4)
    
    
    # Berechnung des kürzesten Pfads von Station A nach D
    result = network.shortest_path(s1, s4)
    if result:
        path, duration = result
        print(f"Der kürzeste Pfad von A nach D hat eine Dauer von {duration} Minuten.")
        print("Pfad:", " -> ".join(station.name for station in path))
    else:
        print(f"Es wurde kein Pfad von A nach D gefunden.")

if __name__ == "__main__":
    main()
