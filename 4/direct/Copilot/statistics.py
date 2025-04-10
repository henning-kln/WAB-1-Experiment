#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modul zur Berechnung von Statistiken aus geparsten Logdateien.
"""

from typing import List, Dict, Tuple
from collections import Counter

def count_requests(log_entries: List[Dict]) -> int:
    """
    Zählt die Gesamtanzahl der Anfragen (gültige Logzeilen).
    
    Args:
        log_entries: Liste der geparsten Logzeilen
        
    Returns:
        Anzahl der Anfragen
    """
    return len(log_entries)

def count_status_codes(log_entries: List[Dict]) -> Dict[int, int]:
    """
    Zählt die Häufigkeit jedes HTTP-Statuscodes.
    
    Args:
        log_entries: Liste der geparsten Logzeilen
        
    Returns:
        Dictionary mit Statuscodes und deren Häufigkeit
    """
    status_counter = Counter()
    for entry in log_entries:
        status_counter[entry['status']] += 1
    
    return dict(status_counter)

def get_top_urls(log_entries: List[Dict], n: int = 10) -> List[Tuple[str, int]]:
    """
    Ermittelt die N am häufigsten angefragten URLs.
    
    Args:
        log_entries: Liste der geparsten Logzeilen
        n: Anzahl der zurückzugebenden Top-URLs
        
    Returns:
        Liste von Tupeln (URL, Anzahl)
    """
    url_counter = Counter()
    for entry in log_entries:
        url_counter[entry['url']] += 1
    
    return url_counter.most_common(n)

def get_top_hosts(log_entries: List[Dict], n: int = 10) -> List[Tuple[str, int]]:
    """
    Ermittelt die N häufigsten IP-Adressen.
    
    Args:
        log_entries: Liste der geparsten Logzeilen
        n: Anzahl der zurückzugebenden Top-IPs
        
    Returns:
        Liste von Tupeln (IP, Anzahl)
    """
    host_counter = Counter()
    for entry in log_entries:
        host_counter[entry['host']] += 1
    
    return host_counter.most_common(n)

def calculate_total_bytes(log_entries: List[Dict]) -> int:
    """
    Berechnet die Gesamtmenge der erfolgreich übertragenen Bytes.
    Als erfolgreich gelten alle Anfragen mit Status 2xx und 3xx.
    
    Args:
        log_entries: Liste der geparsten Logzeilen
        
    Returns:
        Summe der übertragenen Bytes
    """
    total_bytes = 0
    for entry in log_entries:
        # Nur erfolgreiche Anfragen zählen (2xx und 3xx)
        if 200 <= entry['status'] < 400:
            total_bytes += entry['bytes_sent']
    
    return total_bytes