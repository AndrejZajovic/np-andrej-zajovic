"""Obrada rezervacija: refaktorisana verzija monolitne klase.

Odgovornosti su razdvojene (princip S):
    - model podataka:  Rezervacija
    - obračun iznosa:  izracunaj_iznos
    - učitavanje:      CsvIzvor, JsonIzvor
    - izvještavanje:   FajlIzvjestilac, KonzolniIzvjestilac
    - koordinacija:    ServisRezervacija

Servis zavisi samo od apstrakcija (Protocol), a ne od konkretnih klasa
(princip D), pa se izvor ili izvještaj mogu zamijeniti bez izmjene servisa
(princip O).
"""

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Rezervacija:
    """Jedna rezervacija: gost, broj noćenja i cijena po noćenju."""

    gost: str
    noci: int
    cijena_noci: float


class IzvorRezervacija(Protocol):
    """Ugovor za svaki izvor podataka o rezervacijama."""

    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestilac(Protocol):
    """Ugovor za svaki način izvještavanja o iznosima."""

    def posalji(self, iznosi: list[float]) -> None: ...


def izracunaj_iznos(rezervacija: Rezervacija) -> float:
    """Vraća iznos rezervacije (noćenja puta cijena noćenja).

    Raises:
        ValueError: ako je broj noćenja ili cijena negativna.
    """
    if rezervacija.noci < 0 or rezervacija.cijena_noci < 0:
        raise ValueError("Noćenja i cijena ne smiju biti negativni.")
    return rezervacija.noci * rezervacija.cijena_noci


class CsvIzvor:
    """Učitava rezervacije iz CSV datoteke (gost,noci,cijena_noci)."""

    def __init__(self, putanja: Path) -> None:
        self._putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self._putanja.open(newline="", encoding="utf-8") as f:
            return [
                Rezervacija(red["gost"], int(red["noci"]), float(red["cijena_noci"]))
                for red in csv.DictReader(f)
            ]


class JsonIzvor:
    """Drugi izvor podataka: lista rezervacija u JSON datoteci."""

    def __init__(self, putanja: Path) -> None:
        self._putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        podaci = json.loads(self._putanja.read_text(encoding="utf-8"))
        return [
            Rezervacija(p["gost"], int(p["noci"]), float(p["cijena_noci"]))
            for p in podaci
        ]


class FajlIzvjestilac:
    """Upisuje iznose u tekstualnu datoteku."""

    def __init__(self, putanja: Path) -> None:
        self._putanja = putanja

    def posalji(self, iznosi: list[float]) -> None:
        self._putanja.write_text(str(iznosi), encoding="utf-8")


class KonzolniIzvjestilac:
    """Ispisuje ukupan iznos na ekran (zamjena za slanje maila)."""

    def posalji(self, iznosi: list[float]) -> None:
        print("Poslato:", sum(iznosi))


class ServisRezervacija:
    """Koordinira obradu: učitava, računa iznose i šalje izvještaje."""

    def __init__(
        self, izvor: IzvorRezervacija, izvjestioci: list[Izvjestilac]
    ) -> None:
        self._izvor = izvor
        self._izvjestioci = izvjestioci

    def obradi(self) -> list[float]:
        iznosi = [izracunaj_iznos(r) for r in self._izvor.ucitaj()]
        for izvjestilac in self._izvjestioci:
            izvjestilac.posalji(iznosi)
        return iznosi


if __name__ == "__main__":
    servis = ServisRezervacija(
        CsvIzvor(Path("rezervacije.csv")),
        [FajlIzvjestilac(Path("izvjestaj.txt")), KonzolniIzvjestilac()],
    )
    servis.obradi()
