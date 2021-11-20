import unittest
import aufgabe5


class MyTestCase(unittest.TestCase):
    def test_scale(self):
        scale = aufgabe5.Scale("/home/tarek/Projects/BWInf/Beispiele/a5-Marktwaage/beispieldaten/gewichtsstuecke0.txt")
        self.assertTrue(str(scale))
        pass


if __name__ == '__main__':
    unittest.main()
