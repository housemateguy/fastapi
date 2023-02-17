import unittest
from app.api.models.commune import Commune
from app.api import app
from unittest.mock import patch
from typing import List

class TestHelpers(unittest.TestCase):

    def test_get_communes_by_department(self):
        # Test for valid department code and expected number of communes
        result = app.get_communes_by_department('69', 5, 0)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 5)

        # Test for invalid department code
        result = app.get_communes_by_department('invalid', 5, 0)
        self.assertIsNone(result)

    def test_load_data(self):
        # Test for loading data from local file path
        result = app.load_data("indicateurs-loyers-appartements.csv")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        # Test for loading data from URL
        result = app.load_data("https://static.data.gouv.fr/resources/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018/20201203-114600/indicateurs-loyers-appartements.csv")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_average_rent_in_commune_with_max(self):
        # Test for valid city name, surface area, and max rent
        result = app.get_average_rent_in_commune_with_max('Lyon', 50, 20.0)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0.0)

        # Test for invalid city name
        result = app.get_average_rent_in_commune_with_max('Invalid City', 50, 20.0)
        self.assertIsNone(result)

    def test_get_city_rating(self):
        # Test for valid city and postal code
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = """
                <html>
                    <body>
                        <main>
                            <section>
                                <div>4.5</div>
                            </section>
                        </main>
                    </body>
                </html>
            """
            result = app.get_city_rating('Lyon', '69001')
            self.assertIsInstance(result, int)
            self.assertGreaterEqual(result, 0)

        # Test for invalid city name
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            result = app.get_city_rating('Invalid City', '00000')
            self.assertEqual(result, 0)

    def test_get_cities_helper(self):
        # Test for valid department code, surface area, and max rent
        result = app.get_cities_helper('69', 50, 20.0, 5, 0)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 5)

        # Test for invalid department code
        result = app.get_cities_helper('invalid', 50, 20.0, 5, 0)
        self.assertEqual(result, [])
