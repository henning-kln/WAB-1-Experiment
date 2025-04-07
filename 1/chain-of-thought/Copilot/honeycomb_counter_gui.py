#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zahlen-Zähler mit Wabenmuster-Hintergrund

Eine einfache GUI-Anwendung mit einer Zahl in der Mitte und zwei Knöpfen zum
Erhöhen und Verringern der Zahl. Der Hintergrund besteht aus einem Wabenmuster.
"""

import math
import tkinter as tk
from typing import List, Tuple, Optional, Any, Callable


# Konstanten
WINDOW_TITLE = "Zahlen-Zähler mit Wabenmuster"
WINDOW_SIZE = "500x400"
BG_COLOR = "#f0f0f0"
HEX_SIZE = 30  # Radius des Hexagons in Pixeln
HEX_COLORS = ["#e6e6fa", "#d8bfd8", "#dda0dd"]
HEX_OUTLINE_COLOR = "#e0e0e0"
FONT_SIZE_NUMBER = 48
FONT_SIZE_BUTTON = 16
BUTTON_WIDTH = 3
RESIZE_DELAY_MS = 100


class NumberCounterApp:
    """Hauptklasse für die Zahlen-Zähler-Anwendung mit Wabenmuster-Hintergrund."""
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialisiert die Anwendung.
        
        Args:
            root: Das Hauptfenster der Anwendung
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Aktuelle Zahl als Variable
        self.current_number: int = 0
        
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Erstellt und konfiguriert alle UI-Komponenten."""
        # Canvas für das Wabenmuster erstellen
        self.bg_canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Frame für die Steuerelemente
        self.main_frame = tk.Frame(self.bg_canvas, bg=BG_COLOR)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Frame für die Buttons
        button_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        # Button zum Verringern der Zahl
        self.decrease_button = tk.Button(
            button_frame, 
            text="-", 
            font=("Arial", FONT_SIZE_BUTTON),
            width=BUTTON_WIDTH,
            command=self.decrease_number
        )
        self.decrease_button.grid(row=0, column=0, padx=10)
        
        # Label für die Zahl in der Mitte
        self.number_label = tk.Label(
            button_frame, 
            text=str(self.current_number), 
            font=("Arial", FONT_SIZE_NUMBER),
            bg=BG_COLOR
        )
        self.number_label.grid(row=0, column=1, padx=20)
        
        # Button zum Erhöhen der Zahl
        self.increase_button = tk.Button(
            button_frame, 
            text="+", 
            font=("Arial", FONT_SIZE_BUTTON),
            width=BUTTON_WIDTH,
            command=self.increase_number
        )
        self.increase_button.grid(row=0, column=2, padx=10)
        
        # Event-Binding für Fenstergrößenänderungen
        self.root.bind("<Configure>", self._on_resize)
        
    def draw_honeycomb_pattern(self) -> None:
        """Zeichnet ein Wabenmuster (Hexagon-Muster) auf dem Canvas."""
        # Löschen des vorherigen Musters
        self.bg_canvas.delete("all")
        
        # Fenstergröße erfassen
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Hexagon-Parameter berechnen
        hex_width = HEX_SIZE * 2
        hex_height = HEX_SIZE * math.sqrt(3)
        
        # Berechnen der Anzahl der benötigten Hexagone
        cols = int(width / (hex_width * 0.75)) + 2
        rows = int(height / hex_height) + 2
        
        # Zeichnen der Hexagone
        for row in range(rows):
            offset = hex_width * 0.5 if row % 2 == 1 else 0
            for col in range(cols):
                x = col * hex_width * 0.75 + offset
                y = row * hex_height
                
                # Farbe für das Hexagon bestimmen
                color_index = (row + col) % len(HEX_COLORS)
                
                # Koordinaten für das Hexagon berechnen
                points = self._calculate_hexagon_points(x, y, HEX_SIZE)
                
                # Hexagon zeichnen
                self.bg_canvas.create_polygon(
                    points, 
                    fill=HEX_COLORS[color_index], 
                    outline=HEX_OUTLINE_COLOR, 
                    width=1
                )
    
    def _calculate_hexagon_points(self, center_x: float, center_y: float, 
                                 size: float) -> List[float]:
        """
        Berechnet die Koordinaten für ein regelmäßiges Hexagon.
        
        Args:
            center_x: X-Koordinate des Zentrums
            center_y: Y-Koordinate des Zentrums
            size: Radius des Hexagons
            
        Returns:
            Liste der X- und Y-Koordinaten für alle Ecken des Hexagons
        """
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = center_x + size * math.cos(angle)
            py = center_y + size * math.sin(angle)
            points.append(px)
            points.append(py)
        return points
    
    def _on_resize(self, event: Any) -> None:
        """
        Behandelt das Ereignis bei Änderung der Fenstergröße.
        
        Args:
            event: Das Ereignis-Objekt
        """
        # Warte kurz und zeichne dann das Muster neu, um Performance-Probleme
        # bei kontinuierlichen Größenänderungen zu vermeiden
        if hasattr(self, '_resize_job') and self._resize_job:
            self.root.after_cancel(self._resize_job)
            
        self._resize_job = self.root.after(RESIZE_DELAY_MS, self.draw_honeycomb_pattern)
    
    def increase_number(self) -> None:
        """Erhöht die Zahl um 1 und aktualisiert die Anzeige."""
        self.current_number += 1
        self._update_display()
    
    def decrease_number(self) -> None:
        """Verringert die Zahl um 1 und aktualisiert die Anzeige."""
        self.current_number -= 1
        self._update_display()
    
    def _update_display(self) -> None:
        """Aktualisiert die Zahlenanzeige im UI."""
        self.number_label.config(text=str(self.current_number))


def main() -> None:
    """Hauptfunktion zum Starten der Anwendung."""
    root = tk.Tk()
    app = NumberCounterApp(root)
    
    # Initial das Wabenmuster zeichnen (nach dem ersten Rendering des Fensters)
    root.update()
    app.draw_honeycomb_pattern()
    
    root.mainloop()


if __name__ == "__main__":
    main()