"""
Testmodul für den mathematischen Ausdrucksauswerter.
"""

from expression_evaluator import evaluate

def test_evaluate():
    """Testet die evaluate-Funktion mit verschiedenen Ausdrücken."""
    # Grundlegende Operationen
    assert evaluate("3 + 2") == 5
    assert evaluate("3 - 2") == 1
    assert evaluate("3 * 2") == 6
    assert evaluate("6 / 2") == 3
    
    # Operator-Priorität
    assert evaluate("3 + 2 * 4") == 11
    assert evaluate("(3 + 2) * 4") == 20
    
    # Beispiel aus der Aufgabenstellung
    assert evaluate("3 + (2 * (1 + 1))") == 7
    
    # Komplexere Ausdrücke
    assert evaluate("3 * (4 + 2) / 3 - 1") == 5
    assert evaluate("10 / (2 + 3)") == 2
    assert evaluate("2.5 + 3.5") == 6
    
    print("Alle Tests erfolgreich!")

if __name__ == "__main__":
    test_evaluate()