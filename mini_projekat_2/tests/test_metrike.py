import pytest

from ml_okvir.metrike import (METRIKE, MakroF1, Tacnost, dohvati_metriku,
                              evaluiraj)

Y_TACNO = [0, 0, 1, 1, 2, 2]
Y_PRED = [0, 1, 1, 1, 2, 0]


def test_tacnost_na_poznatom_primjeru():
    assert Tacnost().izracunaj(Y_TACNO, Y_PRED) == pytest.approx(4 / 6)


def test_makro_f1_na_poznatom_primjeru():
    # klasa 0: tp=1 fp=1 fn=1 -> 0.5 ; klasa 1: tp=2 fp=1 fn=0 -> 0.8 ;
    # klasa 2: tp=1 fp=0 fn=1 -> 0.6667
    ocekivano = (0.5 + 0.8 + 2 / 3) / 3
    assert MakroF1().izracunaj(Y_TACNO, Y_PRED) == pytest.approx(ocekivano)


def test_savrsen_pogodak_daje_jedan_za_sve_metrike():
    for metrika in METRIKE.values():
        assert metrika.izracunaj(Y_TACNO, Y_TACNO) == pytest.approx(1.0)


def test_strategija_se_bira_po_nazivu():
    assert evaluiraj(Y_TACNO, Y_PRED, "tacnost") == pytest.approx(4 / 6)
    assert isinstance(dohvati_metriku("f1_makro"), MakroF1)


def test_nepoznata_metrika_podize_gresku():
    with pytest.raises(ValueError, match="Nepoznata metrika"):
        dohvati_metriku("xyz")


def test_razlicite_duzine_i_prazan_unos_podizu_gresku():
    with pytest.raises(ValueError):
        Tacnost().izracunaj([1, 2], [1])
    with pytest.raises(ValueError):
        Tacnost().izracunaj([], [])
