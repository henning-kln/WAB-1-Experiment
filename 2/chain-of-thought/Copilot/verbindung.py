from __future__ import annotations
from typing import TYPE_CHECKING

# Vermeidung zirkulärer Importe
if TYPE_CHECKING:
    from station import Station

class Verbindung:
    """Repräsentiert eine Verbindung zwischen zwei Stationen im Verkehrsnetz."""
    
    def __init__(self, start_station: Station, ziel_station: Station, fahrzeit: int) -> None:
        """Initialisiert eine neue Verbindung.
        
        Args:
            start_station: Die Ausgangsstation
            ziel_station: Die Zielstation
            fahrzeit: Die Fahrzeit in Minuten
        
        Raises:
            ValueError: Wenn die Fahrzeit negativ ist
        """
        if fahrzeit < 0:
            raise ValueError("Fahrzeit darf nicht negativ sein")
            
        self.start_station = start_station
        self.ziel_station = ziel_station
        self.fahrzeit = fahrzeit
    
    def __str__(self) -> str:
        """Gibt eine lesbare String-Darstellung zurück."""
        return (f"Verbindung von {self.start_station.name} nach "
                f"{self.ziel_station.name} ({self.fahrzeit} Minuten)")
    
    def __repr__(self) -> str:
        """Gibt eine eindeutige String-Darstellung zurück."""
        return (f"Verbindung({self.start_station!r}, "
                f"{self.ziel_station!r}, {self.fahrzeit})")