"""Strategy: zamjenjive metrike iza istog interfejsa (izracunaj)."""
from abc import ABC, abstractmethod


def _provjeri(y_tacno, y_pred) -> None:
    if len(y_tacno) != len(y_pred):
        raise ValueError("y_tacno i y_pred moraju imati istu dužinu")
    if len(y_tacno) == 0:
        raise ValueError("Nema podataka za izračunavanje metrike")


def _brojaci(y_tacno, y_pred, klasa):
    tp = sum(1 for a, p in zip(y_tacno, y_pred) if a == klasa and p == klasa)
    fp = sum(1 for a, p in zip(y_tacno, y_pred) if a != klasa and p == klasa)
    fn = sum(1 for a, p in zip(y_tacno, y_pred) if a == klasa and p != klasa)
    return tp, fp, fn


class Metrika(ABC):
    """Zajednički interfejs svih strategija."""

    @abstractmethod
    def izracunaj(self, y_tacno, y_pred) -> float: ...


class Tacnost(Metrika):
    def izracunaj(self, y_tacno, y_pred) -> float:
        _provjeri(y_tacno, y_pred)
        tacno = sum(1 for a, p in zip(y_tacno, y_pred) if a == p)
        return tacno / len(y_tacno)


class MakroPreciznost(Metrika):
    def izracunaj(self, y_tacno, y_pred) -> float:
        _provjeri(y_tacno, y_pred)
        klase = sorted(set(y_tacno) | set(y_pred))
        vrijednosti = []
        for k in klase:
            tp, fp, _ = _brojaci(y_tacno, y_pred, k)
            vrijednosti.append(tp / (tp + fp) if tp + fp else 0.0)
        return sum(vrijednosti) / len(vrijednosti)


class MakroF1(Metrika):
    def izracunaj(self, y_tacno, y_pred) -> float:
        _provjeri(y_tacno, y_pred)
        klase = sorted(set(y_tacno) | set(y_pred))
        vrijednosti = []
        for k in klase:
            tp, fp, fn = _brojaci(y_tacno, y_pred, k)
            imenilac = 2 * tp + fp + fn
            vrijednosti.append(2 * tp / imenilac if imenilac else 0.0)
        return sum(vrijednosti) / len(vrijednosti)


METRIKE: dict[str, Metrika] = {
    "tacnost": Tacnost(),
    "preciznost_makro": MakroPreciznost(),
    "f1_makro": MakroF1(),
}


def dohvati_metriku(naziv: str) -> Metrika:
    if naziv not in METRIKE:
        raise ValueError(f"Nepoznata metrika: {naziv}")
    return METRIKE[naziv]


def evaluiraj(y_tacno, y_pred, metrika: str = "tacnost") -> float:
    return dohvati_metriku(metrika).izracunaj(y_tacno, y_pred)
