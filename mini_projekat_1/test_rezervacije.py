import json

import pytest

from rezervacije import (
    CsvIzvor,
    FajlIzvjestilac,
    JsonIzvor,
    Rezervacija,
    ServisRezervacija,
    izracunaj_iznos,
)


class LazniIzvor:
    """Zamjenski izvor podataka: vraća rezervacije iz memorije."""

    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self._rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self._rezervacije


class LazniIzvjestilac:
    """Zamjenski izvještilac: pamti šta bi bilo poslato."""

    def __init__(self) -> None:
        self.primljeno: list[list[float]] = []

    def posalji(self, iznosi: list[float]) -> None:
        self.primljeno.append(iznosi)


def test_servis_racuna_iznose_sa_laznim_izvorom():
    izvor = LazniIzvor([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 5, 65)])
    servis = ServisRezervacija(izvor, [])

    assert servis.obradi() == [240, 325]


def test_servis_salje_iznose_svim_izvjestiocima():
    izvor = LazniIzvor([Rezervacija("Ivana", 2, 120)])
    prvi, drugi = LazniIzvjestilac(), LazniIzvjestilac()

    ServisRezervacija(izvor, [prvi, drugi]).obradi()

    assert prvi.primljeno == [[240]]
    assert drugi.primljeno == [[240]]


def test_servis_sa_praznim_izvorom_vraca_praznu_listu():
    izvjestilac = LazniIzvjestilac()

    rezultat = ServisRezervacija(LazniIzvor([]), [izvjestilac]).obradi()

    assert rezultat == []
    assert izvjestilac.primljeno == [[]]


def test_negativan_broj_nocenja_baca_gresku():
    with pytest.raises(ValueError):
        izracunaj_iznos(Rezervacija("Ana", -1, 80))


def test_csv_izvor_cita_rezervacije(tmp_path):
    datoteka = tmp_path / "r.csv"
    datoteka.write_text("gost,noci,cijena_noci\nAna,2,100\nMarko,2,50\n")

    rezervacije = CsvIzvor(datoteka).ucitaj()

    assert rezervacije == [Rezervacija("Ana", 2, 100), Rezervacija("Marko", 2, 50)]


def test_json_izvor_radi_bez_izmjene_servisa(tmp_path):
    datoteka = tmp_path / "r.json"
    datoteka.write_text(json.dumps([{"gost": "Ana", "noci": 2, "cijena_noci": 100}]))

    assert ServisRezervacija(JsonIzvor(datoteka), []).obradi() == [200]


def test_fajl_izvjestilac_upisuje_iznose(tmp_path):
    izvjestaj = tmp_path / "izvjestaj.txt"

    FajlIzvjestilac(izvjestaj).posalji([240.0, 325.0])

    assert izvjestaj.read_text(encoding="utf-8") == "[240.0, 325.0]"
