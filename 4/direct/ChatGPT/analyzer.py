#!/usr/bin/env python3
"""
Dieses Modul definiert die Klasse LogAnalyzer, die Logdateien Zeile für Zeile
analysiert und die gewünschten Statistiken sammelt:
    - Anzahl gültiger Logzeilen (Anfragen)
    - Vorkommen der HTTP-Statuscodes
    - Die N häufigsten angefragten URLs
    - Die n häufigsten IP-Adressen
    - Gesamtzahl der bei erfolgreichen Anfragen (HTTP-Status 200-299) übertragenen Bytes
"""
from collections import Counter
from log_parser import parse_log_line


class LogAnalyzer:
    def __init__(self):
        self.total_requests = 0
        self.status_counts = Counter()
        self.url_counts = Counter()
        self.ip_counts = Counter()
        self.total_bytes = 0

    def process_log_file(self, file_handle):
        """Verarbeitet eine Logdatei zeilenweise.

        Args:
            file_handle: Ein Dateihandle, das die Logdatei darstellt.
        """
        for line in file_handle:
            line = line.strip()
            if not line:
                continue

            log_entry = parse_log_line(line)
            if not log_entry:
                continue  # Ungültige Zeile überspringen

            self.total_requests += 1

            # Zähle den HTTP-Statuscode
            status = log_entry.get('status')
            self.status_counts[status] += 1

            # Parsen des Request-Felds, um die URL zu extrahieren
            request = log_entry.get('request')
            if request:
                request_parts = request.split()
                if len(request_parts) >= 2:
                    url = request_parts[1]
                    self.url_counts[url] += 1

            # Zähle die IP-Adresse
            ip = log_entry.get('ip')
            if ip:
                self.ip_counts[ip] += 1

            # Summiere die Bytes, falls die Anfrage erfolgreich war (Statuscode 200-299)
            if 200 <= status < 300:
                self.total_bytes += log_entry.get('bytes', 0)

    def top_urls(self, n):
        """Gibt die n häufigsten URLs als Liste von (URL, Anzahl)-Tupeln zurück."""
        return self.url_counts.most_common(n)

    def top_ips(self, n):
        """Gibt die n häufigsten IP-Adressen als Liste von (IP, Anzahl)-Tupeln zurück."""
        return self.ip_counts.most_common(n)
