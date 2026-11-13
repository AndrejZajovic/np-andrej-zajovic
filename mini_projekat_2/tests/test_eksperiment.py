import pytest

from ml_okvir.eksperiment import (Eksperiment, IrisEksperiment,
                                  SintetickiEksperiment)
from ml_okvir.posmatraci import BiljeznikDogadjaja


def test_template_method_poziva_korake_ovim_redoslijedom():
    pozivi = []

    class Probni(Eksperiment):
        def ucitaj(self):
            pozivi.append("ucitaj")
            return [[0], [1], [2], [3]] * 5, [0, 1, 0, 1] * 5

        def pripremi(self, X, y):
            pozivi.append("pripremi")
            return super().pripremi(X, y)

        def treniraj(self, podaci):
            pozivi.append("treniraj")
            return super().treniraj(podaci)

        def evaluiraj(self, podaci):
            pozivi.append("evaluiraj")
            return super().evaluiraj(podaci)

    Probni("stablo").pokreni()
    assert pozivi == ["ucitaj", "pripremi", "treniraj", "evaluiraj"]


def test_apstraktna_osnovna_klasa_se_ne_moze_instancirati():
    with pytest.raises(TypeError):
        Eksperiment("knn")


@pytest.mark.parametrize("model", ["linearni", "stablo", "knn"])
def test_iris_svi_modeli_daju_visoku_tacnost(model):
    rezultati = IrisEksperiment(model).pokreni()
    assert rezultati["tacnost"] > 0.85
    assert 0.0 <= rezultati["f1_makro"] <= 1.0


def test_isti_seed_daje_isti_rezultat():
    a = IrisEksperiment("stablo", seed=7).pokreni()
    b = IrisEksperiment("stablo", seed=7).pokreni()
    assert a == b


def test_posmatrac_dobija_dogadjaje_eksperimenta():
    eksperiment, biljeznik = IrisEksperiment("knn"), BiljeznikDogadjaja()
    eksperiment.pretplati(biljeznik)
    eksperiment.pokreni()
    assert biljeznik.nazivi() == ["pocetak", "kraj_treninga", "kraj"]


def test_vrijeme_treninga_je_izmjereno_dekoratorom():
    eksperiment = IrisEksperiment("linearni")
    eksperiment.pokreni()
    assert eksperiment.vremena["treniraj"] > 0


def test_nepoznat_model_ili_metrika_pada_odmah():
    with pytest.raises(ValueError):
        IrisEksperiment("nepostojeci")
    with pytest.raises(ValueError):
        IrisEksperiment("knn", metrike=("nepostojeca",))


def test_drugi_konkretan_eksperiment_koristi_isti_okvir():
    rezultati = SintetickiEksperiment("knn", n_uzoraka=200).pokreni()
    assert set(rezultati) == {"tacnost", "f1_makro"}
