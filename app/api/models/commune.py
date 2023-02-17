from pydantic import BaseModel

class Commune(BaseModel):
    name: str
    population: int
    code_region: str
    code_departement: str
    siren: str
    code_epci: str
    codes_postaux: str
    rating: float
    average_rent: float