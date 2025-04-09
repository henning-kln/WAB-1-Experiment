#!/usr/bin/env python3
"""
Hauptmodul für das Log Analyzer Tool.
Dieses Programm verarbeitet Logdateien im Common Log Format und gibt aus:
    - Die Anzahl gültiger Logzeilen (Anfragen)
    - Die Häufigkeit der HTTP-Statuscodes
    - Die N häufigsten angefragten URLs
    - Die n häufigsten IP-Adressen
    - Die insgesamt erfolgreich übertragenen Bytes (bei HTTP-Status 200-299)
"""
import argparse
import sys
from analyzer import LogAnalyzer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analysiere Webserver-Logdateien im Common Log Format (CLF)."
    )
    parser.add_argument(
        '-f', '--files',
        nargs='+',
        required=True,
        help="Pfad(e) zur/logdatei(en), die analysiert werden sollen."
    )
    parser.add_argument(
        '-u', '--top-urls',
        type=int,
        default=10,
        help="Anzahl der häufigsten URLs, die ausgegeben werden sollen."
    )
    parser.add_argument(
        '-i', '--top-ips',
        type=int,
        default=10,
        help="Anzahl der häufigsten IP-Adressen, die ausgegeben werden sollen."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    analyzer = LogAnalyzer()

    for file_path in args.files:
        try:
            with open(file_path, 'r') as log_file:
                analyzer.process_log_file(log_file)
        except FileNotFoundError:
            sys.stderr.write(f"Fehler: Datei nicht gefunden: {file_path}\n")
        except IOError as e:
            sys.stderr.write(f"Fehler beim Lesen der Datei {file_path}: {e}\n")

    print("Ergebnisse der Log-Analyse:")
    print(f"Anzahl gültiger Logzeilen (Anfragen): {analyzer.total_requests}")
    print("\nHTTP-Statuscodes:")
    for status, count in sorted(analyzer.status_counts.items()):
        print(f"  {status}: {count}")

    print("\nTop angefragte URLs:")
    for url, count in analyzer.top_urls(args.top_urls):
        print(f"  {url}: {count}")

    print("\nTop IP-Adressen:")
    for ip, count in analyzer.top_ips(args.top_ips):
        print(f"  {ip}: {count}")

    print("\nInsgesamt erfolgreich übertragene Bytes (HTTP-Status 200-299):")
    print(analyzer.total_bytes)


if __name__ == '__main__':
    main()
