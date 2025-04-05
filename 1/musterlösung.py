from typing import List, Set


def find_word(grid: List[List[str]], word: str) -> bool:
    """
    Prüft, ob ein gegebenes Wort durch benachbarte
    Buchstaben (oben, unten, links, rechts)
    in einem 2D-Array gebildet werden kann, ohne
    ein Feld mehr als einmal zu verwenden.

    Args:
        grid: 2D-Liste von Zeichen, die das Buchstabenraster repräsentiert.
        word: Das zu suchende Wort.

    Returns:
        True, wenn das Wort gefunden werden kann, ansonsten False.
    """

    if not grid or not grid[0]:
        return False

    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int, index: int, visited: Set[tuple]) -> bool:
        # Wenn alle Buchstaben gefunden wurden, ist das Wort vollständig
        if index == len(word):
            return True

        # Prüfe, ob (r, c) außerhalb des Gitters liegt oder
        # bereits besucht wurde
        r_out_of_bounds = r < 0 or r >= rows
        c_out_of_bounds = c < 0 or c >= cols
        is_visited = (r, c) in visited
        if r_out_of_bounds or c_out_of_bounds or is_visited:
            return False

        # Wenn der aktuelle Buchstabe nicht passt, abbrechen
        if grid[r][c] != word[index]:
            return False

        # Markiere das aktuelle Feld als besucht
        visited.add((r, c))

        # Prüfe alle vier Richtungen (unten, oben, rechts, links)
        down = dfs(r + 1, c, index + 1, visited)
        up = dfs(r - 1, c, index + 1, visited)
        right = dfs(r, c + 1, index + 1, visited)
        left = dfs(r, c - 1, index + 1, visited)
        if (down or up or right or left):
            return True

        # Backtracking: Entferne den aktuellen Punkt aus der Besuchsliste
        visited.remove((r, c))
        return False

    # Starte die Suche an jedem Feld, das zum ersten Buchstaben passt
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == word[0] and dfs(i, j, 0, set()):
                return True

    return False
