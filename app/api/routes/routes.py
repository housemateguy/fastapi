from typing import List
from app.api.helpers.communes_helpers import get_cities_helper
from app.api.models.commune import Commune
from app.api.models.filters import Filters
from app.api.serializers.commune import commune_serializer
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/municipalities")
def get_cities( 
    department: str = Query(...),
    rent: int = Query(..., gt=0, lt=100000000000),
    surface: int = Query(..., gt=0, lt=2000000000),
    limit: int = Query(10, gt=0, lt=1000),
    page: int = Query(1, gt=0, lt=100000),
):
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
    max_limit = 1000
    max_page = 100000
    if limit is None:
        limit = 10
    if page is None:
        page = 1
    if limit > max_limit:
        raise HTTPException(status_code=400, detail="Limit parameter exceeds maximum value.")
    if page > max_page:
        raise HTTPException(status_code=400, detail="Page parameter exceeds maximum value.")
    offset = (page - 1) * limit
    limit = min(limit, max_limit - offset)
    cities = get_cities_helper(department, surface, rent, limit=limit, offset=offset)
    response = []
    for city in cities:
        response.append(commune_serializer(city))
    return {
        "success": True,
        "data": response,
    }
    
@router.get("/helloworld")
def hello_world():
    return {
        "success": True,
        "data": "Hello World!",
    }    



