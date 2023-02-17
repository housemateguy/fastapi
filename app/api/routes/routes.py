from typing import List
from app.api.helpers.communes_helpers import get_cities_helper
from app.api.models.commune import Commune
from app.api.models.filters import Filters
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/cities", response_model=List[Commune])
def get_cities( 
    department: str = Query(...),
    rent: int = Query(..., gt=0, lt=10000),
    surface: int = Query(..., gt=0, lt=2000)):
    """
    Get cities that match the filters.
        @param department: Code of the department.
        @param surface: Desired surface area of the property.
        @param rent: Maximum rent for the property.
        @return: A list of cities that match the given filters, with the following properties:
        - average rent for the given surface area
        - city rating
        - city name
        - city postal code
        - city population
    """
    cities = get_cities_helper(department, surface, rent)
    return cities
    
    


