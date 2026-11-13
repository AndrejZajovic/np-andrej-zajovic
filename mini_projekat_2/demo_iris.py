"""Demonstracija: svi registrovani modeli na skupu iris."""
from ml_okvir import IspisPosmatrac, IrisEksperiment, dostupni_modeli


def main() -> None:
    print("Modeli:", ", ".join(dostupni_modeli()), "\n")
    tabela = {}
    for naziv in dostupni_modeli():
        eksperiment = IrisEksperiment(naziv, metrike=("tacnost", "f1_makro"))
        eksperiment.pretplati(IspisPosmatrac())     # Observer
        tabela[naziv] = eksperiment.pokreni()       # Template Method
        print()

    print(f"{'model':<10}{'tacnost':>10}{'f1_makro':>10}")
    for naziv, rez in tabela.items():
        print(f"{naziv:<10}{rez['tacnost']:>10.3f}{rez['f1_makro']:>10.3f}")


if __name__ == "__main__":
    main()
