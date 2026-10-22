import unittest

from fibonacci_testable import fibonacci, fibonacci_sequence


class TestFibonacci(unittest.TestCase):
    def test_base_cases(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

    def test_known_values(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, value in enumerate(expected):
            self.assertEqual(fibonacci(i), value)

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            fibonacci(1.5)
        with self.assertRaises(TypeError):
            fibonacci("5")
        with self.assertRaises(TypeError):
            fibonacci(True)


class TestFibonacciSequence(unittest.TestCase):
    def test_empty_sequence(self):
        self.assertEqual(fibonacci_sequence(0), [])

    def test_sequence_values(self):
        self.assertEqual(
            fibonacci_sequence(10),
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
        )

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            fibonacci_sequence(-3)

    def test_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            fibonacci_sequence(3.0)


if __name__ == "__main__":
    unittest.main()
