import pytest

from src.cijene import izracunaj_iznos


@pytest.mark.parametrize(
    "noci, cijena, popust, ocekivano",
    [
        (3, 80.0, 0.0, 240.0),
        (3, 80.0, 0.1, 216.0),
        (1, 100.0, 0.0, 100.0),
        (30, 50.0, 0.5, 750.0),
        (3, 80.0, 1.0, 0.0),
    ],
)
def test_iznos_ispravni_i_granicni_slucajevi(noci, cijena, popust, ocekivano):
    assert izracunaj_iznos(noci, cijena, popust) == pytest.approx(ocekivano)


def test_popust_je_podrazumijevano_nula():
    assert izracunaj_iznos(2, 50.0) == 100.0


def test_iznos_je_zaokruzen_na_dvije_decimale():
    assert izracunaj_iznos(3, 33.333, 0.0) == 100.0


@pytest.mark.parametrize(
    "noci, cijena, popust",
    [
        (0, 80.0, 0.0),
        (31, 80.0, 0.0),
        (-1, 80.0, 0.0),
        (3, 0.0, 0.0),
        (3, -5.0, 0.0),
        (3, 1_000_000.0, 0.0),
        (3, 80.0, -0.1),
        (3, 80.0, 1.5),
    ],
)
def test_neispravan_unos_podize_value_error(noci, cijena, popust):
    with pytest.raises(ValueError):
        izracunaj_iznos(noci, cijena, popust)
