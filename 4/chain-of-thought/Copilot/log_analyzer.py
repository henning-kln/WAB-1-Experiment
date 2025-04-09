#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Server Log Analyzer.

Analyzes web server logs in Common Log Format (CLF) to count valid log entries,
count HTTP status codes, display top URLs and IPs, and calculate transferred bytes.
"""

import re
import os
import sys
from glob import glob
from collections import Counter
from datetime import datetime


def parse_log_entry(line):
    """
    Parse a single log entry in Common Log Format.

    Args:
        line (str): A single line from a log file

    Returns:
        dict or None: Parsed log entry or None if invalid format
    """
    clf_pattern = (
        r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] '
        r'"([^"]*)" (\d{3}) (\S+)$'
    )
    match = re.match(clf_pattern, line.strip())
    
    if not match:
        return None
        
    groups = match.groups()
    request_parts = groups[4].split()
    
    result = {
        'ip_address': groups[0],
        'status_code': groups[5],
        'bytes_sent': groups[6],
        'url': request_parts[1] if len(request_parts) >= 2 else '-'
    }
    
    return result


def analyze_log_file(file_path):
    """
    Analyze log entries in a file.
    
    Args:
        file_path (str): Path to the log file
        
    Returns:
        tuple: (valid_entries, status_codes, urls, ip_addresses, total_bytes)
    """
    valid_entries = 0
    status_codes = Counter()
    urls = Counter()
    ip_addresses = Counter()
    total_bytes = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    entry = parse_log_entry(line)
                    if entry is None:
                        continue
                    
                    valid_entries += 1
                    ip_addresses[entry['ip_address']] += 1
                    status_codes[entry['status_code']] += 1
                    urls[entry['url']] += 1
                    
                    # Count bytes for successful responses (2xx status codes)
                    if (entry['status_code'].startswith('2') and 
                            entry['bytes_sent'] != '-'):
                        try:
                            bytes_sent = int(entry['bytes_sent'])
                            total_bytes += bytes_sent
                        except ValueError:
                            pass
                except Exception as e:
                    print(f"Error parsing line {line_number} in {file_path}: {e}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    
    return valid_entries, status_codes, urls, ip_addresses, total_bytes


def format_bytes(bytes_count):
    """
    Format bytes into a human-readable string.
    
    Args:
        bytes_count (int): Number of bytes
        
    Returns:
        str: Formatted string with appropriate unit
    """
    if bytes_count == 0:
        return "0 Bytes"
        
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    value = float(bytes_count)
    
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{value:.2f} {units[unit_index]}"


def get_status_code_description(status_code):
    """
    Return a description for common HTTP status codes.
    
    Args:
        status_code (str): HTTP status code
        
    Returns:
        str: Description of the status code
    """
    descriptions = {
        "200": "OK",
        "201": "Created",
        "204": "No Content",
        "301": "Moved Permanently",
        "302": "Found",
        "304": "Not Modified",
        "400": "Bad Request",
        "401": "Unauthorized",
        "403": "Forbidden",
        "404": "Not Found",
        "405": "Method Not Allowed",
        "500": "Internal Server Error",
        "502": "Bad Gateway",
        "503": "Service Unavailable",
        "504": "Gateway Timeout"
    }
    
    return descriptions.get(status_code, "Unknown Status Code")


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        tuple: (file_paths, top_urls_count, top_ips_count)
    """
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file_path> [log_file_path2 ...] "
              "[--top-urls N] [--top-ips n]")
        sys.exit(1)
    
    # Default values
    top_urls_count = 10
    top_ips_count = 10
    
    args = sys.argv[1:]
    file_args = []
    
    i = 0
    while i < len(args):
        if args[i] == "--top-urls" and i + 1 < len(args):
            try:
                top_urls_count = int(args[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid value for --top-urls: {args[i + 1]}")
                sys.exit(1)
        elif args[i] == "--top-ips" and i + 1 < len(args):
            try:
                top_ips_count = int(args[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid value for --top-ips: {args[i + 1]}")
                sys.exit(1)
        else:
            file_args.append(args[i])
            i += 1
    
    if not file_args:
        print("No log files specified.")
        sys.exit(1)
    
    # Expand file patterns (e.g., *.log)
    expanded_file_paths = []
    for pattern in file_args:
        paths = glob(pattern)
        if not paths:
            print(f"Warning: No files found matching pattern '{pattern}'")
        expanded_file_paths.extend([p for p in paths if os.path.isfile(p)])
    
    if not expanded_file_paths:
        print("No valid log files found.")
        sys.exit(1)
        
    return expanded_file_paths, top_urls_count, top_ips_count


def print_statistics(total_valid_entries, total_bytes, status_codes, urls, ip_addresses,
                    top_urls_count, top_ips_count):
    """
    Print analysis statistics.
    
    Args:
        total_valid_entries (int): Total number of valid log entries
        total_bytes (int): Total bytes transferred
        status_codes (Counter): Counter of HTTP status codes
        urls (Counter): Counter of URLs
        ip_addresses (Counter): Counter of IP addresses
        top_urls_count (int): Number of top URLs to display
        top_ips_count (int): Number of top IP addresses to display
    """
    # Print execution information
    print(f"\nAusführungsdatum: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Benutzer: {os.getenv('USER', 'unbekannt')}")
    
    # Print summary
    print(f"\nGesamtanzahl der gültigen Anfragen: {total_valid_entries}")
    print(f"Erfolgreich übertragene Datenmenge: {format_bytes(total_bytes)} "
          f"({total_bytes:,} Bytes)".replace(',', '.'))
    
    # Print status code statistics
    print("\nHTTP-Statuscode Statistik:")
    for status_code, count in sorted(status_codes.items()):
        status_description = get_status_code_description(status_code)
        percentage = (count / total_valid_entries) * 100 if total_valid_entries > 0 else 0
        print(f"  {status_code} ({status_description}): {count} ({percentage:.2f}%)")
    
    # Print top URLs
    print(f"\nDie {top_urls_count} häufigsten URLs:")
    for url, count in urls.most_common(top_urls_count):
        percentage = (count / total_valid_entries) * 100 if total_valid_entries > 0 else 0
        print(f"  {url}: {count} ({percentage:.2f}%)")
    
    # Print top IP addresses
    print(f"\nDie {top_ips_count} häufigsten IP-Adressen:")
    for ip, count in ip_addresses.most_common(top_ips_count):
        percentage = (count / total_valid_entries) * 100 if total_valid_entries > 0 else 0
        print(f"  {ip}: {count} ({percentage:.2f}%)")


def main():
    """Main function to process log files and analyze log entries."""
    # Parse command line arguments
    file_paths, top_urls_count, top_ips_count = parse_arguments()
    
    total_valid_entries = 0
    all_status_codes = Counter()
    all_urls = Counter()
    all_ip_addresses = Counter()
    total_bytes_transferred = 0
    
    # Process each file
    for file_path in file_paths:
        file_entries, file_status_codes, file_urls, file_ips, file_bytes = analyze_log_file(file_path)
        print(f"Found {file_entries} valid requests in {file_path}")
        total_valid_entries += file_entries
        all_status_codes.update(file_status_codes)
        all_urls.update(file_urls)
        all_ip_addresses.update(file_ips)
        total_bytes_transferred += file_bytes
    
    # Print statistics
    print_statistics(
        total_valid_entries, 
        total_bytes_transferred,
        all_status_codes, 
        all_urls, 
        all_ip_addresses,
        top_urls_count, 
        top_ips_count
    )


if __name__ == "__main__":
    main()