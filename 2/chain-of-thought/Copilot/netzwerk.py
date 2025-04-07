from __future__ import annotations
from typing import Dict, List, Tuple, Union, Optional
import heapq

from station import Station
from verbindung import Verbindung

class Netzwerk:
    """Repräsentiert ein Verkehrsnetz mit Stationen und Verbindungen."""
    
    def __init__(self, name: str = "Verkehrsnetz") -> None:
        """Initialisiert ein neues Verkehrsnetz.
        
        Args:
            name: Der Name des Verkehrsnetzes
        """
        self.name = name
        self.stationen: Dict[str, Station] = {}
        self.verbindungen: List[Verbindung] = []
    
    def station_hinzufuegen(self, name: str) -> Station:
        """Fügt eine neue Station zum Netzwerk hinzu.
        
        Args:
            name: Der Name der Station
            
        Returns:
            Die erstellte oder bereits existierende Station
        """
        if name not in self.stationen:
            station = Station(name)
            self.stationen[name] = station
            return station
        return self.stationen[name]
    
    def verbindung_hinzufuegen(self, start_name: str, ziel_name: str, fahrzeit: int) -> Verbindung:
        """Fügt eine neue Verbindung zwischen zwei Stationen hinzu.
        
        Args:
            start_name: Name der Ausgangsstation
            ziel_name: Name der Zielstation
            fahrzeit: Fahrzeit in Minuten
            
        Returns:
            Die erstellte Verbindung
            
        Raises:
            ValueError: Wenn eine der Stationen nicht existiert
        """
        if start_name not in self.stationen:
            raise ValueError(f"Startstation '{start_name}' existiert nicht im Netzwerk")
        if ziel_name not in self.stationen:
            raise ValueError(f"Zielstation '{ziel_name}' existiert nicht im Netzwerk")
            
        start_station = self.stationen[start_name]
        ziel_station = self.stationen[ziel_name]
        
        verbindung = start_station.verbinde_mit(ziel_station, fahrzeit)
        self.verbindungen.append(verbindung)
        
        return verbindung
    
    def get_station(self, name: str) -> Optional[Station]:
        """Gibt eine Station anhand ihres Namens zurück.
        
        Args:
            name: Name der gesuchten Station
            
        Returns:
            Die gefundene Station oder None
        """
        return self.stationen.get(name)
    
    def get_alle_stationen(self) -> List[Station]:
        """Gibt alle Stationen im Netzwerk zurück.
        
        Returns:
            Liste aller Station-Objekte
        """
        return list(self.stationen.values())
    
    def get_alle_verbindungen(self) -> List[Verbindung]:
        """Gibt alle Verbindungen im Netzwerk zurück.
        
        Returns:
            Liste aller Verbindungs-Objekte
        """
        return self.verbindungen
    
    def shortest_path(self, start: Union[str, Station], end: Union[str, Station]) -> Tuple[List[Station], int]:
        """Berechnet den kürzesten Pfad zwischen zwei Stationen.
        
        Implementiert den Dijkstra-Algorithmus zur Pfadsuche basierend auf
        der Fahrzeit als Gewicht.
        
        Args:
            start: Startstation (Name oder Station-Objekt)
            end: Zielstation (Name oder Station-Objekt)
            
        Returns:
            Tuple mit der Liste der Stationen auf dem kürzesten Pfad 
            und der Gesamtfahrzeit in Minuten
                
        Raises:
            ValueError: Wenn Start-/Zielstation nicht existiert oder kein Pfad existiert
        """
        # Eingabeparameter in Station-Objekte umwandeln
        start_station = self._get_station_object(start)
        end_station = self._get_station_object(end)
        
        # Initialisierung für Dijkstra-Algorithmus
        unbesuchte_stationen = []
        distanzen = {station: float('infinity') for station in self.get_alle_stationen()}
        vorgaenger = {station: None for station in self.get_alle_stationen()}
        
        # Startdistanz auf 0 setzen
        distanzen[start_station] = 0
        heapq.heappush(unbesuchte_stationen, (0, start_station))
        
        while unbesuchte_stationen:
            # Station mit kleinster Distanz auswählen
            aktuelle_distanz, aktuelle_station = heapq.heappop(unbesuchte_stationen)
            
            # Wenn die Zielstation erreicht wurde, ist der kürzeste Pfad gefunden
            if aktuelle_station == end_station:
                break
            
            # Wenn die aktuelle Distanz größer ist als die bekannte, überspringen
            if aktuelle_distanz > distanzen[aktuelle_station]:
                continue
            
            # Alle Nachbarstationen überprüfen
            for verbindung in aktuelle_station.get_verbindungen():
                nachbar = verbindung.ziel_station
                distanz = aktuelle_distanz + verbindung.fahrzeit
                
                # Wenn ein kürzerer Weg gefunden wurde, aktualisieren
                if distanz < distanzen[nachbar]:
                    distanzen[nachbar] = distanz
                    vorgaenger[nachbar] = aktuelle_station
                    heapq.heappush(unbesuchte_stationen, (distanz, nachbar))
        
        # Wenn kein Pfad gefunden wurde
        if distanzen[end_station] == float('infinity'):
            raise ValueError(f"Es existiert kein Pfad zwischen {start_station.name} und {end_station.name}")
        
        # Pfad rekonstruieren
        pfad = []
        station = end_station
        while station:
            pfad.append(station)
            station = vorgaenger[station]
        
        pfad.reverse()  # Von Start zu Ziel umkehren
        
        return pfad, distanzen[end_station]
    
    def _get_station_object(self, station: Union[str, Station]) -> Station:
        """Hilfsmethod zum Umwandeln von Stationsnamen in Station-Objekte.
        
        Args:
            station: Stationsname oder Station-Objekt
            
        Returns:
            Das Station-Objekt
            
        Raises:
            ValueError: Wenn die Station nicht existiert
        """
        if isinstance(station, str):
            station_obj = self.get_station(station)
            if not station_obj:
                raise ValueError(f"Station '{station}' existiert nicht im Netzwerk")
            return station_obj
        return station
    
    def __str__(self) -> str:
        """Gibt eine lesbare String-Darstellung zurück."""
        return (f"{self.name} mit {len(self.stationen)} Stationen "
                f"und {len(self.verbindungen)} Verbindungen")