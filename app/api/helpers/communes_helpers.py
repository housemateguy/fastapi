import requests
from typing import List, Optional
from app.api.models.commune import Commune
from lxml import html

GEO_FRENCH_GOV_API_URL = 'https://geo.api.gouv.fr'
FRENCH_GOV_API_URL = 'https://api.gouv.fr'


def get_communes_by_department(departement: str) -> Optional[Commune]:
    """
    @param departement: code of the department
    @return: a list of communes"""
    url = GEO_FRENCH_GOV_API_URL + \
        f'/departements/{departement}/communes?fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=json&geometry=centre'
    response = requests.get(url)
    data = response.json()
    communes_list = []
    print(data)
    for commune in data:
        name = commune['nom']
        population = commune['population']
        code_region = commune['codeRegion']
        code_departement = commune['codeDepartement']
        siren = commune['siren']
        code_epci = commune['codeEpci']
        codes_postaux = ",".join(commune['codesPostaux'])
        communes_list.append(Commune(name=name, population=population, code_region=code_region, code_departement=code_departement,
                             siren=siren, code_epci=code_epci, codes_postaux=codes_postaux, rating=0, average_rent=0))
    return communes_list


def get_average_rent_in_commune(city_name: str, surface_area: int) -> Optional[float]:
    """
    Get the average rent for a given surface area in a commune.
    @param city_name: The name of the commune.
    @param surface_area: The surface area of the property.
    @return: The average rent for the given surface area in the commune.
    """
    url = GEO_FRENCH_GOV_API_URL + \
        f'/les-indicateurs-de-loyers/carto-indicateurs-de-loyers-dannonce-par-commune-en-2018/api/indicateurs/v1/communes?nomCommune={city_name}&surface={surface_area}&champ=loyerMoyen'
    response = requests.get(url)
    print(response)
    data = response.json()
    if len(data) > 0:
        return data[0]['loyerMoyen']
    else:
        return None


def get_average_rent_in_commune_with_max(city_name: str, surface_area: int, max_rent: float) -> Optional[float]:
    """
    Get the average rent for a given surface area and maximum rent in a commune.
    @param city_name: The name of the commune.
    @param surface_area: The surface area of the property.
    @param max_rent: The maximum rent for the property.
    @return: The average rent for the given surface area in the commune below the given maximum rent.
    """
    url = FRENCH_GOV_API_URL + \
        f'/les-indicateurs-de-loyers/carto-indicateurs-de-loyers-dannonce-par-commune-en-2018/api/indicateurs/v1/communes?nomCommune={city_name}&surface={surface_area}&loyerMax={max_rent}&champ=loyerMoyen'
    response = requests.get(url)
    data = response.json()
    print (data)
    if len(data) > 0:
        return data[0]['loyerMoyen']
    else:
        return None


def get_city_rating(city, postal_code):
    url = f"https://www.bien-dans-ma-ville.fr/{city.lower()}-{postal_code}/avis.html"
    response = requests.get(url)
    response.raise_for_status()
    doc = html.fromstring(response.content)
    element = doc.find('/html/body/main/section[2]/div/div[@class="total"]')
    if element is not None:
        return element.text_content()
    else:
        raise ValueError("Element not found")


def get_cities_helper(department: str, surface: float, rent_max: float) -> List[Commune]:
    """
    Get cities that match the filters.
    @param department: The department code.
    @param surface: The desired surface area for the property.
    @param rent_max: The maximum rent for the property.
    @return: A list of cities that match the filters.
    """
    cities = []
    communes = get_communes_by_department(department)
    for commune in communes:
        avg_rent = get_average_rent_in_commune_with_max(
            commune.name, surface, rent_max)
        if avg_rent is not None:
            rating = get_city_rating(commune.name, commune.codes_postaux[0])
            cities.append(Commune(name=commune.name, population=commune.population, code_region=commune.code_region, code_departement=commune.code_departement,
                          siren=commune.siren, code_epci=commune.code_epci, codes_postaux=commune.codes_postaux, rating=rating, average_rent=avg_rent))
    return cities
