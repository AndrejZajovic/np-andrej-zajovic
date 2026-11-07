# Mini projekat 1: refaktoring obrade rezervacija

Polazna tačka je monolitna klasa `UpravljanjeRezervacijama` (`monolit_original.py`)
koja istovremeno učitava podatke, računa iznos, čuva izvještaj i šalje poruku.
Refaktorisano rješenje je u `rezervacije.py`.

## Pokretanje

```bash
cd mini_projekat_1
pip install -r requirements.txt
ruff check .
pytest
python rezervacije.py
```

## Dizajn

| Princip | Kako je primijenjen |
| --- | --- |
| S (jedna odgovornost) | Svaka klasa ima jedan razlog za promjenu: `CsvIzvor` učitava, `izracunaj_iznos` računa, `FajlIzvjestilac` i `KonzolniIzvjestilac` izvještavaju, `ServisRezervacija` koordinira. |
| D (inverzija zavisnosti) | `ServisRezervacija` prima `IzvorRezervacija` i `Izvjestilac` (oba `Protocol`) kroz konstruktor i ne zna za konkretne klase. |
| O (otvoreno/zatvoreno) | Dodat je `JsonIzvor` bez ijedne izmjene u servisu. |

## Testovi

`test_rezervacije.py` ima 7 testova. Servis se testira sa zamjenskim izvorom
(`LazniIzvor`) i zamjenskim izvještiocem (`LazniIzvjestilac`), bez stvarnih
datoteka. Datoteke se koriste samo za testove konkretnih klasa (`tmp_path`).

## Upotrijebljeni upiti

Za izradu sam koristio AI asistenta (Claude). Priložio sam prezentacije
"Nedjelja 01" i "Nedjelja 02" i bilježnicu sa vježbama, pa sam poslao upite:

1. "Mini projekat 1 je da uradiš ovako. Ne znam da li on traži neki fajl, da li
   je to što sam ti poslao?"
2. "Zadatak iz prve nedjelje je već poslat, sad moramo da radimo taj mini
   projekat 1. Pošalji mi ga."

Iz zadatka na slajdu 20 proizlazi da se refaktoriše monolitna klasa sa slajda 17
(principi S i D, `Protocol` za izvor podataka i izvještavanje, najmanje tri testa
sa zamjenskim izvorom podataka).

## Ispravke i uočeni nedostaci generisanog koda

Razlike u odnosu na polazni (monolitni) kod:

- Polazni kod čita CSV bez zaglavlja i pristupa kolonama po indeksu
  (`r[1]`, `r[2]`). Refaktorisana verzija koristi zaglavlje
  (`gost,noci,cijena_noci`) i `csv.DictReader`, isto kao u vježbi iz prve nedjelje.
- Polazni `open(...)` ne zatvara datoteku i ne zadaje kodiranje. Sada se koristi
  `Path.open` / `read_text` sa `encoding="utf-8"`.
- `posalji_mail` je samo ispisivao poruku, pa je zamijenjen klasom
  `KonzolniIzvjestilac`. Stvarno slanje maila nije implementirano.
- `monolit_original.py` je isključen iz `ruff` provjere (u `pyproject.toml`),
  jer namjerno sadrži loš stil (npr. promjenljivu `l`) i služi samo za poređenje.

Uočeni nedostaci koji su ostali:

- Neispravan CSV ili JSON (nedostaje kolona, tekst umjesto broja) izaziva
  `KeyError` ili `ValueError` bez jasne poruke; izvori ne hvataju te greške.
- `FajlIzvjestilac` upisuje običnu listu (`str(iznosi)`), bez imena gostiju i
  bez čitljivog formata.
- Provjera ulaza postoji samo za negativne vrijednosti u `izracunaj_iznos`;
  nema provjere praznog imena gosta ni nerealnih vrijednosti.
- Testovi ne pokrivaju neispravne datoteke ni slučaj kad izvor baci grešku.
- `ServisRezervacija.obradi()` u jednoj metodi učitava, računa i izvještava;
  za veći sistem bi obračun mogao biti zaseban objekat.
