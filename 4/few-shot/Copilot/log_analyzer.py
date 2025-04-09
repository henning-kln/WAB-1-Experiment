#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hauptmodul zur Analyse von Webserver-Logdateien im Common Log Format (CLF).
"""

import sys
import argparse
from typing import List

from log_parser import parse_log_file
from statistics import (
    count_requests, 
    count_status_codes, 
    get_top_urls, 
    get_top_hosts, 
    calculate_total_bytes
)

def format_bytes(bytes_value: int) -> str:
    """
    Formatiert Bytes in lesbare Größen (KB, MB, GB).
    
    Args:
        bytes_value: Anzahl der Bytes
        
    Returns:
        Formatierter String mit Einheit
    """
    for unit in ['Bytes', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

def analyze_logs(file_paths: List[str], top_n: int = 10) -> None:
    """
    Analysiert die angegebenen Logdateien und gibt die Ergebnisse aus.
    
    Args:
        file_paths: Liste der Pfade zu den zu analysierenden Logdateien
        top_n: Anzahl der anzuzeigenden Top-URLs und Top-IP-Adressen
    """
    all_entries = []
    
    for file_path in file_paths:
        print(f"Analysiere Logdatei: {file_path}")
        entries = parse_log_file(file_path)
        all_entries.extend(entries)
    
    if not all_entries:
        print("Keine gültigen Logzeilen gefunden!")
        return
    
    # Berechne alle Statistiken
    total_requests = count_requests(all_entries)
    status_counts = count_status_codes(all_entries)
    top_urls = get_top_urls(all_entries, top_n)
    top_hosts = get_top_hosts(all_entries, top_n)
    total_bytes = calculate_total_bytes(all_entries)
    
    # Ergebnisse ausgeben
    print("\n=== Webserver-Log Analyse ===")
    print(f"Gesamtanzahl der Anfragen: {total_requests}")
    
    print("\nHTTP-Statuscodes:")
    for status, count in sorted(status_counts.items()):
        percentage = (count / total_requests) * 100
        print(f"  {status}: {count} ({percentage:.2f}%)")
    
    print(f"\nTop {top_n} URLs:")
    for url, count in top_urls:
        percentage = (count / total_requests) * 100
        print(f"  {url}: {count} ({percentage:.2f}%)")
    
    print(f"\nTop {top_n} IP-Adressen:")
    for host, count in top_hosts:
        percentage = (count / total_requests) * 100
        print(f"  {host}: {count} ({percentage:.2f}%)")
    
    print(f"\nGesamte übertragene Datenmenge: {format_bytes(total_bytes)}")

def main():
    """
    Hauptfunktion für die Kommandozeilenschnittstelle.
    """
    parser = argparse.ArgumentParser(description='Analysiert Webserver-Logdateien im Common Log Format.')
    parser.add_argument('files', nargs='+', help='Eine oder mehrere zu analysierende Logdateien')
    parser.add_argument('-n', '--top-n', type=int, default=10, help='Anzahl der anzuzeigenden Top-URLs und IP-Adressen (Standard: 10)')
    
    args = parser.parse_args()
    
    analyze_logs(args.files, args.top_n)

if __name__ == "__main__":
    main()