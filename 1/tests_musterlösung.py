from musterlösung import find_word
import unittest


class TestFindWord(unittest.TestCase):
    def setUp(self):
        self.grid = [
            ['A', 'B', 'C', 'E'],
            ['S', 'F', 'C', 'S'],
            ['A', 'D', 'E', 'E']
        ]

    def test_word_found(self):
        # Testet, ob ein vorhandenes Wort korrekt gefunden wird
        self.assertTrue(find_word(self.grid, "ABCCED"))
        self.assertTrue(find_word(self.grid, "SEE"))

    def test_word_not_found(self):
        # Testet Fälle, in denen das Wort nicht im Gitter vorkommt
        self.assertFalse(find_word(self.grid, "ABCB"))
        self.assertFalse(find_word(self.grid, "ABS"))
    
    def test_word_double_use(self):
        # Testet Fälle, in denen Buchstaben doppelt verwendet werden
        self.assertFalse(find_word(self.grid, "ABAB"))
        self.assertFalse(find_word(self.grid, "CCCC"))

    def test_empty_grid(self):
        # Testet, ob bei einem leeren Gitter (oder leeren Zeilen) korrekt False zurückgegeben wird
        self.assertFalse(find_word([], "ANY"))
        self.assertFalse(find_word([[]], "ANY"))

    def test_single_cell_grid(self):
        # Testet ein Gitter, das nur eine Zelle enthält
        grid_single = [['A']]
        self.assertTrue(find_word(grid_single, "A"))
        self.assertFalse(find_word(grid_single, "B"))

    def test_empty_word(self):
        # Da in der aktuellen Implementierung kein expliziter Fall für ein leeres Wort
        # abgehandelt wird, erwartet dieser Test, dass ein IndexError geworfen wird.
        with self.assertRaises(IndexError):
            find_word(self.grid, "")

if __name__ == '__main__':
    unittest.main()