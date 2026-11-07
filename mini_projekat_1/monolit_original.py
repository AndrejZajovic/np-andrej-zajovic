"""Originalni monolitni skript (slajd 17, Nedjelja 2).

Služi samo kao polazna tačka za poređenje. Refaktorisano rješenje je u
fajlu rezervacije.py.
"""


class UpravljanjeRezervacijama:
    def __init__(self, putanja):
        self.putanja = putanja

    def ucitaj(self):
        return [l.strip().split(",")
                for l in open(self.putanja)]

    def izracunaj_iznos(self, r):
        return int(r[1]) * float(r[2])

    def sacuvaj_izvjestaj(self, iznosi):
        open("izvjestaj.txt", "w").write(str(iznosi))

    def posalji_mail(self, iznosi):
        print("Poslato:", sum(iznosi))
