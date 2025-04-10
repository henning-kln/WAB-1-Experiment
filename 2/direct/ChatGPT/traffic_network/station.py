class Station:
    """Repräsentiert eine Station im Verkehrsnetz."""
    
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Station):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Station({self.name!r})"
