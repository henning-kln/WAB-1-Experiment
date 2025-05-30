import ast
import operator

def evaluate(expression: str) -> float:
    """
    Wandelt einen mathematischen Ausdruck in einen AST um und wertet diesen
    rekursiv aus. Erlaubt werden die Operatoren +, -, * und / sowie Klammern.
    """
    # Definierte erlaubte Operatoren
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }

    def eval_node(node):
        if isinstance(node, ast.BinOp):
            # Rekursive Auswertung des linken und rechten Ausdrucks
            left_val = eval_node(node.left)
            right_val = eval_node(node.right)
            op_type = type(node.op)
            if op_type in allowed_operators:
                return allowed_operators[op_type](left_val, right_val)
            else:
                raise ValueError(f"Operator {op_type} nicht erlaubt")
        elif isinstance(node, ast.UnaryOp):
            # Unterstützung für unäre Plus- und Minusoperatoren
            if isinstance(node.op, ast.UAdd):
                return +eval_node(node.operand)
            elif isinstance(node.op, ast.USub):
                return -eval_node(node.operand)
            else:
                raise ValueError("Unärer Operator nicht erlaubt")
        elif isinstance(node, ast.Num):  # Für Python-Versionen vor 3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Für Python 3.8 und höher
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Nur int und float als Konstanten erlaubt")
        else:
            raise ValueError("Nicht unterstützter Ausdruckstyp")
    
    try:
        # Parse den Ausdruck im "eval"-Modus
        parsed_expr = ast.parse(expression, mode='eval')
        return eval_node(parsed_expr.body)
    except Exception as e:
        raise ValueError(f"Ungültiger Ausdruck: {expression}") from e

# Beispiel:
print(evaluate("3 + (2 * (1 * 1))"))  # Ausgabe: 7
print(evaluate("3 + 2 * 1"))  # Ausgabe: 5


### selbsterstelle Tests
# Test 1: Einfache Addition
print(evaluate("1 + 1"))  # Erwartete Ausgabe: 2
# Test 2: Einfache Subtraktion
print(evaluate("5 - 3"))  # Erwartete Ausgabe: 2
# Test 3: Einfache Multiplikation
print(evaluate("2 * 3"))  # Erwartete Ausgabe: 6
# Test 4: Einfache Division
print(evaluate("6 / 3"))  # Erwartete Ausgabe: 2.0
# Test 5: Kombination von Operationen
print(evaluate("2 + 3 * 4"))  # Erwartete Ausgabe: 14
# Test 6: Verwendung von Klammern
print(evaluate("(2 + 3) * 4"))  # Erwartete Ausgabe: 20
# Test 7: Negative Zahlen
print(evaluate("-2 + 3"))  # Erwartete Ausgabe: 1
# Test 8: Komplexer Ausdruck
print(evaluate("3 + 2 * (1 - 5)"))  # Erwartete Ausgabe: -5
# Test 9: Division durch Null (sollte eine Ausnahme auslösen)
try:
    print(evaluate("1 / 0"))
except ValueError as e:
    print(f"Fehler: {e}")