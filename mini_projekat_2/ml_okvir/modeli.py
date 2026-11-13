"""Factory: kreiranje modela prema nazivu (registar + funkcija kreiranja)."""
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

MODELI: dict[str, type] = {}


def registruj_model(naziv: str):
    """Dekorator: upisuje klasu modela u registar pod zadatim nazivom."""

    def dekorator(klasa):
        MODELI[naziv] = klasa
        return klasa

    return dekorator


# Postojeće scikit-learn klase registrujemo bez izmjene njihovog koda.
registruj_model("linearni")(LogisticRegression)
registruj_model("stablo")(DecisionTreeClassifier)
registruj_model("knn")(KNeighborsClassifier)

# Podrazumijevani parametri po modelu (mogu se prepisati pri kreiranju).
PODRAZUMIJEVANO: dict[str, dict] = {
    "linearni": {"max_iter": 1000},
    "stablo": {"random_state": 42},
    "knn": {"n_neighbors": 5},
}


def dostupni_modeli() -> list[str]:
    return sorted(MODELI)


def kreiraj_model(naziv: str, **parametri):
    """Kreira model prema nazivu; nepoznat naziv podiže ValueError."""
    if naziv not in MODELI:
        raise ValueError(
            f"Nepoznat model: {naziv}. Dostupni: {', '.join(dostupni_modeli())}"
        )
    postavke = {**PODRAZUMIJEVANO.get(naziv, {}), **parametri}
    return MODELI[naziv](**postavke)
