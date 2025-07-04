# tests.py

import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


class TestCalculator(unittest.TestCase):
    def test_run_python_file_main(self):
        result = run_python_file("calculator", "main.py")
        print(result)
    
    def test_run_python_file_tests(self):
        result = run_python_file("calculator", "tests.py")
        print(result)
    
    def test_run_python_file_err(self):
        result = run_python_file("calculator", "../main.py")
        print(result)
    
    def test_run_python_file_nonexistent(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)

    # def test_subtraction(self):
    #     result = self.calculator.evaluate("10 - 4")
    #     self.assertEqual(result, 6)

    # def test_multiplication(self):
    #     result = self.calculator.evaluate("3 * 4")
    #     self.assertEqual(result, 12)

    # def test_division(self):
    #     result = self.calculator.evaluate("10 / 2")
    #     self.assertEqual(result, 5)

    # def test_nested_expression(self):
    #     result = self.calculator.evaluate("3 * 4 + 5")
    #     self.assertEqual(result, 17)

    # def test_complex_expression(self):
    #     result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
    #     self.assertEqual(result, 7)

    # def test_empty_expression(self):
    #     result = self.calculator.evaluate("")
    #     self.assertIsNone(result)

    # def test_invalid_operator(self):
    #     with self.assertRaises(ValueError):
    #         self.calculator.evaluate("$ 3 5")

    # def test_not_enough_operands(self):
    #     with self.assertRaises(ValueError):
    #         self.calculator.evaluate("+ 3")


if __name__ == "__main__":
    unittest.main()