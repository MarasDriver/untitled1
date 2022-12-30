from unittest import TestCase
from hasło import defklas


class HasloTest(TestCase):
    def sprawdz_haslo(self):
        czytaj = open(r"/hasło.txt", "r+")
        print(czytaj)
        p = defklas()
        self.assertEqual('dupa', czytaj)
