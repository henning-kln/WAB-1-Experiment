"""
Modul zur Auswertung mathematischer Ausdrücke.
Unterstützt die Operationen +, -, *, / und Klammern.
"""

def tokenize(expression: str) -> list:
    """Konvertiert einen Ausdruck in eine Liste von Tokens."""
    tokens = []
    i = 0
    
    while i < len(expression):
        char = expression[i]
        
        # Leerzeichen überspringen
        if char.isspace():
            i += 1
            continue
        
        # Zahlen verarbeiten
        if char.isdigit():
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                j += 1
            tokens.append(float(expression[i:j]))
            i = j
            continue
        
        # Operatoren und Klammern
        if char in '+-*/()':
            tokens.append(char)
            i += 1
            continue
        
        # Ungültiges Zeichen
        raise ValueError(f"Ungültiges Zeichen im Ausdruck: {char}")
    
    return tokens

def infix_to_postfix(tokens: list) -> list:
    """Konvertiert Infix-Notation zu Postfix-Notation mit dem Shunting-Yard-Algorithmus."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    
    for token in tokens:
        # Wenn Token eine Zahl ist, füge sie zur Ausgabe hinzu
        if isinstance(token, float):
            output.append(token)
        
        # Wenn Token ein Operator ist
        elif token in '+-*/':
            while (operators and operators[-1] in '+-*/' and 
                   precedence.get(operators[-1], 0) >= precedence.get(token, 0)):
                output.append(operators.pop())
            operators.append(token)
        
        # Wenn Token eine öffnende Klammer ist
        elif token == '(':
            operators.append(token)
        
        # Wenn Token eine schließende Klammer ist
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            
            if operators and operators[-1] == '(':
                operators.pop()  # Entferne die öffnende Klammer
            else:
                raise ValueError("Unpassende Klammern")
    
    # Verbleibende Operatoren zur Ausgabe hinzufügen
    while operators:
        if operators[-1] == '(':
            raise ValueError("Unpassende Klammern")
        output.append(operators.pop())
    
    return output

def evaluate_postfix(postfix: list) -> float:
    """Wertet einen Postfix-Ausdruck aus."""
    stack = []
    
    for token in postfix:
        # Wenn Token eine Zahl ist, lege sie auf den Stack
        if isinstance(token, float):
            stack.append(token)
        
        # Wenn Token ein Operator ist
        elif token in '+-*/':
            if len(stack) < 2:
                raise ValueError("Ungültiger Ausdruck")
            
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division durch Null")
                stack.append(a / b)
    
    # Das Ergebnis sollte das einzige Element auf dem Stack sein
    if len(stack) != 1:
        raise ValueError("Ungültiger Ausdruck")
    
    return stack[0]

def evaluate(expression: str) -> float:
    """
    Wertet einen mathematischen Ausdruck mit +, -, *, / und Klammern aus.
    
    Args:
        expression: Ein String, der den mathematischen Ausdruck enthält
        
    Returns:
        Das Ergebnis der Auswertung als Zahl
        
    Beispiel:
        >>> evaluate("3 + (2 * (1 + 1))")
        7
    """
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix)
    
    # Wenn das Ergebnis ganzzahlig ist, gib es als Integer zurück
    if result == int(result):
        return int(result)
    return result