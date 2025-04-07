from typing import List


class InvalidExpressionError(ValueError):
    """Exception raised for errors in the mathematical expression."""
    pass


def tokenize(expression: str) -> List[str]:
    """
    Zerlegt den gegebenen mathematischen Ausdruck in einzelne Token.
    
    Token können sein:
      - Zahlen (inklusive Dezimalpunkt)
      - Operatoren: +, -, *, /
      - Klammern: ( und )
    
    Raises:
        InvalidExpressionError: Wenn ein ungültiges Zeichen gefunden wird.
    """
    tokens: List[str] = []
    current_token = ""
    
    for char in expression:
        if char.isdigit() or char == ".":
            current_token += char
        elif char in "+-*/()":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
            # Leerzeichen überspringen
            continue
        else:
            raise InvalidExpressionError(f"Ungültiges Zeichen im Ausdruck: {char}")
    
    if current_token:
        tokens.append(current_token)
    
    return tokens


def evaluate(expression: str) -> float:
    """
    Evaluiert einen mathematischen Ausdruck und gibt das Ergebnis als float zurück.
    
    Der Ausdruck wird tokenisiert und rekursiv verarbeitet:
      1. Klammerausdrücke werden rekursiv ausgewertet und ihr Ergebnis ersetzt
         den gesamten Klammerausdruck in der Tokenliste.
      2. Anschließend werden Multiplikation und Division (höhere Priorität)
         ausgewertet, wobei die Teilergebnisse in die Tokenliste "zusammengeführt" werden.
      3. Zum Schluss werden Addition und Subtraktion ausgewertet.
    
    Raises:
        InvalidExpressionError: Wenn der Ausdruck nicht mathematisch korrekt ist,
                                z. B. bei unausgeglichenen Klammern, fehlenden Operanden,
                                Division durch Null oder ungültigen Operatoren.
    """
    tokens = tokenize(expression)
    
    if not tokens:
        raise InvalidExpressionError("Ausdruck ist leer")
    
    if tokens.count("(") != tokens.count(")"):
        raise InvalidExpressionError("Unausgeglichene Klammern im Ausdruck")
    
    # Basisfall: Ausdruck besteht nur aus einer Zahl
    if len(tokens) == 1 and tokens[0].replace('.', '', 1).isdigit():
        return float(tokens[0])
    
    # Schritt 1: Rekursive Auswertung von Klammerausdrücken
    while "(" in tokens:
        start = None
        for i, token in enumerate(tokens):
            if token == "(":
                start = i  # Merke die Position der zuletzt geöffneten Klammer
            elif token == ")" and start is not None:
                inner_expr_tokens = tokens[start + 1:i]
                if not inner_expr_tokens:
                    raise InvalidExpressionError("Leerer Klammerausdruck")
                inner_expr = " ".join(inner_expr_tokens)
                value = evaluate(inner_expr)
                # Ersetze den gesamten Klammerausdruck (inkl. Klammern) durch das Ergebnis
                tokens = tokens[:start] + [str(value)] + tokens[i + 1:]
                break
        else:
            # Falls keine passende schließende Klammer gefunden wurde
            raise InvalidExpressionError("Unausgeglichene Klammern im Ausdruck")
    
    # Schritt 2: Auswertung von Multiplikation und Division (höhere Priorität)
    i = 0
    while i < len(tokens):
        if tokens[i] in ("*", "/"):
            try:
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])
            except (IndexError, ValueError):
                raise InvalidExpressionError("Ungültiger mathematischer Ausdruck")
            
            if tokens[i] == "*":
                result = left * right
            else:
                if right == 0:
                    raise InvalidExpressionError("Division durch Null")
                result = left / right
            
            # Zusammenführen: Ersetze "left operator right" durch das Ergebnis
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i = 0  # Starte die Schleife neu, da sich die Tokenliste verändert hat
        else:
            i += 1
    
    # Schritt 3: Auswertung von Addition und Subtraktion
    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-"):
            try:
                left = float(tokens[i - 1])
                right = float(tokens[i + 1])
            except (IndexError, ValueError):
                raise InvalidExpressionError("Ungültiger mathematischer Ausdruck")
            
            if tokens[i] == "+":
                result = left + right
            else:
                result = left - right
            
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i = 0  # Nach Zusammenführen neu starten
        else:
            i += 1
    
    if len(tokens) != 1:
        raise InvalidExpressionError("Ungültiger mathematischer Ausdruck")
    
    return float(tokens[0])


def main() -> None:
    test_expressions = [
        "3.5 + 4 * (2 - 1)",  # korrekt
        "3.5 + 4 * (2 - 1",   # unbalancierte Klammern
        "3.5 + 4 * )2 - 1(",   # unbalancierte Klammern
        "3.5 + 4 * (2 - )",   # fehlender Operand
        "3.5 + 4 ** 2",       # ungültiger Operator (**)
        "3.5 + 4 * (2 - 1a)",   # ungültiges Zeichen (a)
    ]
    
    for expr in test_expressions:
        try:
            result = evaluate(expr)
            print(f"Ausdruck: {expr} = {result}")
        except InvalidExpressionError as e:
            print(f"Ausdruck: {expr} -> {e}")


if __name__ == "__main__":
    main()
