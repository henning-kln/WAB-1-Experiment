from traffic_network.station import Station

class Connection:
    """Verbindet zwei Stationen mit einer Reisedauer in Minuten."""
    
    def __init__(self, station1: Station, station2: Station, duration: int) -> None:
        self.station1 = station1
        self.station2 = station2
        self.duration = duration

    def __repr__(self) -> str:
        return (f"Connection({self.station1!r}, {self.station2!r}, "
                f"{self.duration} min)")
