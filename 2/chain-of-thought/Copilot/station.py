from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

# Vermeidung zirkulärer Importe
if TYPE_CHECKING:
    from verbindung import Verbindung

class Station:
    """Repräsentiert eine Station im Verkehrsnetz."""
    
    def __init__(self, name: str) -> None:
        """Initialisiert eine neue Station.
        
        Args:
            name: Der Name der Station
        """
        self.name = name
        self.verbindungen: List[Verbindung] = []
    
    def verbinde_mit(self, ziel_station: Station, fahrzeit: int) -> Verbindung:
        """Erstellt eine neue Verbindung zu einer anderen Station.
        
        Args:
            ziel_station: Die Zielstation
            fahrzeit: Die Fahrzeit in Minuten
            
        Returns:
            Die erstellte Verbindung
        """
        from verbindung import Verbindung
        verbindung = Verbindung(self, ziel_station, fahrzeit)
        self.verbindungen.append(verbindung)
        return verbindung
    
    def get_verbindungen(self) -> List[Verbindung]:
        """Gibt alle ausgehenden Verbindungen zurück.
        
        Returns:
            Liste aller ausgehenden Verbindungen
        """
        return self.verbindungen
    
    def __str__(self) -> str:
        """Gibt eine lesbare String-Darstellung zurück."""
        return f"Station: {self.name}"
    
    def __repr__(self) -> str:
        """Gibt eine eindeutige String-Darstellung zurück."""
        return f"Station('{self.name}')"