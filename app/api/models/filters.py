from pydantic import BaseModel

class Filters(BaseModel):
    """Filters used for search"""
    department: str
    surface: float
    rent_max: float