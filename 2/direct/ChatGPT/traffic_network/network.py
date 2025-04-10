from typing import Dict, List, Tuple, Optional
import heapq

from traffic_network.station import Station
from traffic_network.connection import Connection

class Network:
    """Modelliert ein Verkehrsnetz mit Stationen und Verbindungen."""
    
    def __init__(self) -> None:
        self.stations: set[Station] = set()
        self.connections: List[Connection] = []

    def add_station(self, station: Station) -> None:
        """Fügt eine Station dem Netzwerk hinzu."""
        self.stations.add(station)

    def add_connection(self, connection: Connection) -> None:
        """
        Fügt eine Verbindung dem Netzwerk hinzu.
        Dabei werden die beteiligten Stationen ebenfalls hinzugefügt.
        """
        self.add_station(connection.station1)
        self.add_station(connection.station2)
        self.connections.append(connection)

    def shortest_path(self, start: Station, end: Station) -> Optional[Tuple[int, List[Station]]]:
        """
        Berechnet mit dem Dijkstra-Algorithmus die kürzeste Reisedauer zwischen
        zwei Stationen. Gibt ein Tupel (Gesamtdauer, [Liste der Stationen im Pfad])
        zurück. Falls kein Pfad existiert, wird None zurückgegeben.
        """
        # Aufbau des Graphen als Adjazenzliste
        graph: Dict[Station, List[Tuple[Station, int]]] = {station: [] for station in self.stations}
        for connection in self.connections:
            # Da die Verbindung bidirektional ist, beide Richtungen hinzufügen
            graph[connection.station1].append((connection.station2, connection.duration))
            graph[connection.station2].append((connection.station1, connection.duration))

        # Initialisierung der Dijkstra-Datenstrukturen
        distances: Dict[Station, int] = {station: float('inf') for station in self.stations}
        previous: Dict[Station, Optional[Station]] = {station: None for station in self.stations}
        distances[start] = 0
        queue: List[Tuple[int, Station]] = [(0, start)]

        while queue:
            current_distance, current_station = heapq.heappop(queue)
            if current_station == end:
                break

            # Falls ein bereits besserer Weg gefunden wurde, diesen Eintrag überspringen
            if current_distance > distances[current_station]:
                continue

            for neighbor, duration in graph[current_station]:
                distance = current_distance + duration
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_station
                    heapq.heappush(queue, (distance, neighbor))

        # Kein erreichbarer Pfad
        if distances[end] == float('inf'):
            return None

        # Rekonstruktion des Pfads
        path: List[Station] = []
        current: Optional[Station] = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return distances[end], path
