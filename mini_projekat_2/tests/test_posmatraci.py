from ml_okvir.posmatraci import BiljeznikDogadjaja, IspisPosmatrac, Subjekt


def test_posmatrac_prima_dogadjaj_sa_podacima():
    subjekt, biljeznik = Subjekt(), BiljeznikDogadjaja()
    subjekt.pretplati(biljeznik)
    subjekt._objavi("test", vrijednost=3)
    assert biljeznik.dogadjaji == [("test", {"vrijednost": 3})]


def test_vise_pretplatnika_dobija_isti_dogadjaj():
    subjekt, a, b = Subjekt(), BiljeznikDogadjaja(), BiljeznikDogadjaja()
    subjekt.pretplati(a)
    subjekt.pretplati(b)
    subjekt._objavi("x")
    assert a.nazivi() == b.nazivi() == ["x"]


def test_odjavljen_posmatrac_ne_prima_dogadjaje():
    subjekt, biljeznik = Subjekt(), BiljeznikDogadjaja()
    subjekt.pretplati(biljeznik)
    subjekt.odjavi(biljeznik)
    subjekt._objavi("x")
    assert biljeznik.dogadjaji == []


def test_dupla_pretplata_ne_duplira_obavjestenja():
    subjekt, biljeznik = Subjekt(), BiljeznikDogadjaja()
    subjekt.pretplati(biljeznik)
    subjekt.pretplati(biljeznik)
    subjekt._objavi("x")
    assert len(biljeznik.dogadjaji) == 1


def test_ispis_posmatrac_formatira_poruku():
    linije = []
    subjekt = Subjekt()
    subjekt.pretplati(IspisPosmatrac(izlaz=linije.append))
    subjekt._objavi("kraj", tacnost=0.9)
    assert linije == ["[kraj] tacnost=0.9"]
