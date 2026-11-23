"""Poslovna logika obračuna cijene (bez zavisnosti od FastAPI-ja)."""

MIN_NOCI = 1
MAX_NOCI = 30
MAX_CIJENA_NOCI = 100_000.0


def izracunaj_iznos(noci: int, cijena_noci: float, popust: float = 0.0) -> float:
    """Ukupan iznos smještaja umanjen za popust (0.0 do 1.0), zaokružen na 2 decimale."""
    if not MIN_NOCI <= noci <= MAX_NOCI:
        raise ValueError(f"Broj noćenja mora biti od {MIN_NOCI} do {MAX_NOCI}")
    if not 0 < cijena_noci <= MAX_CIJENA_NOCI:
        raise ValueError(f"Cijena noćenja mora biti veća od 0 i najviše {MAX_CIJENA_NOCI}")
    if not 0.0 <= popust <= 1.0:
        raise ValueError("Popust mora biti u intervalu [0, 1]")
    return round(noci * cijena_noci * (1 - popust), 2)
