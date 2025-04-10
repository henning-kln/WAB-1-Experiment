from traffic_network.station import Station
from traffic_network.connection import Connection
from traffic_network.network import Network

def main() -> None:
    # Erzeugen des Netzwerks
    network = Network()
    
    # Erstellen einiger Stationen
    station_a = Station("A")
    station_b = Station("B")
    station_c = Station("C")
    station_d = Station("D")
    
    # Hinzufügen von Verbindungen zwischen den Stationen
    network.add_connection(Connection(station_a, station_b, 5))
    network.add_connection(Connection(station_b, station_c, 10))
    network.add_connection(Connection(station_a, station_c, 15))
    network.add_connection(Connection(station_c, station_d, 20))
    
    # Berechnung des kürzesten Pfads von Station A nach D
    result = network.shortest_path(station_a, station_d)
    if result:
        duration, path = result
        print(f"Der kürzeste Pfad von {station_a.name} nach {station_d.name} hat eine Dauer von {duration} Minuten.")
        print("Pfad:", " -> ".join(station.name for station in path))
    else:
        print(f"Es wurde kein Pfad von {station_a.name} nach {station_d.name} gefunden.")

if __name__ == "__main__":
    main()
