import unittest
from app.core.engine import CalculatorEngine

class TestCalculatorEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.engine = CalculatorEngine()

    def test_add(self) -> None:
        self.assertEqual(self.engine.add(5, 3), 8)

    def test_subtract(self) -> None:
        self.assertEqual(self.engine.subtract(10, 4), 6)

    def test_multiply(self) -> None:
        self.assertEqual(self.engine.multiply(3, 7), 21)

    def test_divide(self) -> None:
        self.assertEqual(self.engine.divide(10, 2), 5)

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ValueError):
            self.engine.divide(10, 0)

if __name__ == "__main__":
    unittest.main()
