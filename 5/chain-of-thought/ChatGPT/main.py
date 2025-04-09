import csv
import logging
from io import StringIO
from typing import Any, Dict, List, Optional, Union

# Logging konfigurieren: Warnungen werden ausgegeben.
logging.basicConfig(level=logging.WARNING,
                    format='%(levelname)s: %(message)s')


def safe_convert(value: str) -> Optional[Union[int, float, str]]:
    """
    Versucht, den Eingabestring in einen int oder float zu konvertieren.
    Ist der String leer oder "not available" (unabhängig von der Groß-/Kleinschreibung),
    wird None zurückgegeben.

    Args:
        value (str): Der zu konvertierende String.

    Returns:
        Optional[Union[int, float, str]]: Konvertierter numerischer Wert, der Originalstring
            (falls keine Konvertierung möglich war) oder None.
    """
    if value is None:
        return None
    value = value.strip()
    if value == "" or value.lower() == "not available":
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Liest eine CSV-Datei ein und verarbeitet jede Zeile.

    Für jede Zeile wird:
      - Jeder Wert mit safe_convert verarbeitet.
      - Die Zeile validiert: Das Feld "Name" darf nicht fehlen oder leer sein; Felder,
        die numerisch sein sollten (hier "Alter" und "Punkte"), müssen entweder None
        oder ein int/float sein.

    Fehlerhafte Zeilen werden protokolliert und übersprungen.

    Args:
        file_path (str): Pfad zur CSV-Datei.

    Returns:
        List[Dict[str, Any]]: Liste korrekt verarbeiteter Zeilen als Dictionaries.
    """
    results: List[Dict[str, Any]] = []
    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        # Die Kopfzeile entspricht Zeile 1
        line_number = 1
        for row in reader:
            line_number += 1
            try:
                processed_row = {key: safe_convert(value) for key, value in row.items()}

                # Validierung: "Name" darf nicht fehlen oder leer sein.
                if not processed_row.get("Name"):
                    logging.warning("Faulty row at line %d (missing Name): %s",
                                    line_number, row)
                    continue

                # Validierung: Numerische Felder ("Alter", "Punkte")
                faulty_row = False
                for field in ["Alter", "Punkte"]:
                    if field in processed_row:
                        field_value = processed_row[field]
                        if field_value is not None and not isinstance(field_value, (int, float)):
                            logging.warning("Faulty row at line %d (invalid %s format): %s",
                                            line_number, field, row)
                            faulty_row = True
                            break
                if faulty_row:
                    continue

                results.append(processed_row)
            except Exception as exc:
                logging.warning("Error processing row at line %d: %s. Error: %s",
                                line_number, row, exc)
                continue
    return results


def compute_average(data: List[Dict[str, Any]], field: str) -> Optional[float]:
    """
    Berechnet den Durchschnitt des angegebenen Feldes aus einer Liste von Zeilen.
    Es werden nur numerische Werte (int, float) berücksichtigt. Falls keine gültigen Werte
    vorliegen, wird None zurückgegeben.

    Args:
        data (List[Dict[str, Any]]): Liste der Zeilen als Dictionaries.
        field (str): Das Feld, für das der Durchschnitt berechnet werden soll.

    Returns:
        Optional[float]: Durchschnittswert oder None, wenn keine numerischen Werte vorhanden sind.
    """
    valid_values = [
        row[field]
        for row in data
        if row.get(field) is not None and isinstance(row[field], (int, float))
    ]
    if valid_values:
        return sum(valid_values) / len(valid_values)
    return None


def main() -> None:
    """
    Testfunktion, um die CSV-Verarbeitung und Durchschnittsberechnung zu demonstrieren.
    Verwendet Beispieldaten, bei denen fehlerhafte Zeilen protokolliert und übersprungen werden.
    """
    # Beispieldaten als mehrzeiliger String
    sample_data = (
        "Name,Alter,Punkte\n"
        "Alice,25,88\n"
        "Bob,,74\n"
        "Clara,31,not available\n"
        ",,\n"
        "David,abc,95\n"
    )

    # Simulation des Einlesens mittels StringIO
    sample_file = StringIO(sample_data)
    reader = csv.DictReader(sample_file)

    data: List[Dict[str, Any]] = []
    line_number = 1
    for row in reader:
        line_number += 1
        try:
            processed_row = {key: safe_convert(value) for key, value in row.items()}

            if not processed_row.get("Name"):
                logging.warning("Faulty row at line %d (missing Name): %s",
                                line_number, row)
                continue

            faulty_row = False
            for field in ["Alter", "Punkte"]:
                if field in processed_row:
                    field_value = processed_row[field]
                    if field_value is not None and not isinstance(field_value, (int, float)):
                        logging.warning("Faulty row at line %d (invalid %s format): %s",
                                        line_number, field, row)
                        faulty_row = True
                        break
            if faulty_row:
                continue

            data.append(processed_row)
        except Exception as exc:
            logging.warning("Error processing row at line %d: %s. Error: %s",
                            line_number, row, exc)
            continue

    print("Processed data:")
    for entry in data:
        print(entry)

    # Durchschnittsberechnungen für die Felder "Alter" und "Punkte"
    average_age = compute_average(data, "Alter")
    average_points = compute_average(data, "Punkte")

    print("\nCalculated averages:")
    print("Average age:", average_age)
    print("Average points:", average_points)


if __name__ == "__main__":
    main()
