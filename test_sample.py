import unittest
from sample import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_numbers(self):
        self.assertEqual(add_numbers(5, 10), 15)
    
    def test_add_numbers_negative(self):
        self.assertEqual(add_numbers(-5, -10), -15)

if __name__ == '__main__':
    unittest.main()