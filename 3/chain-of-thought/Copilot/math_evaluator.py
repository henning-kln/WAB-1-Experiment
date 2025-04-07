"""
Modul zur Auswertung mathematischer Ausdrücke.

Dieses Modul bietet Funktionen zur Tokenisierung und Auswertung
mathematischer Ausdrücke unter Berücksichtigung der Operatorpräzedenz
und mathematischer Korrektheit.
"""

from typing import Union, List, Optional, Any, Tuple


# Typdefinitionen für bessere Lesbarkeit
Number = Union[int, float]
Token = Union[str, Number]
TokenList = List[Token]


# Konstanten
OPERATORS = {'+', '-', '*', '/', '^'}
PRECEDENCE = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}


def tokenize(expression: str) -> TokenList:
    """
    Zerlegt einen mathematischen Ausdruck in Tokens (Zahlen, Operatoren, Klammern).

    Args:
        expression: Der zu zerlegende mathematische Ausdruck als String

    Returns:
        Eine Liste von Tokens (Zahlen, Operatoren oder Klammern)

    Raises:
        ValueError: Wenn der Ausdruck syntaktisch nicht korrekt ist
    """
    if not expression:
        raise ValueError("Der Ausdruck darf nicht leer sein")

    # Entferne alle Leerzeichen aus dem Ausdruck
    expression = expression.replace(" ", "")
    
    # Überprüfung auf ungültige aufeinanderfolgende Operatoren
    for j in range(len(expression) - 1):
        if (expression[j] in OPERATORS and 
            expression[j+1] in OPERATORS and 
            not (expression[j+1] in '+-' and (j == 0 or expression[j] in '*/^('))):
            raise ValueError(
                f"Ungültige aufeinanderfolgende Operatoren: "
                f"'{expression[j]}{expression[j+1]}'"
            )
    
    tokens = []
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        # Verarbeite Zahlen (ganze Zahlen und Dezimalzahlen)
        if char.isdigit() or char == '.':
            j = i
            has_decimal = False
            
            # Extrahiere die vollständige Zahl
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                if expression[j] == '.':
                    if has_decimal:
                        raise ValueError(
                            f"Ungültige Zahl: Mehrere Dezimalpunkte in "
                            f"'{expression[i:j+1]}'"
                        )
                    has_decimal = True
                j += 1
            
            # Überprüfe spezielle Fehler bei Dezimalzahlen
            if has_decimal:
                if j > i + 1 and expression[j-1] == '.':
                    raise ValueError(
                        f"Ungültige Zahl: Dezimalpunkt am Ende von "
                        f"'{expression[i:j]}'"
                    )
                if j == i + 1:
                    raise ValueError(
                        f"Ungültige Zahl: Einzelner Dezimalpunkt an Position {i}"
                    )
            
            # Füge die Zahl als Token hinzu
            number_str = expression[i:j]
            tokens.append(float(number_str) if '.' in number_str else int(number_str))
            i = j
        
        # Verarbeite Operatoren
        elif char in OPERATORS:
            tokens.append(char)
            i += 1
        
        # Verarbeite Klammern
        elif char in '()':
            tokens.append(char)
            i += 1
        
        else:
            raise ValueError(f"Unbekanntes Zeichen: '{char}' an Position {i}")
    
    # Überprüfung auf ausgewogene Klammern
    check_balanced_brackets(tokens)
    
    # Überprüfung auf gültige Operatorpositionen
    validate_operator_positions(tokens)
    
    return tokens


def check_balanced_brackets(tokens: TokenList) -> None:
    """
    Überprüft, ob die Klammern im Ausdruck ausgewogen sind.

    Args:
        tokens: Liste der Tokens, die überprüft werden sollen

    Raises:
        ValueError: Wenn die Klammern nicht ausgewogen sind
    """
    open_brackets = 0
    
    for token in tokens:
        if token == '(':
            open_brackets += 1
        elif token == ')':
            open_brackets -= 1
            if open_brackets < 0:
                raise ValueError(
                    "Schließende Klammer ohne zugehörige öffnende Klammer"
                )
    
    if open_brackets > 0:
        raise ValueError(
            "Öffnende Klammer ohne zugehörige schließende Klammer"
        )


