from typing import List, Tuple, Optional, Dict
import heapq

class Station:
    """
    Repräsentiert eine Station im Verkehrsnetz.
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Station: {self.name}"

    def __repr__(self) -> str:
        return f"Station({self.name!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Station):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Verbindung:
    """
    Repräsentiert eine Verbindung zwischen zwei Stationen mit einer Fahrzeit in Minuten.
    """
    def __init__(self, station1: Station, station2: Station, fahrzeit: int) -> None:
        self.station1 = station1
        self.station2 = station2
        self.fahrzeit = fahrzeit

    def __str__(self) -> str:
        return (f"Verbindung: {self.station1.name} <-> {self.station2.name} "
                f"(Fahrzeit: {self.fahrzeit} Minuten)")

    def __repr__(self) -> str:
        return (f"Verbindung({self.station1!r}, {self.station2!r}, "
                f"{self.fahrzeit!r})")


class Netzwerk:
    """
    Enthält alle Stationen und Verbindungen des Verkehrsnetzes.
    Bietet Methoden zum Hinzufügen von Stationen/Verbindungen und zum Finden des kürzesten Weges.
    """
    def __init__(self) -> None:
        self.stations: List[Station] = []
        self.verbindungen: List[Verbindung] = []

    def add_station(self, station: Station) -> None:
        """Fügt eine Station zum Netzwerk hinzu."""
        self.stations.append(station)

    def add_verbindung(self, verbindung: Verbindung) -> None:
        """Fügt eine Verbindung zum Netzwerk hinzu."""
        self.verbindungen.append(verbindung)

    def shortest_path(self, start: Station, end: Station) -> Optional[Tuple[List[Station], int]]:
        """
        Findet den kürzesten Weg (nach Fahrzeit) von 'start' zu 'end' mithilfe von Dijkstras Algorithmus.
        
        :param start: Startstation
        :param end: Zielstation
        :return: Ein Tupel (Weg, Gesamtfahrzeit) oder None, falls kein Weg existiert.
        """
        # Aufbau des Graphen: Jede Station erhält eine Liste von (Nachbarstation, Fahrzeit)
        graph: Dict[Station, List[Tuple[Station, int]]] = {station: [] for station in self.stations}
        for verbindung in self.verbindungen:
            graph[verbindung.station1].append((verbindung.station2, verbindung.fahrzeit))
            graph[verbindung.station2].append((verbindung.station1, verbindung.fahrzeit))

        # Initialisiere Distanzen: Unendlich für alle Stationen, außer der Startstation
        distances: Dict[Station, int] = {station: float('inf') for station in self.stations}
        previous: Dict[Station, Optional[Station]] = {station: None for station in self.stations}
        distances[start] = 0

        # Priority Queue für Dijkstras Algorithmus
        queue: List[Tuple[int, Station]] = [(0, start)]
        while queue:
            current_distance, current_station = heapq.heappop(queue)
            if current_station == end:
                break  # Ziel erreicht
            if current_distance > distances[current_station]:
                continue  # Ein besserer Weg wurde bereits gefunden

            # Überprüfung der Nachbarn
            for neighbor, weight in graph[current_station]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_station
                    heapq.heappush(queue, (distance, neighbor))

        # Wenn das Ziel nicht erreichbar ist
        if distances[end] == float('inf'):
            return None

        # Rekonstruiere den Pfad vom Endpunkt zurück zum Start
        path: List[Station] = []
        current: Optional[Station] = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        return path, distances[end]

    def __str__(self) -> str:
        stations_str = "\n".join(f"  - {station.name}" for station in self.stations)
        verbindungen_str = "\n".join(f"  - {verbindung}" for verbindung in self.verbindungen)
        return f"Netzwerk:\nStations:\n{stations_str}\nVerbindungen:\n{verbindungen_str}"


def main() -> None:
    # Stationen erstellen
    station_a = Station("A")
    station_b = Station("B")
    station_c = Station("C")
    station_d = Station("D")

    # Verbindungen erstellen
    verbindung_ab = Verbindung(station_a, station_b, 10)
    verbindung_bc = Verbindung(station_b, station_c, 15)
    verbindung_ac = Verbindung(station_a, station_c, 30)
    verbindung_cd = Verbindung(station_c, station_d, 5)

    # Netzwerk erstellen und Elemente hinzufügen
    netz = Netzwerk()
    netz.add_station(station_a)
    netz.add_station(station_b)
    netz.add_station(station_c)
    netz.add_station(station_d)
    netz.add_verbindung(verbindung_ab)
    netz.add_verbindung(verbindung_bc)
    netz.add_verbindung(verbindung_ac)
    netz.add_verbindung(verbindung_cd)

    # Ausgabe des Netzwerks
    print(netz)
    print()

    # Kürzester Weg von Station A nach Station D ermitteln
    result = netz.shortest_path(station_a, station_d)
    if result is None:
        print("Kein Weg gefunden.")
    else:
        path, total_time = result
        path_str = " -> ".join(station.name for station in path)
        print("Kürzester Weg von A nach D:")
        print(path_str)
        print("Gesamtfahrzeit:", total_time, "Minuten")


if __name__ == "__main__":
    main()
