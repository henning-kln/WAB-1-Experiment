import tkinter as tk
import math


class ZahlenGUI:
    """GUI-Anwendung mit Wabenmuster-Hintergrund, einer zentralen Zahl und zwei Buttons zur Veränderung der Zahl."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Zahlen-GUI mit Wabenmuster")

        # Canvas-Größen definieren
        self.canvas_width = 400
        self.canvas_height = 300

        # Canvas erstellen und packen
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        # Wabenmuster als Hintergrund zeichnen
        self._draw_honeycomb_pattern()

        # Startwert der Zahl
        self.number = 42

        # UI-Elemente erstellen
        self.label = tk.Label(master, text=str(self.number), font=("Helvetica", 48))
        self.button_decrease = tk.Button(master, text="Verringern", command=self.decrease)
        self.button_increase = tk.Button(master, text="Erhöhen", command=self.increase)

        # UI-Elemente über den Canvas positionieren
        self.canvas.create_window(self.canvas_width / 2, self.canvas_height / 2, window=self.label)
        self.canvas.create_window(self.canvas_width / 2 - 100, self.canvas_height / 2, window=self.button_decrease)
        self.canvas.create_window(self.canvas_width / 2 + 100, self.canvas_height / 2, window=self.button_increase)

    def _draw_honeycomb_pattern(self) -> None:
        """
        Zeichnet ein Wabenmuster (Hexagon-Gitter) als Hintergrund auf den Canvas.
        """
        a = 20  # Seitenlänge eines einzelnen Sechsecks
        horiz_spacing = 1.5 * a              # horizontaler Abstand der Hexagon-Zentren
        vert_spacing = (math.sqrt(3) / 2) * a  # vertikaler Abstand der Hexagon-Zentren

        cols = int(self.canvas_width / horiz_spacing) + 2
        rows = int(self.canvas_height / vert_spacing) + 2

        for row in range(rows):
            # Ungerade Reihen werden horizontal versetzt
            offset = 0 if row % 2 == 0 else 0.75 * a
            for col in range(cols):
                cx = col * horiz_spacing + offset
                cy = row * vert_spacing
                points = []
                # Berechnung der sechs Ecken des Hexagons
                for i in range(6):
                    angle = math.radians(60 * i)
                    x = cx + a * math.cos(angle)
                    y = cy + a * math.sin(angle)
                    points.extend([x, y])
                self.canvas.create_polygon(points, outline="gray", fill="white", width=1)

    def update_label(self) -> None:
        """Aktualisiert das Label, um den aktuellen Zahlenwert anzuzeigen."""
        self.label.config(text=str(self.number))

    def increase(self) -> None:
        """Erhöht die Zahl um 1 und aktualisiert das Label."""
        self.number += 1
        self.update_label()

    def decrease(self) -> None:
        """Verringert die Zahl um 1 und aktualisiert das Label."""
        self.number -= 1
        self.update_label()


def main() -> None:
    root = tk.Tk()
    app = ZahlenGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
