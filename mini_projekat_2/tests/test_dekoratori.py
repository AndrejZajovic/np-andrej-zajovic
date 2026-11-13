import time

from ml_okvir.dekoratori import mjeri_vrijeme


def test_dekorator_ne_mijenja_povratnu_vrijednost_ni_naziv():
    @mjeri_vrijeme
    def saberi(a, b):
        """Sabira."""
        return a + b

    assert saberi(2, 3) == 5
    assert saberi.__name__ == "saberi"
    assert saberi.__doc__ == "Sabira."


def test_dekorator_mjeri_trajanje():
    @mjeri_vrijeme
    def spor():
        time.sleep(0.02)

    assert spor.zadnje_trajanje is None
    spor()
    assert spor.zadnje_trajanje >= 0.02


def test_dekorator_upisuje_vrijeme_u_objekat():
    class Radnik:
        def __init__(self):
            self.vremena = {}

        @mjeri_vrijeme
        def radi(self):
            return "gotovo"

    r = Radnik()
    assert r.radi() == "gotovo"
    assert r.vremena["radi"] >= 0


def test_dekorator_biljezi_vrijeme_i_kad_funkcija_baci_gresku():
    @mjeri_vrijeme
    def kvar():
        raise RuntimeError("greska")

    try:
        kvar()
    except RuntimeError:
        pass
    assert kvar.zadnje_trajanje is not None
