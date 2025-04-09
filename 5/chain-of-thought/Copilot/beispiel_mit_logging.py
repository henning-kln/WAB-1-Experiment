"""
Beispiel für die Verwendung des CSV-Analyzers.

Dieses Skript demonstriert, wie der CSV-Analyzer mit und ohne Pandas verwendet wird,
um Durchschnittswerte aus einer CSV-Datei zu berechnen und gleichzeitig Fehler
zu protokollieren.
"""

import csv_analyzer
from datetime import datetime


def main():
    """
    Hauptfunktion, die die CSV-Analyse-Funktionen demonstriert.
    """
    # Aktueller Benutzer und Datum
    current_user = "henning-kln"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Ausführung am: {current_date}")
    print(f"Benutzer: {current_user}")

    # Datei mit Beispieldaten (inklusive fehlerhafter Zeilen)
    file_path = 'daten_mit_fehlern.csv'

    try:
        # Mit Pandas (empfohlen)
        print("--- Berechnung mit Pandas ---")
        avg_age, avg_score = csv_analyzer.calculate_averages(
            file_path, 
            username=current_user
        )
        print(f"Durchschnittsalter: {avg_age:.2f} Jahre")
        print(f"Durchschnittspunktzahl: {avg_score:.2f} Punkte")

        # Ohne Pandas
        print("\n--- Berechnung ohne Pandas ---")
        avg_age, avg_score = csv_analyzer.calculate_averages_without_pandas(
            file_path, 
            username=current_user
        )
        print(f"Durchschnittsalter: {avg_age:.2f} Jahre")
        print(f"Durchschnittspunktzahl: {avg_score:.2f} Punkte")

    except Exception as e:
        print(f"Fehler bei der Analyse: {e}")
        print("Details wurden in die Log-Datei geschrieben.")


if __name__ == "__main__":
    main()