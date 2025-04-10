"""
Modul: analyzer.py

Enthält die Funktion analyze_csv, die eine CSV-Datei einliest,
fehlerhafte Daten protokolliert und ignoriert und am Ende den
Durchschnitt des Alters und der Punkte berechnet.
"""

import csv
import logging


def analyze_csv(filename: str) -> None:
    """
    Liest die CSV-Datei mit den Spalten 'Name', 'Alter' und 'Punkte' ein.
    Fehlerhafte Datensätze (leere oder ungültige Felder) werden erkannt, 
    protokolliert und ignoriert. Am Ende werden der Durchschnittsalter 
    und der Durchschnitt der Punkte über alle gültigen Zeilen ausgegeben.

    :param filename: Pfad zur CSV-Datei.
    """
    # Logging konfigurieren: Warnungen werden ausgegeben.
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    total_age = 0
    total_points = 0
    valid_lines = 0

    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            row_number = 1  # Zählt die Header-Zeile als Zeile 1.
            for row in reader:
                row_number += 1
                try:
                    # Entferne führende/abschließende Leerzeichen.
                    age_str = row.get('Alter', '').strip()
                    points_str = row.get('Punkte', '').strip()

                    if age_str == '' or points_str == '':
                        raise ValueError("Leeres Feld gefunden")

                    # Versuche, die Werte in Integer zu konvertieren.
                    age = int(age_str)
                    points = int(points_str)

                except Exception as err:
                    logging.warning(f"Überspringe Zeile {row_number}: {err}")
                    continue

                total_age += age
                total_points += points
                valid_lines += 1

    except FileNotFoundError:
        logging.error(f"Datei '{filename}' wurde nicht gefunden.")
        return
    except Exception as err:
        logging.error(f"Ein Fehler beim Verarbeiten der Datei ist aufgetreten: {err}")
        return

    if valid_lines == 0:
        print("Keine gültigen Daten gefunden.")
        return

    avg_age = total_age / valid_lines
    avg_points = total_points / valid_lines

    print(f"Durchschnittsalter: {avg_age:.2f}")
    print(f"Durchschnitt der Punkte: {avg_points:.2f}")
