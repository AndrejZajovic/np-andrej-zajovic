"""FastAPI servis za obračun cijene hotelskog smještaja."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.cijene import MAX_CIJENA_NOCI, MAX_NOCI, MIN_NOCI, izracunaj_iznos

app = FastAPI(
    title="Hotelske rezervacije API",
    description="API za izračunavanje cijene hotelskog smještaja",
    version="1.0.0",
)


class ZahtjevCijene(BaseModel):
    noci: int = Field(ge=MIN_NOCI, le=MAX_NOCI, description="Broj noćenja (1 do 30)")
    cijena_noci: float = Field(
        gt=0, le=MAX_CIJENA_NOCI, description="Cijena jednog noćenja u EUR"
    )
    popust: float = Field(default=0.0, ge=0, le=1, description="Popust od 0 do 1")


class OdgovorCijene(BaseModel):
    iznos: float


@app.get("/health", tags=["Sistem"], summary="Provjera statusa API-ja")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/cijena",
    response_model=OdgovorCijene,
    tags=["Rezervacije"],
    summary="Izračunaj cijenu smještaja",
)
def izracunaj(z: ZahtjevCijene) -> OdgovorCijene:
    return OdgovorCijene(iznos=izracunaj_iznos(z.noci, z.cijena_noci, z.popust))