def validate_operator_positions(tokens: TokenList) -> None:
    """
    Überprüft, ob die Operatoren an gültigen Positionen stehen.

    Args:
        tokens: Liste der Tokens, die überprüft werden sollen

    Raises:
        ValueError: Wenn ein Operator an einer ungültigen Position steht
    """
    for i, token in enumerate(tokens):
        if token in OPERATORS:
            # Überprüfe, ob der Operator am Ende steht
            if i == len(tokens) - 1:
                raise ValueError(f"Operator '{token}' am Ende des Ausdrucks")
            
            # Überprüfe spezielle Fälle für Operatoren nach Klammern oder vor Klammern
            if (i > 0 and tokens[i-1] == '(' and token not in '+-'):
                raise ValueError(
                    f"Operator '{token}' direkt nach öffnender Klammer"
                )
            
            if i < len(tokens) - 1 and tokens[i+1] == ')':
                raise ValueError(
                    f"Operator '{token}' direkt vor schließender Klammer"
                )


def evaluate(expression: str, debug: bool = False) -> Number:
    """
    Wertet einen mathematischen Ausdruck aus.

    Diese Funktion zerlegt den Ausdruck in Tokens, überprüft dessen
    mathematische Korrektheit und berechnet das Ergebnis.

    Args:
        expression: Der auszuwertende mathematische Ausdruck als String
        debug: Wenn True, werden Zwischenschritte der Auswertung ausgegeben

    Returns:
        Das Ergebnis der Auswertung als Zahl (int oder float)

    Raises:
        ValueError: Wenn der Ausdruck mathematisch nicht korrekt ist
    """
    try:
        tokens = tokenize(expression)
        
        if debug:
            print(f"Tokenisierter Ausdruck: {tokens}")
        
        # Überprüfe, ob der Ausdruck leer ist
        if not tokens:
            raise ValueError("Der Ausdruck darf nicht leer sein")
        
        result = evaluate_tokens(tokens, debug)
        return result
    
    except Exception as e:
        # Fange alle Fehler ab und gebe einen einheitlichen Fehlertyp zurück
        error_msg = str(e)
        if not error_msg.startswith("Mathematisch ungültiger Ausdruck"):
            error_msg = f"Mathematisch ungültiger Ausdruck: {error_msg}"
        raise ValueError(error_msg)


def evaluate_tokens(tokens: TokenList, debug: bool = False, level: int = 0) -> Number:
    """
    Wertet eine Liste von Tokens rekursiv aus und führt Teilergebnisse zusammen.

    Args:
        tokens: Die Liste der auszuwertenden Tokens
        debug: Wenn True, werden Zwischenschritte der Auswertung ausgegeben
        level: Rekursionsebene für Einrückung in Debug-Ausgaben

    Returns:
        Das Ergebnis der Auswertung als Zahl

    Raises:
        ValueError: Wenn die Token-Liste nicht korrekt ausgewertet werden kann
    """
    indent = "  " * level
    
    # Basisfall: Leere Token-Liste
    if not tokens:
        raise ValueError("Leerer Ausdruck")
    
    # Basisfall: Nur ein Token und es ist eine Zahl
    if len(tokens) == 1:
        if isinstance(tokens[0], (int, float)):
            return tokens[0]
        else:
            raise ValueError(
                f"Einzelner Token '{tokens[0]}' kann nicht ausgewertet werden"
            )
    
    if debug:
        print(f"{indent}Auswertung von: {tokens}")
    
    # Kopiere Tokens, um die Originalliste nicht zu verändern
    tokens = tokens.copy()
    
    # Schritt 1: Klammern auswerten
    tokens = evaluate_brackets(tokens, debug, level)
    
    # Schritt 2: Unäre Operatoren auswerten
    tokens = evaluate_unary_operators(tokens, debug, level)
    
    # Schritt 3: Implizite Multiplikation überprüfen
    check_implicit_multiplication(tokens)
    
    # Schritt 4: Operatoren in Reihenfolge ihrer Präzedenz auswerten
    for precedence_level in range(3, 0, -1):
        tokens = evaluate_operators_by_precedence(
            tokens, precedence_level, debug, level
        )
    
    # Nach der Auswertung sollte nur noch ein Token übrig sein
    if len(tokens) != 1:
        raise ValueError(
            f"Ungültiger Ausdruck: Konnte nicht vollständig ausgewertet werden. "
            f"Übrige Tokens: {tokens}"
        )
    
    if not isinstance(tokens[0], (int, float)):
        raise ValueError(f"Ergebnis '{tokens[0]}' ist keine Zahl")
    
    if debug:
        print(f"{indent}Finales Ergebnis: {tokens[0]}")
    
    return tokens[0]


