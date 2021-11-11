from unittest import TestCase
import aufgabe1


class TestParkingLot(TestCase):
    def test_parkplatz0(self):
        path = "/home/tarek/Projects/BWInf/Beispiele/a1-Schiebeparkplatz/beispieldaten/parkplatz0.txt"
        result = {'A': [], 'B': [], 'C': [{'H': 1}], 'D': [{'H': -1}], 'E': [], 'F': [{'I': -2}], 'G': [{'I': -1}]}
        self.assertEqual(aufgabe1.ParkingLot(path).solution, result)
