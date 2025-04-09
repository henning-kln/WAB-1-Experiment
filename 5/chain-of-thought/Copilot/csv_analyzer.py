"""
CSV Analyzer Modul.

Dieses Modul stellt Funktionen zum Einlesen und Analysieren von CSV-Dateien bereit.
Es bietet Implementierungen mit und ohne Pandas sowie Funktionen zur Berechnung
von Durchschnittswerten mit robuster Fehlerbehandlung und Protokollierung.
"""

import csv
import logging
from typing import Dict, List, Optional, Tuple, Any, Union

import pandas as pd


def setup_logging(log_file: str = "csv_processing.log") -> None:
    """
    Richtet das Logging-System ein.
    
    Args:
        log_file: Pfad zur Log-Datei. Standard ist "csv_processing.log".
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def log_message(
    level: str,
    message: str,
    row_data: Optional[Any] = None,
    username: Optional[str] = None
) -> None:
    """
    Protokolliert eine Nachricht mit optionalen Benutzerinformationen.
    
    Args:
        level: Logging-Level ('info', 'warning', 'error')
        message: Die zu protokollierende Nachricht
        row_data: Optionale Daten der Zeile für Fehlerberichte
        username: Optionaler Benutzername für die Nachverfolgung
    """
    user_info = f" (Benutzer: {username})" if username else ""
    full_message = f"{message}{user_info}"
    
    if row_data:
        full_message += f". Daten: {row_data}"
    
    if level.lower() == 'info':
        logging.info(full_message)
    elif level.lower() == 'warning':
        logging.warning(full_message)
    elif level.lower() == 'error':
        logging.error(full_message)


def read_csv_file(
    file_path: str,
    delimiter: str = ',',
    handle_missing: bool = True,
    convert_numbers: bool = True,
    username: Optional[str] = None
) -> pd.DataFrame:
    """
    Liest eine CSV-Datei ein und gibt die Daten als Pandas DataFrame zurück.
    Fehlerhafte Zeilen werden protokolliert und ignoriert.
    
    Args:
        file_path: Pfad zur CSV-Datei
        delimiter: Trennzeichen der CSV-Datei. Standard ist ','
        handle_missing: Wenn True, werden leere Felder als None behandelt
        convert_numbers: Wenn True, werden numerische Strings in Zahlen konvertiert
        username: Optionaler Benutzername für das Logging
    
    Returns:
        DataFrame mit den Daten aus der CSV-Datei
        
    Raises:
        ValueError: Wenn die Datei leer ist oder keinen Header hat
        FileNotFoundError: Wenn die Datei nicht gefunden wird
    """
    setup_logging()
    log_message('info', f"Starte Einlesen der CSV-Datei: {file_path}", username=username)
    
    try:
        # Zuerst als Liste einlesen, um Zeilen-für-Zeile zu validieren
        valid_rows = []
        error_count = 0
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Lese die CSV-Datei
            reader = csv.reader(csvfile, delimiter=delimiter)
            
            try:
                # Header lesen
                header = next(reader)
                header = [h.strip() for h in header]  # Leerzeichen entfernen
                valid_rows.append(header)
            except StopIteration:
                error_msg = "CSV-Datei ist leer oder hat keinen Header"
                log_message('error', error_msg, username=username)
                raise ValueError(error_msg)
            
            # Zeilen lesen und validieren
            for row_idx, row in enumerate(reader, start=2):
                try:
                    # Prüfen, ob die Anzahl der Spalten mit dem Header übereinstimmt
                    if len(row) != len(header):
                        error_msg = (
                            f"Spaltenanzahl stimmt nicht mit Header überein "
                            f"(Header: {len(header)}, Zeile: {len(row)})"
                        )
                        raise ValueError(error_msg)
                    
                    # Zeile hinzufügen, wenn keine Fehler erkannt wurden
                    valid_rows.append(row)
                except Exception as e:
                    error_count += 1
                    log_message(
                        'error',
                        f"Fehler in Zeile {row_idx}: {str(e)}",
                        row_data=row,
                        username=username
                    )
        
        if error_count > 0:
            log_message(
                'warning',
                f"{error_count} fehlerhafte Zeilen wurden ignoriert",
                username=username
            )
        
        # Aus den validierten Zeilen ein DataFrame erstellen
        df = pd.DataFrame(valid_rows[1:], columns=valid_rows[0])
        
        if handle_missing:
            # Leere Strings und "not available" durch None ersetzen
            df = df.replace(['', 'not available'], None)
        
        if convert_numbers:
            # Versuchen, numerische Spalten zu konvertieren
            for col in df.columns:
                # Nur versuchen, wenn die Spalte nicht bereits numerisch ist
                if not pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        # pd.to_numeric mit errors='coerce' wandelt nicht-konvertierbare 
                        # Werte in NaN um
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except Exception:
                        # Bei Fehlern, die Spalte unverändert lassen
                        pass
        
        log_message(
            'info',
            f"CSV-Datei erfolgreich eingelesen: {len(df)} gültige Datensätze",
            username=username
        )
        return df
    
    except FileNotFoundError:
        error_msg = f"Die Datei '{file_path}' wurde nicht gefunden"
        log_message('error', error_msg, username=username)
        raise
    except Exception as e:
        error_msg = f"Fehler beim Einlesen der CSV-Datei: {str(e)}"
        log_message('error', error_msg, username=username)
        raise


def calculate_averages(
    file_path: str,
    age_column: str = "Alter",
    score_column: str = "Punkte",
    username: Optional[str] = None
) -> Tuple[float, float]:
    """
    Berechnet das Durchschnittsalter und die Durchschnittspunktzahl aus einer CSV-Datei.
    
    Args:
        file_path: Pfad zur CSV-Datei
        age_column: Name der Altersspalte. Standard ist "Alter"
        score_column: Name der Punktespalte. Standard ist "Punkte"
        username: Optionaler Benutzername für das Logging
    
    Returns:
        Tupel mit (Durchschnittsalter, Durchschnittspunktzahl)
        
    Raises:
        ValueError: Wenn die berechneten Durchschnitte ungültig sind
        KeyError: Wenn die angegebenen Spalten nicht in der CSV-Datei existieren
    """
    try:
        # CSV-Datei einlesen
        df = read_csv_file(file_path, username=username)
        
        # Prüfen, ob die benötigten Spalten existieren
        if age_column not in df.columns:
            error_msg = f"Spalte '{age_column}' nicht in der CSV-Datei gefunden"
            log_message('error', error_msg, username=username)
            raise KeyError(error_msg)
            
        if score_column not in df.columns:
            error_msg = f"Spalte '{score_column}' nicht in der CSV-Datei gefunden"
            log_message('error', error_msg, username=username)
            raise KeyError(error_msg)
        
        # Durchschnitte berechnen (mean() ignoriert automatisch NaN-Werte)
        avg_age = df[age_column].mean()
        avg_score = df[score_column].mean()
        
        # Prüfen auf gültige Durchschnittswerte
        if pd.isna(avg_age) or pd.isna(avg_score):
            error_msg = "Mindestens ein Durchschnittswert ist ungültig (NaN)"
            log_message('error', error_msg, username=username)
            raise ValueError(error_msg)
        
        # Anzahl der gültigen Werte für das Logging
        valid_age_count = df[age_column].notna().sum()
        valid_score_count = df[score_column].notna().sum()
        
        log_message(
            'info',
            f"Durchschnittsberechnung abgeschlossen: "
            f"Alter={avg_age:.2f} (aus {valid_age_count} Werten), "
            f"Punkte={avg_score:.2f} (aus {valid_score_count} Werten)",
            username=username
        )
        
        return avg_age, avg_score
    
    except Exception as e:
        error_msg = f"Fehler bei der Berechnung der Durchschnittswerte: {str(e)}"
        log_message('error', error_msg, username=username)
        raise


def read_csv_file_without_pandas(
    file_path: str,
    delimiter: str = ',',
    username: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Liest eine CSV-Datei ein und gibt die Daten als Liste von Dictionaries zurück.
    Verwendet das csv-Modul anstelle von pandas.
    Fehlerhafte Zeilen werden protokolliert und ignoriert.
    
    Args:
        file_path: Pfad zur CSV-Datei
        delimiter: Trennzeichen der CSV-Datei. Standard ist ','
        username: Optionaler Benutzername für das Logging
    
    Returns:
        Liste von Dictionaries mit den Daten aus der CSV-Datei
        
    Raises:
        ValueError: Wenn die Datei leer ist oder keinen Header hat
        FileNotFoundError: Wenn die Datei nicht gefunden wird
    """
    setup_logging()
    log_message(
        'info',
        f"Starte Einlesen der CSV-Datei ohne Pandas: {file_path}",
        username=username
    )
    
    try:
        results = []
        error_count = 0
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # CSV-Datei lesen
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            
            try:
                # Header lesen
                header = next(csv_reader)
                header = [h.strip() for h in header]
            except StopIteration:
                error_msg = "CSV-Datei ist leer oder hat keinen Header"
                log_message('error', error_msg, username=username)
                raise ValueError(error_msg)
            
            # Zeilen lesen
            for row_idx, row in enumerate(csv_reader, start=2):
                try:
                    # Prüfen, ob die Anzahl der Spalten mit dem Header übereinstimmt
                    if len(row) != len(header):
                        error_msg = (
                            f"Spaltenanzahl stimmt nicht mit Header überein "
                            f"(Header: {len(header)}, Zeile: {len(row)})"
                        )
                        raise ValueError(error_msg)
                    
                    # Zeile verarbeiten
                    processed_row = {}
                    for i, value in enumerate(row):
                        key = header[i]
                        value = value.strip()
                        
                        if value == '' or value == 'not available':
                            processed_row[key] = None
                        else:
                            # Versuche, numerische Werte zu konvertieren
                            try:
                                # Versuche, in Integer zu konvertieren
                                processed_row[key] = int(value)
                            except ValueError:
                                try:
                                    # Wenn nicht möglich, versuche Float
                                    processed_row[key] = float(value)
                                except ValueError:
                                    # Wenn beides nicht möglich, behalte den String-Wert
                                    processed_row[key] = value
                    
                    results.append(processed_row)
                except Exception as e:
                    error_count += 1
                    log_message(
                        'error',
                        f"Fehler in Zeile {row_idx}: {str(e)}",
                        row_data=row,
                        username=username
                    )
        
        if error_count > 0:
            log_message(
                'warning',
                f"{error_count} fehlerhafte Zeilen wurden ignoriert",
                username=username
            )
        
        log_message(
            'info',
            f"CSV-Datei erfolgreich eingelesen: {len(results)} gültige Datensätze",
            username=username
        )
        return results
    
    except FileNotFoundError:
        error_msg = f"Die Datei '{file_path}' wurde nicht gefunden"
        log_message('error', error_msg, username=username)
        raise
    except Exception as e:
        error_msg = f"Fehler beim Einlesen der CSV-Datei: {str(e)}"
        log_message('error', error_msg, username=username)
        raise