def evaluate_brackets(tokens: TokenList, debug: bool, level: int) -> TokenList:
    """
    Findet und wertet alle Klammerausdrücke in den Tokens aus.
    
    Args:
        tokens: Die zu verarbeitende Token-Liste
        debug: Debug-Modus aktivieren/deaktivieren
        level: Aktuelle Rekursionsebene
        
    Returns:
        Die aktualisierte Token-Liste mit ausgewerteten Klammerausdrücken
    """
    indent = "  " * level
    i = 0
    
    while i < len(tokens):
        if tokens[i] == '(':
            # Suche die schließende Klammer
            open_brackets = 1
            j = i + 1
            
            while j < len(tokens) and open_brackets > 0:
                if tokens[j] == '(':
                    open_brackets += 1
                elif tokens[j] == ')':
                    open_brackets -= 1
                j += 1
            
            # Überprüfe, ob der Klammerinhalt leer ist
            if j - i == 2:
                raise ValueError("Leerer Klammerausdruck")
            
            # Extrahiere den Klammerinhalt
            bracket_content = tokens[i+1:j-1]
            
            if debug:
                print(f"{indent}Klammerinhalt gefunden: {bracket_content}")
            
            # Rekursiver Aufruf für den Klammerinhalt
            sub_result = evaluate_tokens(bracket_content, debug, level + 1)
            
            if debug:
                print(
                    f"{indent}Klammerausdruck {bracket_content} = {sub_result}"
                )
            
            # Ersetze den Klammerausdruck durch sein Ergebnis
            tokens = tokens[:i] + [sub_result] + tokens[j:]
            
            if debug:
                print(f"{indent}Nach Ersetzung: {tokens}")
        else:
            i += 1
    
    return tokens


def evaluate_unary_operators(tokens: TokenList, debug: bool, level: int) -> TokenList:
    """
    Wertet unäre Operatoren (+ und -) in der Token-Liste aus.
    
    Args:
        tokens: Die zu verarbeitende Token-Liste
        debug: Debug-Modus aktivieren/deaktivieren
        level: Aktuelle Rekursionsebene
        
    Returns:
        Die aktualisierte Token-Liste mit ausgewerteten unären Operatoren
    """
    indent = "  " * level
    i = 0
    
    while i < len(tokens):
        if (tokens[i] in '+-' and 
            (i == 0 or tokens[i-1] in OPERATORS or tokens[i-1] == '(')):
            if i + 1 < len(tokens) and isinstance(tokens[i+1], (int, float)):
                if tokens[i] == '-':
                    tokens[i+1] = -tokens[i+1]
                # Entferne den unären Operator
                tokens.pop(i)
                
                if debug:
                    print(
                        f"{indent}Nach Auswertung des unären Operators: {tokens}"
                    )
            else:
                raise ValueError(
                    f"Unärer Operator '{tokens[i]}' ohne nachfolgende Zahl"
                )
        else:
            i += 1
    
    return tokens


def check_implicit_multiplication(tokens: TokenList) -> None:
    """
    Überprüft auf implizite Multiplikation (fehlende Operatoren zwischen Zahlen).
    
    Args:
        tokens: Die zu überprüfende Token-Liste
        
    Raises:
        ValueError: Wenn eine implizite Multiplikation gefunden wird
    """
    for i in range(len(tokens) - 1):
        if (isinstance(tokens[i], (int, float)) and 
            isinstance(tokens[i+1], (int, float))):
            raise ValueError(
                f"Fehlender Operator zwischen {tokens[i]} und {tokens[i+1]}"
            )


