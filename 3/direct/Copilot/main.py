"""
Hauptprogramm zum Testen des mathematischen Ausdrucksauswerters.
"""

from expression_evaluator import evaluate

def main():
    """Führt eine einfache Benutzeroberfläche zum Testen der Ausdrucksauswertung aus."""
    print("Mathematischer Ausdrucksauswerter")
    print("Geben Sie 'exit' ein, um das Programm zu beenden.")
    
    while True:
        try:
            expression = input("\nBitte geben Sie einen Ausdruck ein: ")
            if expression.lower() in ['exit', 'quit', 'ende']:
                break
                
            result = evaluate(expression)
            print(f"Ergebnis: {result}")
            
        except Exception as e:
            print(f"Fehler: {e}")

if __name__ == "__main__":
    main()