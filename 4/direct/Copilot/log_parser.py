#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul zum Parsen von Webserver-Logdateien im Common Log Format (CLF).
"""

import re
from typing import Dict, Tuple, Optional, List

# Regulärer Ausdruck für das Common Log Format
# Format: host ident authuser [date] "request" status bytes
CLF_PATTERN = r'(\S+) (\S+) (\S+) \[(.*?)\] "([^"]*)" (\d+) (\S+)'
CLF_REGEX = re.compile(CLF_PATTERN)

def parse_log_line(line: str) -> Optional[Dict]:
    """
    Parst eine einzelne Logzeile im Common Log Format.
    
    Args:
        line: Die zu parsende Logzeile
        
    Returns:
        Dictionary mit den extrahierten Werten oder None, wenn die Zeile ungültig ist
    """
    match = CLF_REGEX.match(line.strip())
    if not match:
        return None
    
    host, ident, authuser, date, request, status, bytes_sent = match.groups()
    
    # Extrahiere URL aus der Anfrage (falls vorhanden)
    url = "-"
    request_parts = request.split()
    if len(request_parts) >= 2:
        url = request_parts[1]
    
    # Konvertiere Bytes zu Integer (falls möglich)
    try:
        bytes_sent = int(bytes_sent) if bytes_sent != '-' else 0
    except ValueError:
        bytes_sent = 0
    
    # Konvertiere Status zu Integer
    try:
        status = int(status)
    except ValueError:
        # Ungültiger Status, Zeile überspringen
        return None
    
    return {
        'host': host,
        'ident': ident,
        'authuser': authuser,
        'date': date,
        'request': request,
        'url': url,
        'status': status,
        'bytes_sent': bytes_sent
    }

def parse_log_file(file_path: str) -> List[Dict]:
    """
    Parst eine komplette Logdatei.
    
    Args:
        file_path: Pfad zur Logdatei
        
    Returns:
        Liste von Dictionaries mit geparsten Logzeilen
    """
    parsed_entries = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = parse_log_line(line)
                if entry:  # Nur gültige Einträge hinzufügen
                    parsed_entries.append(entry)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei {file_path}: {e}")
    
    return parsed_entries