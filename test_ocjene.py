import pytest

from ocjene import prosjecna_ocjena


def test_prosjek_cijelih_brojeva():
    assert prosjecna_ocjena([5, 4, 3]) == pytest.approx(4.0)


def test_prosjek_decimalnih_brojeva():
    assert prosjecna_ocjena([4.5, 3.5]) == pytest.approx(4.0)


def test_jedna_ocjena():
    assert prosjecna_ocjena([5]) == 5


def test_prazna_lista_baca_gresku():
    with pytest.raises(ValueError):
        prosjecna_ocjena([])
