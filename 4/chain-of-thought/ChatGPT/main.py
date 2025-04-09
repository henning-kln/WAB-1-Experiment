#!/usr/bin/env python3
"""
Webserver-Loganalyse

Dieses Skript analysiert Logdateien im Common Log Format (CLF) und berechnet
folgende Statistiken:
  - Gesamtzahl der gültigen Logzeilen (Anfragen)
  - Häufigkeit der HTTP-Statuscodes
  - Meist angefragte URLs
  - Häufigste IP-Adressen
  - Summe der erfolgreich übertragenen Bytes (nur bei 2xx-Status)
"""

import re
import argparse
from collections import defaultdict
from typing import List, Tuple, Dict


def count_valid_logs_with_details(
    filenames: List[str]
) -> Tuple[int, Dict[str, int], Dict[str, int], Dict[str, int], int]:
    """
    Liest die angegebenen Logdateien ein und sammelt Statistiken.

    Parameter:
        filenames (List[str]): Liste der Pfade zu den Logdateien.

    Rückgabe:
        Tuple:
            total_valid (int): Anzahl der gültigen Logzeilen.
            status_counts (Dict[str, int]): Häufigkeit der HTTP-Statuscodes.
            url_counts (Dict[str, int]): Häufigkeit der aufgerufenen URLs.
            ip_counts (Dict[str, int]): Häufigkeit der abfragenden IP-Adressen.
            total_bytes (int): Summe der erfolgreich übertragenen Bytes (bei HTTP 2xx).
    """
    # Regulärer Ausdruck zur Erkennung einer Logzeile im Common Log Format
    log_pattern = re.compile(
        r"^(?P<host>\S+)\s+"           # IP-Adresse (Host)
        r"(?P<ident>\S+)\s+"           # Ident (meist '-')
        r"(?P<authuser>\S+)\s+"        # Authuser (meist '-')
        r"\[(?P<date>.*?)\]\s+"        # Datum in eckigen Klammern
        r'"(?P<request>.*?)"\s+'       # Request (z. B. "GET /index.html HTTP/1.1")
        r"(?P<status>\d{3})\s+"        # HTTP-Statuscode
        r"(?P<bytes>\S+)$"             # Übertragene Bytes oder '-' bei unbekannt
    )

    total_valid = 0
    status_counts = defaultdict(int)
    url_counts = defaultdict(int)
    ip_counts = defaultdict(int)
    total_bytes = 0

    for filename in filenames:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    match = log_pattern.match(line)
                    if match:
                        total_valid += 1

                        # Zähle HTTP-Statuscode
                        status = match.group("status")
                        status_counts[status] += 1

                        # Zähle IP-Adresse
                        ip = match.group("host")
                        ip_counts[ip] += 1

                        # Extrahiere die URL aus dem Request-Feld ("METHOD URL PROTOCOL")
                        request = match.group("request")
                        request_parts = request.split()
                        if len(request_parts) >= 2:
                            url = request_parts[1]
                            url_counts[url] += 1

                        # Summiere die Bytes, wenn die Anfrage erfolgreich war (Status 2xx)
                        bytes_field = match.group("bytes")
                        if status.startswith("2") and bytes_field != "-":
                            try:
                                total_bytes += int(bytes_field)
                            except ValueError:
                                # Bei ungültigen Zahlenwerten wird der Eintrag übersprungen.
                                pass
        except Exception as exc:
            print(f"Fehler beim Lesen von {filename}: {exc}")

    return total_valid, dict(status_counts), dict(url_counts), dict(ip_counts), total_bytes


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse von Webserver-Logs im Common Log Format (CLF)"
    )
    parser.add_argument(
        "files",
        metavar="file",
        nargs="+",
        help="Zu analysierende Logdateien",
    )
    parser.add_argument(
        "--top-urls",
        type=int,
        default=10,
        help="Anzahl der häufigsten URLs, die aufgelistet werden sollen (Standard: 10)",
    )
    parser.add_argument(
        "--top-ips",
        type=int,
        default=10,
        help="Anzahl der häufigsten IP-Adressen, die aufgelistet werden sollen (Standard: 10)",
    )
    args = parser.parse_args()

    (
        total_valid,
        status_counts,
        url_counts,
        ip_counts,
        total_bytes,
    ) = count_valid_logs_with_details(args.files)

    print(f"Es gab {total_valid} gültige Anfragen.\n")

    print("HTTP-Statuscodes:")
    for status in sorted(status_counts):
        print(f"  {status}: {status_counts[status]}")

    print("\nTop angefragte URLs:")
    top_urls = sorted(url_counts.items(), key=lambda x: x[1], reverse=True)[
        : args.top_urls
    ]
    for url, count in top_urls:
        print(f"  {url}: {count} Anfragen")

    print("\nTop IP-Adressen:")
    top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[
        : args.top_ips
    ]
    for ip, count in top_ips:
        print(f"  {ip}: {count} Anfragen")

    print(f"\nErfolgreich übertragene Bytes (nur 2xx Status): {total_bytes}")


if __name__ == "__main__":
    main()
