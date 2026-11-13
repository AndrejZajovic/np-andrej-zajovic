import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from ml_okvir.modeli import MODELI, dostupni_modeli, kreiraj_model, registruj_model


@pytest.mark.parametrize("naziv, ocekivana_klasa", [
    ("linearni", LogisticRegression),
    ("stablo", DecisionTreeClassifier),
    ("knn", KNeighborsClassifier),
])
def test_factory_kreira_pravi_tip_modela(naziv, ocekivana_klasa):
    assert isinstance(kreiraj_model(naziv), ocekivana_klasa)


def test_factory_nepoznat_model_podize_gresku():
    with pytest.raises(ValueError, match="Nepoznat model"):
        kreiraj_model("nepostojeci")


def test_factory_prosljedjuje_parametre():
    model = kreiraj_model("knn", n_neighbors=7)
    assert model.n_neighbors == 7


def test_factory_se_prosiruje_bez_izmjene_fabrike():
    @registruj_model("probni")
    class Probni:
        def __init__(self):
            self.ok = True

    try:
        assert "probni" in dostupni_modeli()
        assert kreiraj_model("probni").ok is True
    finally:
        MODELI.pop("probni")
