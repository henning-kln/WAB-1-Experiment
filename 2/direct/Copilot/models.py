class Station:
    """
    Repräsentiert eine Station im Verkehrsnetz.
    
    Attributes:
        name (str): Der Name der Station
    """
    
    def __init__(self, name):
        """
        Initialisiert eine neue Station.
        
        Args:
            name (str): Name der Station
        """
        self.name = name
        
    def __eq__(self, other):
        """Vergleicht zwei Stationen anhand ihres Namens."""
        if not isinstance(other, Station):
            return False
        return self.name == other.name
    
    def __hash__(self):
        """Erzeugt einen Hash-Wert basierend auf dem Namen der Station."""
        return hash(self.name)
    
    def __str__(self):
        """Liefert eine lesbare String-Darstellung."""
        return self.name
    
    def __repr__(self):
        """Liefert eine eindeutige String-Repräsentation."""
        return f"Station('{self.name}')"


class Connection:
    """
    Repräsentiert eine Verbindung zwischen zwei Stationen.
    
    Attributes:
        start (Station): Die Startstation
        end (Station): Die Zielstation
        duration (int): Die Dauer der Verbindung in Minuten
    """
    
    def __init__(self, start, end, duration):
        """
        Initialisiert eine neue Verbindung.
        
        Args:
            start (Station): Die Startstation
            end (Station): Die Zielstation
            duration (int): Die Dauer der Verbindung in Minuten
        """
        self.start = start
        self.end = end
        self.duration = duration
        
    def __str__(self):
        """Liefert eine lesbare String-Darstellung."""
        return f"{self.start} -> {self.end} ({self.duration} min)"
    
    def __repr__(self):
        """Liefert eine eindeutige String-Repräsentation."""
        return f"Connection({repr(self.start)}, {repr(self.end)}, {self.duration})"