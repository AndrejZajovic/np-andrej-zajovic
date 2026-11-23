# Mini projekat 3: testiran i obezbijeđen API

Predmet: Napredno programiranje (FIST4NP), Univerzitet Donja Gorica
Autor: Andrej Zajović

FastAPI servis za obračun cijene hotelskog smještaja sa dva endpointa, pytest testovima, CI-em u GitHub Actions i bezbjednosnim pregledom.

## Endpointi

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/health` | Provjera statusa, vraća `{"status": "ok"}` |
| POST | `/cijena` | Računa iznos: `noci * cijena_noci * (1 - popust)`, zaokruženo na 2 decimale |

Primjer zahtjeva:

```bash
curl -X POST http://127.0.0.1:8000/cijena \
  -H "Content-Type: application/json" \
  -d '{"noci": 3, "cijena_noci": 80, "popust": 0.1}'
# {"iznos":216.0}
```

Ograničenja ulaza (validira Pydantic, neispravan unos vraća HTTP 422): `noci` od 1 do 30, `cijena_noci` veća od 0 i najviše 100 000, `popust` od 0 do 1.

## Struktura

```
mini_projekat_3/
├── src/
│   ├── cijene.py        # poslovna logika (bez FastAPI-ja)
│   └── main.py          # FastAPI aplikacija
├── tests/
│   ├── test_cijene.py   # unit testovi logike
│   └── test_api.py      # testovi API-ja preko TestClient-a
├── Dockerfile
├── pyproject.toml       # ruff i mypy podešavanja
├── pytest.ini
├── requirements.txt     # zavisnosti servisa
└── requirements-dev.txt # alati za testiranje, kvalitet i bezbjednost
```

CI workflow se nalazi u korijenu repozitorijuma: `.github/workflows/mini_projekat_3.yml` (GitHub čita workflow samo odatle).

## Pokretanje

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

uvicorn src.main:app --reload    # Swagger: http://127.0.0.1:8000/docs
```

Docker:

```bash
docker build -t rezervacije-api .
docker run -p 8000:8000 rezervacije-api
```

## Testovi i provjere kvaliteta

```bash
pytest --cov=src --cov-report=term-missing
ruff check .
mypy src/
bandit -r src/
pip-audit -r requirements.txt
```

Testovi pokrivaju uobičajene vrijednosti, granične vrijednosti (1 i 30 noćenja, popust 0 i 1), neispravne unose (HTTP 422: van opsega, nedostajuće polje, pogrešan tip, prazno tijelo), pogrešnu metodu (405), nepoznatu putanju (404) i dostupnost Swagger dokumentacije.

## Kontinuirana integracija

Workflow se pokreće na svaki `push` i `pull_request` i izvršava redom: `ruff check`, `mypy`, `pytest --cov`, `bandit` i `pip-audit`. Neuspjeh bilo kog koraka označava izmjenu kao neispravnu.

## Bezbjednosni pregled

Rezultati alata _(dopuniti nakon lokalnog pokretanja)_:

- `bandit -r src/`: _(zalijepiti sažetak, npr. broj nalaza po ozbiljnosti)_
- `pip-audit -r requirements.txt`: _(zalijepiti rezultat; ako ima nalaza, navesti ispravku ili obrazloženje)_

### Rizici i mjere

| Rizik | Mjera | Status |
| --- | --- | --- |
| Neispravan ili zlonamjeran unos (negativne ili ogromne vrijednosti, pogrešni tipovi) | Pydantic ograničenja na svakom polju, dodatna provjera u `izracunaj_iznos`, testovi za 422 | Implementirano |
| Tajne u kodu ili repozitorijumu | U kodu nema ključeva ni lozinki, `.env` je u `.gitignore`, `bandit` u CI-u. Za buduće tajne koristiti varijable okruženja | Implementirano |
| Ranjive zavisnosti | `pip-audit` u CI-u, ograničeni opsezi verzija u `requirements.txt` | Implementirano |
| Kontejner pokrenut kao root | `Dockerfile` pokreće aplikaciju kao običan korisnik `appuser` | Implementirano |
| Endpointi bez autentikacije | Za produkciju uvesti API ključ ili OAuth2, ključ čuvati u varijabli okruženja | Preporuka, nije implementirano |
| Zloupotreba i preopterećenje (veliki broj zahtjeva) | Ograničenje broja zahtjeva na API gateway-u ili reverse proxy-ju | Preporuka, nije implementirano |


- **Alat:** Claude (Anthropic).
- **Šta je AI radio:** na osnovu zadatka i slajdova iz nedjelja 5 i 6 napisao je nacrt koda, testova, CI workflow-a i ovog README-a.
- **Šta sam ja provjerio:** _(npr. pokrenuo sve testove, ruff, mypy, bandit i pip-audit lokalno, provjerio da CI prolazi na GitHubu)_.
- **Namjerno pokvaren kod:** _(npr. promijenio sam granicu popusta i provjerio da test pada)_.
- **Šta je AI predložio, a ja sam izmijenio ili odbacio:** _(ako ima)_.
- **Primjeri prompta:** _(zalijepiti 1-2 stvarna prompta)_.
