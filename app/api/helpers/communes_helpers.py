import time
from bs4 import BeautifulSoup
import requests
from typing import List, Optional

import unidecode
from app.api.models.commune import Commune
from lxml import html
import os
import requests
import pandas as pd

GEO_FRENCH_GOV_API_URL = 'https://geo.api.gouv.fr'
FRENCH_GOV_API_URL = 'https://api.gouv.fr'


def get_communes_by_department(departement: str, limit, offset) -> Optional[Commune]:
    """
    @param departement: code of the department
    @return: a list of communes"""
    url = GEO_FRENCH_GOV_API_URL + \
        f'/departements/{departement}/communes?fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=json&geometry=centre'
    response = requests.get(url)
    data = response.json()
    communes_list = []
    for commune in data:
        name = commune['nom']
        population = commune['population']
        code_region = commune['codeRegion']
        code_departement = commune['codeDepartement']
        siren = commune['siren']
        code_epci = commune['codeEpci']
        codes_postaux = ",".join(commune['codesPostaux'])
        communes_list.append(Commune(name=name, population=population, code_region=code_region, code_departement=code_departement,
                             siren=siren, code_epci=code_epci, codes_postaux=codes_postaux, rating=0, average_rent=0, code=int(commune['code'])))
    return communes_list[offset:offset+limit]


def load_data(file_path="https://static.data.gouv.fr/resources/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018/20201203-114600/indicateurs-loyers-appartements.csv"):
    """
    Load the rental data from the specified CSV file.
    @param file_path: The URL or local file path of the CSV file to load.
    @return: A list of dictionaries representing the rows in the CSV file.
    """
    file = "indicateurs-loyers-appartements.csv"
    if file_path.startswith("http") and not os.path.exists(os.path.basename(file)):
        response = requests.get(file_path)
        file_name = os.path.basename(file_path)
        with open(file_name, "wb") as f:
            f.write(response.content)
        file_path = file_name
    # Load the CSV file into a list of dictionaries
    with open(file, "r", encoding='latin-1') as f:
        lines = f.readlines()
    headers = lines[0].strip().split(";")
    data = []
    for line in lines[1:]:
        values = line.strip().split(";")
        values = [v.replace(",", ".") for v in values]
        data.append(dict(zip(headers, values)))
    return data


def get_average_rent_in_commune_with_max(city_name: str, surface_area: int, max_rent: float) -> Optional[float]:
    """
    Get the average rent for a given surface area and maximum rent in a commune.
    @param city_name: The name of the commune.
    @param surface_area: The surface area of the property.
    @param max_rent: The maximum rent for the property.
    @return: The average rent for the given surface area in the commune below the given maximum rent.
    """
    # Load the data from the source into a pandas DataFrame
    data = pd.read_csv("indicateurs-loyers-appartements.csv",
                       sep=";", encoding='latin-1')
    # Filter the data by the given city name
    data = data[data['LIBGEO'] == city_name]
    # Sort the data by the requested fields in ascending order
    data = data.sort_values(by=['TYPPRED', 'loypredm2', 'NBobs_maille'])
    # Filter the data by the given maximum rent
    data = data[data['loypredm2'].apply(
        lambda x: float(x.replace(",", "."))) <= max_rent]
    # Filter the data by the given surface area
    data = data[data['NBobs_maille'] >= surface_area]
    # Return the average rent for the given surface area in the commune below the given maximum rent
    if not data.empty:
        return float(data.iloc[0]['loypredm2'].replace(",", "."))
    else:
        return None


def get_city_rating(city, postal_code):
    url = f"https://www.bien-dans-ma-ville.fr/{city.lower()}-{postal_code}/avis.html"
    print(url)
    response = None
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return 0
    except requests.exceptions.ConnectionError as e:
        print(e)
        time.sleep(5)  # wait for 5 seconds before retrying
        return get_city_rating(city, postal_code)  # recursive call to retry
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select_one('html > body > main > section:nth-of-type(2) > div > div > div')
    if element is not None:
        return float(element.text.split("/")[0])
    else:
        print("No rating found for", city)
        return 0

def get_cities_helper(department: str, surface: float, rent_max: float, limit: int, offset: int) -> List[Commune]:
    """
    Get cities that match the filters.
    @param department: The department code.
    @param surface: The desired surface area for the property.
    @param rent_max: The maximum rent for the property.
    @return: A list of cities that match the filters.
    """
    cities = []
    communes = get_communes_by_department(department, limit, offset)
    for commune in communes:
        avg_rent = get_average_rent_in_commune_with_max(
            commune.name, surface, rent_max)
        if avg_rent is not None:
            # remove accents from city name to make it compatible with the website
            rating = get_city_rating(unidecode.unidecode(commune.name).lower(), commune.code)
            # rating = 0
            cities.append(Commune(name=commune.name, population=commune.population, code_region=commune.code_region, code_departement=commune.code_departement,
                          siren=commune.siren, code_epci=commune.code_epci, codes_postaux=commune.codes_postaux, rating=rating, average_rent=avg_rent, code=commune.code))
    return cities
