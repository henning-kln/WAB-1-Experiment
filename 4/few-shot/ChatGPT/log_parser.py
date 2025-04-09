#!/usr/bin/env python3
"""
Dieses Modul enthält Funktionen zum Parsen einzelner Logzeilen im
Common Log Format.
"""
import re

# Regulärer Ausdruck für das Common Log Format
LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'              # IP-Adresse
    r'(?P<ident>\S+)\s+'            # Ident
    r'(?P<user>\S+)\s+'             # Authuser
    r'\[(?P<time>[^\]]+)\]\s+'      # Datum und Zeit
    r'"(?P<request>[^"]*)"\s+'      # Request
    r'(?P<status>\d{3})\s+'         # HTTP-Statuscode
    r'(?P<bytes>\S+)'              # Übertragene Bytes
)


def parse_log_line(line):
    """Parst eine einzelne Logzeile und gibt ein Dictionary der Komponenten zurück.

    Args:
        line (str): Eine Zeile aus der Logdatei.

    Returns:
        dict: Dictionary mit den Feldern 'ip', 'ident', 'user', 'time',
              'request', 'status' und 'bytes'.
        None: Falls die Zeile ungültig ist.
    """
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()

    # Konvertiere Status in eine ganze Zahl
    try:
        data['status'] = int(data['status'])
    except ValueError:
        return None

    # Konvertiere Bytes in eine ganze Zahl; falls '-' oder ungültig, setze auf 0
    byte_field = data.get('bytes')
    if byte_field == '-' or not byte_field.isdigit():
        data['bytes'] = 0
    else:
        try:
            data['bytes'] = int(byte_field)
        except ValueError:
            data['bytes'] = 0

    return data
