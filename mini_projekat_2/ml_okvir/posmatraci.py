"""Observer: praćenje događaja u toku eksperimenta."""
from abc import ABC, abstractmethod


class Posmatrac(ABC):
    """Interfejs pretplatnika: prima događaj i podatke o njemu."""

    @abstractmethod
    def obavijesti(self, dogadjaj: str, **podaci) -> None: ...


class Subjekt:
    """Čuva listu pretplatnika i objavljuje im događaje."""

    def __init__(self):
        self._posmatraci: list[Posmatrac] = []

    def pretplati(self, posmatrac: Posmatrac) -> None:
        if posmatrac not in self._posmatraci:
            self._posmatraci.append(posmatrac)

    def odjavi(self, posmatrac: Posmatrac) -> None:
        if posmatrac in self._posmatraci:
            self._posmatraci.remove(posmatrac)

    def _objavi(self, dogadjaj: str, **podaci) -> None:
        for posmatrac in list(self._posmatraci):
            posmatrac.obavijesti(dogadjaj, **podaci)


class IspisPosmatrac(Posmatrac):
    """Ispisuje svaki događaj (izlaz se može zamijeniti, npr. u testu)."""

    def __init__(self, izlaz=print):
        self.izlaz = izlaz

    def obavijesti(self, dogadjaj: str, **podaci) -> None:
        detalji = ", ".join(f"{k}={v}" for k, v in podaci.items())
        self.izlaz(f"[{dogadjaj}] {detalji}")


class BiljeznikDogadjaja(Posmatrac):
    """Pamti sve događaje, korisno za testove i kasniju analizu."""

    def __init__(self):
        self.dogadjaji: list[tuple[str, dict]] = []

    def obavijesti(self, dogadjaj: str, **podaci) -> None:
        self.dogadjaji.append((dogadjaj, podaci))

    def nazivi(self) -> list[str]:
        return [naziv for naziv, _ in self.dogadjaji]