def calculate_averages_without_pandas(
    file_path: str,
    age_column: str = "Alter",
    score_column: str = "Punkte",
    username: Optional[str] = None
) -> Tuple[float, float]:
    """
    Berechnet das Durchschnittsalter und die Durchschnittspunktzahl 
    aus einer CSV-Datei ohne Pandas.
    
    Args:
        file_path: Pfad zur CSV-Datei
        age_column: Name der Altersspalte. Standard ist "Alter"
        score_column: Name der Punktespalte. Standard ist "Punkte"
        username: Optionaler Benutzername für das Logging
    
    Returns:
        Tupel mit (Durchschnittsalter, Durchschnittspunktzahl)
        
    Raises:
        ValueError: Wenn keine gültigen Daten für die Durchschnittsberechnung vorhanden sind
        KeyError: Wenn die angegebenen Spalten nicht in der CSV-Datei existieren
    """
    try:
        # CSV-Datei einlesen
        data = read_csv_file_without_pandas(file_path, username=username)
        
        if not data:
            error_msg = "Keine gültigen Daten zum Berechnen des Durchschnitts"
            log_message('error', error_msg, username=username)
            raise ValueError(error_msg)
        
        # Prüfen auf erste Zeile, um Spaltennamen zu validieren
        first_row = data[0] if data else {}
        
        if age_column not in first_row:
            error_msg = f"Spalte '{age_column}' nicht in der CSV-Datei gefunden"
            log_message('error', error_msg, username=username)
            raise KeyError(error_msg)
            
        if score_column not in first_row:
            error_msg = f"Spalte '{score_column}' nicht in der CSV-Datei gefunden"
            log_message('error', error_msg, username=username)
            raise KeyError(error_msg)
        
        # Variablen für die Summen und Zähler initialisieren
        total_age = 0
        age_count = 0
        total_score = 0
        score_count = 0
        
        # Über alle Zeilen iterieren und Summen berechnen
        for row in data:
            # Alter addieren, wenn vorhanden
            if row[age_column] is not None:
                total_age += row[age_column]
                age_count += 1
            
            # Punkte addieren, wenn vorhanden
            if row[score_column] is not None:
                total_score += row[score_column]
                score_count += 1
        
        # Durchschnitte berechnen (Division durch Null vermeiden)
        if age_count == 0:
            avg_age = 0
            log_message(
                'warning',
                f"Keine gültigen Altersangaben gefunden",
                username=username
            )
        else:
            avg_age = total_age / age_count
            
        if score_count == 0:
            avg_score = 0
            log_message(
                'warning',
                f"Keine gültigen Punkteangaben gefunden",
                username=username
            )
        else:
            avg_score = total_score / score_count
        
        log_message(
            'info',
            f"Durchschnittsberechnung ohne Pandas abgeschlossen: "
            f"Alter={avg_age:.2f} (aus {age_count} Werten), "
            f"Punkte={avg_score:.2f} (aus {score_count} Werten)",
            username=username
        )
        
        return avg_age, avg_score
    
    except Exception as e:
        error_msg = f"Fehler bei der Berechnung der Durchschnittswerte: {str(e)}"
        log_message('error', error_msg, username=username)
        raise