import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def klijent() -> TestClient:
    return TestClient(app)


def test_health(klijent):
    r = klijent.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_cijena_bez_popusta(klijent):
    r = klijent.post("/cijena", json={"noci": 3, "cijena_noci": 80})
    assert r.status_code == 200
    assert r.json()["iznos"] == 240.0


def test_cijena_sa_popustom(klijent):
    r = klijent.post("/cijena", json={"noci": 3, "cijena_noci": 80, "popust": 0.1})
    assert r.status_code == 200
    assert r.json()["iznos"] == pytest.approx(216.0)


@pytest.mark.parametrize(
    "noci, cijena, popust, ocekivano",
    [(1, 100, 0, 100.0), (30, 50, 0.5, 750.0), (3, 80, 1, 0.0)],
)
def test_cijena_granicne_vrijednosti(klijent, noci, cijena, popust, ocekivano):
    r = klijent.post(
        "/cijena", json={"noci": noci, "cijena_noci": cijena, "popust": popust}
    )
    assert r.status_code == 200
    assert r.json()["iznos"] == pytest.approx(ocekivano)


@pytest.mark.parametrize(
    "tijelo",
    [
        {"noci": 0, "cijena_noci": 80},
        {"noci": 31, "cijena_noci": 80},
        {"noci": 3, "cijena_noci": 0},
        {"noci": 3, "cijena_noci": -10},
        {"noci": 3, "cijena_noci": 1_000_000},
        {"noci": 3, "cijena_noci": 80, "popust": 1.5},
        {"noci": 3, "cijena_noci": 80, "popust": -0.1},
    ],
)
def test_neispravan_unos_vraca_422(klijent, tijelo):
    assert klijent.post("/cijena", json=tijelo).status_code == 422


def test_nedostajuce_polje_vraca_422(klijent):
    assert klijent.post("/cijena", json={"noci": 3}).status_code == 422


def test_pogresan_tip_vraca_422(klijent):
    r = klijent.post("/cijena", json={"noci": "tri", "cijena_noci": 80})
    assert r.status_code == 422


def test_prazno_tijelo_vraca_422(klijent):
    assert klijent.post("/cijena").status_code == 422


def test_pogresna_metoda_vraca_405(klijent):
    assert klijent.get("/cijena").status_code == 405


def test_nepoznata_putanja_vraca_404(klijent):
    assert klijent.get("/nepostoji").status_code == 404


def test_swagger_dokumentacija_je_dostupna(klijent):
    assert klijent.get("/docs").status_code == 200
