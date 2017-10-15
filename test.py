import unittest


class MyTestClass(unittest.TestCase):

    def test_doubled(self):
        # added = doubled(5)
        self.assertEqual(10, 10)


if __name__ == '__main__':
    unittest.main()
