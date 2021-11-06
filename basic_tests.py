import unittest
from potential import Grid


class GridTest(unittest.TestCase):
    def test_instantiate_grid(self):
        with self.assertRaises(Exception):

            Grid(10, 2, 2, 2)

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
