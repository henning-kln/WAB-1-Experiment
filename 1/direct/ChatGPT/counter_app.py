import tkinter as tk


class CounterApp:
    """GUI Application that displays a counter with a patterned background."""

    def __init__(self, width=400, height=300):
        self.width = width
        self.height = height
        self.counter = 0
        self.root = tk.Tk()
        self.root.title("Counter App")

        # Erstelle ein Canvas, das als Hintergrund dient
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        # Zeichne das Warbenmuster (Streifenmuster)
        self.draw_background_pattern()

        # Erstelle ein Label, um die Zahl in der Mitte anzuzeigen
        self.label = tk.Label(self.root, text=str(self.counter),
                              font=("Arial", 24), bg="white")
        # Platziere das Label in der Mitte des Canvas
        self.canvas.create_window(self.width // 2, self.height // 2,
                                  window=self.label)

        # Erstelle die Buttons zum Erhöhen und Verringern der Zahl
        self.increase_button = tk.Button(self.root, text="Increase",
                                         command=self.increase_counter)
        self.decrease_button = tk.Button(self.root, text="Decrease",
                                         command=self.decrease_counter)
        # Platziere die Buttons oberhalb und unterhalb des Labels
        self.canvas.create_window(self.width // 2, self.height // 2 + 40,
                                  window=self.increase_button)
        self.canvas.create_window(self.width // 2, self.height // 2 - 40,
                                  window=self.decrease_button)

    def draw_background_pattern(self):
        """Zeichnet ein Streifenmuster als Hintergrund im Canvas."""
        stripe_height = 20
        num_stripes = self.height // stripe_height + 1
        colors = ["#ADD8E6", "#FFFFFF"]  # Hellblau und Weiß

        for i in range(num_stripes):
            y0 = i * stripe_height
            y1 = y0 + stripe_height
            color = colors[i % len(colors)]
            self.canvas.create_rectangle(0, y0, self.width, y1,
                                         fill=color, outline="")

    def increase_counter(self):
        """Erhöht den Zähler um 1 und aktualisiert das Label."""
        self.counter += 1
        self.label.config(text=str(self.counter))

    def decrease_counter(self):
        """Verringert den Zähler um 1 und aktualisiert das Label."""
        self.counter -= 1
        self.label.config(text=str(self.counter))

    def run(self):
        """Startet die Tkinter-Hauptschleife."""
        self.root.mainloop()
