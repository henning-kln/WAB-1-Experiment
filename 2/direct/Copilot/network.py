import heapq
from models import Station, Connection

class Network:
    """
    Repräsentiert ein Verkehrsnetz bestehend aus Stationen und Verbindungen.
    
    Attributes:
        stations (set): Menge aller Stationen im Netzwerk
        connections (list): Liste aller Verbindungen im Netzwerk
        graph (dict): Graphrepräsentation für die Routenberechnung
    """
    
    def __init__(self):
        """Initialisiert ein neues, leeres Verkehrsnetz."""
        self.stations = set()
        self.connections = []
        self.graph = {}  # Adjazenzliste: {station: [(nachbar, dauer), ...]}
        
    def add_station(self, station):
        """
        Fügt eine Station zum Netzwerk hinzu.
        
        Args:
            station (Station): Die hinzuzufügende Station
        """
        self.stations.add(station)
        if station not in self.graph:
            self.graph[station] = []
            
    def add_connection(self, connection):
        """
        Fügt eine Verbindung zum Netzwerk hinzu.
        
        Args:
            connection (Connection): Die hinzuzufügende Verbindung
        """
        # Stelle sicher, dass beide Stationen im Netzwerk sind
        self.add_station(connection.start)
        self.add_station(connection.end)
        
        # Füge die Verbindung zur Liste hinzu
        self.connections.append(connection)
        
        # Aktualisiere den Graphen (für bidirektionale Verbindungen)
        self.graph[connection.start].append((connection.end, connection.duration))
        
    def shortest_path(self, start, end):
        """
        Berechnet den kürzesten Weg zwischen zwei Stationen mittels Dijkstra-Algorithmus.
        
        Args:
            start (Station): Die Startstation
            end (Station): Die Zielstation
            
        Returns:
            tuple: (path, total_duration) wobei path eine Liste von Stationen ist
                  und total_duration die Gesamtdauer in Minuten
        
        Raises:
            ValueError: Wenn start oder end nicht im Netzwerk sind oder kein Weg existiert
        """
        if start not in self.stations:
            raise ValueError(f"Startstation '{start}' ist nicht im Netzwerk")
        if end not in self.stations:
            raise ValueError(f"Zielstation '{end}' ist nicht im Netzwerk")
        
        # Initialisiere die Distanzen mit unendlich
        distances = {station: float('infinity') for station in self.stations}
        distances[start] = 0
        
        # Initialisiere die Vorgänger für die Pfadrekonstruktion
        previous = {station: None for station in self.stations}
        
        # Prioritätswarteschlange für Dijkstra, enthält (distanz, station)
        priority_queue = [(0, start)]
        
        # Menge der bereits besuchten Stationen
        visited = set()
        
        while priority_queue:
            # Hole die Station mit der geringsten Distanz
            current_distance, current_station = heapq.heappop(priority_queue)
            
            # Wenn wir die Zielstation erreicht haben, können wir den Pfad rekonstruieren
            if current_station == end:
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    current = previous[current]
                path.reverse()  # Pfad von Start nach Ziel umdrehen
                return path, distances[end]
            
            # Keine Knoten mehrfach verarbeiten
            if current_station in visited:
                continue
            
            visited.add(current_station)
            
            # Untersuche alle Nachbarn des aktuellen Knotens
            for neighbor, weight in self.graph[current_station]:
                if neighbor in visited:
                    continue
                    
                # Berechne die neue Distanz
                distance = current_distance + weight
                
                # Wenn wir einen kürzeren Weg gefunden haben, aktualisiere die Werte
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_station
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Wenn wir hier ankommen, existiert kein Pfad
        raise ValueError(f"Es existiert kein Weg von '{start}' nach '{end}'")