# np-andrej-zajovic

Vježba: korišćenje AI asistenta za implementaciju funkcije `prosjecna_ocjena`,
uz Python 3.12, VS Code, Ruff i pytest.

## Podešavanje

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

## Pokretanje

```bash
ruff check .
ruff format .
pytest
```

## Funkcija

`prosjecna_ocjena(ocjene)` u fajlu `ocjene.py` vraća aritmetičku sredinu liste
ocjena. Za praznu listu baca `ValueError`.

## Testovi

Fajl `test_ocjene.py`:

```python
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
```

## Upotrijebljeni upit

> Napiši Python 3.12 funkciju `prosjecna_ocjena(ocjene)` koja prima listu
> ocjena i vraća prosjek. Dodaj type hintove i docstring na srpskom/crnogorskom.
> Napiši i pytest testove.

## Uočeni nedostaci generisanog koda

- Ne provjerava tip elemenata: lista stringova izaziva `TypeError` bez jasne poruke.
- Ne provjerava opseg ocjena (npr. 1–5): prihvata se i -3 ili 100.
- `bool` vrijednosti (`True`/`False`) tretiraju se kao brojevi.
- Rezultat nije zaokružen, pa može imati mnogo decimala.
- Testovi ne pokrivaju granične slučajeve (negativne vrijednosti, `None`, pogrešne tipove).
- Funkcija prima samo listu; ne radi sa generatorima ni drugim iterabilnim tipovima.
