import csv
from typing import Tuple
from logger import log_error

def analyze_csv(filename: str) -> Tuple[float, float]:
    total_age = 0
    total_points = 0
    valid_rows = 0

    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                age = int(row['Alter'])
                points = int(row['Punkte'])
                total_age += age
                total_points += points
                valid_rows += 1
            except ValueError as e:
                log_error(f"Fehlerhafte Daten in Zeile {csv_reader.line_num}: {row} - {e}")

    if valid_rows == 0:
        return 0.0, 0.0

    average_age = total_age / valid_rows
    average_points = total_points / valid_rows

    return average_age, average_points