def evaluate_operators_by_precedence(
    tokens: TokenList, precedence_level: int, debug: bool, level: int
) -> TokenList:
    """
    Wertet alle Operatoren mit einer bestimmten Präzedenz aus.
    
    Args:
        tokens: Die zu verarbeitende Token-Liste
        precedence_level: Präzedenzebene der auszuwertenden Operatoren
        debug: Debug-Modus aktivieren/deaktivieren
        level: Aktuelle Rekursionsebene
        
    Returns:
        Die aktualisierte Token-Liste mit ausgewerteten Operatoren
    """
    indent = "  " * level
    i = 1
    
    while i < len(tokens):
        if (tokens[i] in OPERATORS and 
            PRECEDENCE.get(tokens[i], 0) == precedence_level):
            
            operator = tokens[i]
            
            # Überprüfe auf gültige Operanden
            if (i-1 < 0 or i+1 >= len(tokens) or 
                not isinstance(tokens[i-1], (int, float)) or 
                not isinstance(tokens[i+1], (int, float))):
                raise ValueError(
                    f"Ungültige Verwendung des Operators {operator}"
                )
            
            left = tokens[i-1]
            right = tokens[i+1]
            
            # Berechne das Ergebnis basierend auf dem Operator
            result = calculate_operation(left, operator, right)
            
            if debug:
                print(f"{indent}Berechne: {left} {operator} {right} = {result}")
            
            # Ersetze die Operation durch ihr Ergebnis
            tokens = tokens[:i-1] + [result] + tokens[i+2:]
            
            if debug:
                print(
                    f"{indent}Nach Auswertung von '{operator}': {tokens}"
                )
            
            i = 1  # Starte wieder von vorne
        else:
            i += 1
    
    return tokens


def calculate_operation(left: Number, operator: str, right: Number) -> Number:
    """
    Führt eine einzelne mathematische Operation aus.
    
    Args:
        left: Linker Operand
        operator: Mathematischer Operator ('+', '-', '*', '/', '^')
        right: Rechter Operand
        
    Returns:
        Das Ergebnis der Operation
        
    Raises:
        ValueError: Bei Division durch Null oder ungültigem Operator
    """
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        if right == 0:
            raise ValueError("Division durch Null")
        return left / right
    elif operator == '^':
        return left ** right
    else:
        raise ValueError(f"Unbekannter Operator: {operator}")


def main() -> None:
    """
    Hauptfunktion zum Testen des Auswerters für mathematische Ausdrücke.
    """
    # Korrekte Ausdrücke
    valid_expressions = [
        "2 + 3 * 4",
        "10 / (4 - 2)",
        "2.5 * 3 + 4.2",
        "(7 + 3) * (5 - 2)",
        "2^3 + 4",
        "((2 + 3) * 4) / 2",
        "-5 + 3",
        "-(2+3)"
    ]
    
    # Fehlerhafte Ausdrücke
    invalid_expressions = [
        "2 + * 3",        # Aufeinanderfolgende Operatoren
        "2 ++ 3",         # Doppelter Operator
        "(2 + 3",         # Unausgewogene Klammern
        "2 + ",           # Unvollständiger Ausdruck
        "2 3",            # Fehlender Operator
        "2..5",           # Mehrere Dezimalpunkte
        "()",             # Leere Klammern
        "2 / 0",          # Division durch Null
        "5 / (2-2)",      # Division durch Null in Klammern
        "2 + (3 *)",      # Operator am Ende eines Klammerausdrucks
        ".5 + 2"          # Dezimalpunkt am Anfang
    ]
    
    print("\n=== Auswertung korrekter Ausdrücke ===")
    for expr in valid_expressions:
        try:
            result = evaluate(expr)
            print(f"'{expr}' = {result}")
        except ValueError as e:
            print(f"FEHLER bei '{expr}': {e}")
    
    print("\n=== Auswertung fehlerhafter Ausdrücke ===")
    for expr in invalid_expressions:
        try:
            result = evaluate(expr)
            print(f"'{expr}' = {result}")
        except ValueError as e:
            print(f"FEHLER bei '{expr}': {e}")
    
    print("\n=== Detaillierte Auswertung eines Ausdrucks ===")
    try:
        test_expr = "(2 + 3) * 4 - 5^2"
        print(f"Detaillierte Auswertung von '{test_expr}':")
        result = evaluate(test_expr, debug=True)
        print(f"Ergebnis: {result}")
    except ValueError as e:
        print(f"FEHLER: {e}")


if __name__ == "__main__":
    main()