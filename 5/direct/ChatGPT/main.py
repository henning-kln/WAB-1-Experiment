"""
Modul: main.py

Ermöglicht den Aufruf der CSV-Analyse über die Kommandozeile.
"""

import sys
from analyzer import analyze_csv


def main() -> None:
    """
    Führt die CSV-Analyse aus. Es wird erwartet, dass der Pfad zur CSV-Datei 
    als Kommandozeilenparameter übergeben wird.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <csv_file>")
        sys.exit(1)

    filename = sys.argv[1]
    analyze_csv(filename)


if __name__ == '__main__':
    main()
