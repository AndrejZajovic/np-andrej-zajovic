"""Template Method: fiksan tok eksperimenta, koraci se prilagođavaju u podklasama."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sklearn.datasets import load_iris, make_classification
from sklearn.model_selection import train_test_split

from .dekoratori import mjeri_vrijeme
from .metrike import dohvati_metriku
from .modeli import kreiraj_model
from .posmatraci import Subjekt


@dataclass
class Podaci:
    X_train: list
    X_test: list
    y_train: list
    y_test: list


class Eksperiment(Subjekt, ABC):
    """Okvir: ucitaj -> pripremi -> treniraj -> evaluiraj (metoda pokreni)."""

    def __init__(self, model: str, metrike=("tacnost", "f1_makro"),
                 test_udio: float = 0.3, seed: int = 42, **parametri_modela):
        super().__init__()
        self.model_naziv = model
        self.model = kreiraj_model(model, **parametri_modela)  # greška odmah
        self.metrike = {naziv: dohvati_metriku(naziv) for naziv in metrike}
        self.test_udio = test_udio
        self.seed = seed
        self.vremena: dict[str, float] = {}

    # --- šablonska metoda: redoslijed koraka je fiksan -----------------
    def pokreni(self) -> dict[str, float]:
        self._objavi("pocetak", model=self.model_naziv)
        X, y = self.ucitaj()
        podaci = self.pripremi(X, y)
        self.treniraj(podaci)
        self._objavi("kraj_treninga",
                     trajanje=round(self.vremena.get("treniraj", 0.0), 6))
        rezultati = self.evaluiraj(podaci)
        self._objavi("kraj", rezultati={k: round(v, 3) for k, v in rezultati.items()})
        return rezultati

    # --- koraci koje podklase prepisuju ---------------------------------
    @abstractmethod
    def ucitaj(self):
        """Vraća (X, y)."""

    def pripremi(self, X, y) -> Podaci:
        """Podrazumijevano: stratifikovana podjela na trening i test."""
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=self.test_udio, random_state=self.seed, stratify=y)
        return Podaci(X_tr, X_te, y_tr, y_te)

    @mjeri_vrijeme
    def treniraj(self, podaci: Podaci):
        self.model.fit(podaci.X_train, podaci.y_train)
        return self.model

    def evaluiraj(self, podaci: Podaci) -> dict[str, float]:
        y_pred = list(self.model.predict(podaci.X_test))
        y_tacno = list(podaci.y_test)
        return {naziv: metrika.izracunaj(y_tacno, y_pred)
                for naziv, metrika in self.metrike.items()}


class IrisEksperiment(Eksperiment):
    def ucitaj(self):
        X, y = load_iris(return_X_y=True)
        return X, y


class SintetickiEksperiment(Eksperiment):
    """Drugi konkretan eksperiment: isti okvir, drugi izvor podataka."""

    def __init__(self, model: str, n_uzoraka: int = 300, **kwargs):
        super().__init__(model, **kwargs)
        self.n_uzoraka = n_uzoraka

    def ucitaj(self):
        return make_classification(n_samples=self.n_uzoraka, n_features=6,
                                   n_informative=4, n_classes=3,
                                   random_state=self.seed)
