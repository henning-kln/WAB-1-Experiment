import tkinter as tk
import math

class HoneycombCounter:
    """
    Eine GUI-Anwendung mit Wabenmuster im Hintergrund und einem Zähler,
    der durch Knöpfe erhöht oder verringert werden kann.
    """
    def __init__(self, root):
        """Initialisiert die GUI-Anwendung."""
        self.root = root
        self.root.title("Wabenmuster-Zähler")
        self.root.geometry("600x400")
        
        # Zählervariable
        self.counter = tk.IntVar(value=0)
        
        # Canvas für das Wabenmuster erstellen
        self.canvas = tk.Canvas(root, bg="#f0f0f0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Wabenmuster zeichnen
        self.draw_honeycomb_pattern()
        
        # Frame für den Zähler mit leichter Transparenz
        self.center_frame = tk.Frame(self.canvas, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.center_window = self.canvas.create_window(
            300, 200, window=self.center_frame
        )
        
        # Zähleranzeige erstellen
        self.counter_label = tk.Label(
            self.center_frame, 
            textvariable=self.counter, 
            font=("Arial", 48, "bold"),
            bg="#ffffff",
            padx=20,
            pady=10
        )
        self.counter_label.pack()
        
        # Steuerungsknöpfe erstellen
        self.button_frame = tk.Frame(self.center_frame, bg="#ffffff")
        self.button_frame.pack(pady=10)
        
        self.decrease_btn = tk.Button(
            self.button_frame, 
            text="-", 
            font=("Arial", 20),
            command=self.decrease_counter,
            width=3,
            bg="#e0e0e0"
        )
        self.decrease_btn.pack(side=tk.LEFT, padx=10)
        
        self.increase_btn = tk.Button(
            self.button_frame, 
            text="+", 
            font=("Arial", 20),
            command=self.increase_counter,
            width=3,
            bg="#e0e0e0"
        )
        self.increase_btn.pack(side=tk.RIGHT, padx=10)
        
        # Canvas passt sich der Fenstergröße an
        self.root.bind("<Configure>", self.on_resize)
    
    def increase_counter(self):
        """Erhöht den Zähler um 1."""
        self.counter.set(self.counter.get() + 1)
    
    def decrease_counter(self):
        """Verringert den Zähler um 1."""
        self.counter.set(self.counter.get() - 1)
    
    def draw_honeycomb_pattern(self):
        """Zeichnet das Wabenmuster auf dem Canvas."""
        self.canvas.delete("honeycomb")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Falls Canvas noch nicht realisiert wurde, Standardwerte verwenden
        if width <= 1:
            width = 600
        if height <= 1:
            height = 400
        
        # Parameter für das Wabenmuster
        hex_size = 30
        horizontal_spacing = hex_size * 1.5
        vertical_spacing = hex_size * math.sqrt(3)
        
        # Berechnen, wie viele Sechsecke benötigt werden
        cols = int(width / horizontal_spacing) + 2
        rows = int(height / vertical_spacing) + 2
        
        # Wabenmuster zeichnen
        for row in range(-1, rows):
            for col in range(-1, cols):
                # Mittelpunkt des Sechsecks berechnen
                x = col * horizontal_spacing
                y = row * vertical_spacing
                
                # Jede zweite Reihe versetzen
                if row % 2 == 1:
                    x += hex_size * 0.75
                
                # Sechseck mit einer hellen Farbe zeichnen
                color = "#e6e6fa"  # Helles Lavendel
                if (row + col) % 2 == 0:
                    color = "#d8bfd8"  # Distel
                
                self.draw_hexagon(x, y, hex_size, color)
    
    def draw_hexagon(self, x, y, size, color):
        """
        Zeichnet ein Sechseck an der angegebenen Position.
        
        Args:
            x (float): x-Koordinate des Mittelpunkts
            y (float): y-Koordinate des Mittelpunkts
            size (float): Größe des Sechsecks (Abstand vom Mittelpunkt zu den Ecken)
            color (str): Füllfarbe des Sechsecks
        """
        points = []
        for i in range(6):
            angle_rad = math.pi / 3 * i + math.pi / 6
            px = x + size * math.cos(angle_rad)
            py = y + size * math.sin(angle_rad)
            points.extend([px, py])
        
        self.canvas.create_polygon(points, fill=color, outline="#c0c0c0", tags="honeycomb")
    
    def on_resize(self, event):
        """Wird aufgerufen, wenn das Fenster die Größe ändert."""
        # Nur neu zeichnen, wenn das Hauptfenster die Größe ändert
        if event.widget == self.root:
            # Wabenmuster bei Größenänderung neu zeichnen
            self.draw_honeycomb_pattern()
            
            # Position von Zähler und Knöpfen aktualisieren
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            self.canvas.coords(self.center_window, width // 2, height // 2)


def main():
    """Hauptfunktion zum Starten der Anwendung."""
    root = tk.Tk()
    app = HoneycombCounter(root)
    root.mainloop()


if __name__ == "__main__":
    main()