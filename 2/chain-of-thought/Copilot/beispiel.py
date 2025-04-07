"""Beispiel zur Nutzung des Verkehrsnetz-Modells."""

from netzwerk import Netzwerk

def main() -> None:
    """Beispielhafte Nutzung des Verkehrsnetz-Modells."""
    # Erstellen eines Verkehrsnetzes
    berlin_netz = Netzwerk("Berliner Verkehrsnetz")
    
    # Stationen hinzufügen
    for station in ["Hauptbahnhof", "Alexanderplatz", "Friedrichstraße", 
                    "Ostbahnhof", "Potsdamer Platz", "Zoologischer Garten"]:
        berlin_netz.station_hinzufuegen(station)
    
    # Verbindungen hinzufügen
    verbindungen = [
        ("Hauptbahnhof", "Alexanderplatz", 8),
        ("Hauptbahnhof", "Friedrichstraße", 5),
        ("Hauptbahnhof", "Zoologischer Garten", 7),
        ("Alexanderplatz", "Ostbahnhof", 6),
        ("Alexanderplatz", "Friedrichstraße", 4),
        ("Friedrichstraße", "Potsdamer Platz", 3),
        ("Potsdamer Platz", "Zoologischer Garten", 5),
        ("Zoologischer Garten", "Hauptbahnhof", 7)
    ]
    
    for start, ziel, zeit in verbindungen:
        berlin_netz.verbindung_hinzufuegen(start, ziel, zeit)
    
    # Netzwerkinformationen anzeigen
    print(berlin_netz)
    
    # Beispiel: Kürzesten Pfad berechnen
    start_station = "Alexanderplatz"
    ziel_station = "Zoologischer Garten"
    
    try:
        pfad, gesamtzeit = berlin_netz.shortest_path(start_station, ziel_station)
        
        print(f"\nKürzester Pfad von {start_station} nach {ziel_station}:")
        pfad_namen = [station.name for station in pfad]
        print(" → ".join(pfad_namen))
        print(f"Gesamtfahrzeit: {gesamtzeit} Minuten")
        
        # Details zu jeder Verbindung anzeigen
        print("\nDetails der Verbindungen:")
        for i in range(len(pfad) - 1):
            aktuelle = pfad[i]
            naechste = pfad[i + 1]
            
            # Verbindung finden
            verbindung = next(v for v in aktuelle.get_verbindungen() 
                              if v.ziel_station == naechste)
            
            print(f"{aktuelle.name} → {naechste.name}: {verbindung.fahrzeit} Minuten")
        
    except ValueError as e:
        print(f"Fehler: {e}")
    
    # Weitere Beispiele für verschiedene Routen
    print("\nWeitere Routenbeispiele:")
    route_beispiele = [
        ("Hauptbahnhof", "Ostbahnhof"),
        ("Zoologischer Garten", "Alexanderplatz"),
        ("Potsdamer Platz", "Hauptbahnhof")
    ]
    
    for start, ziel in route_beispiele:
        try:
            pfad, zeit = berlin_netz.shortest_path(start, ziel)
            stationen = " → ".join([s.name for s in pfad])
            print(f"Von {start} nach {ziel}: {stationen} ({zeit} Minuten)")
        except ValueError as e:
            print(f"Von {start} nach {ziel}: {e}")

if __name__ == "__main__":
    main()