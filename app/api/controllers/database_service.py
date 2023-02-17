from typing import List
import psycopg2
import os

from app.api.models.commune import Commune

class DatabaseService:
    def __init__(self, db_name=os.environ["DATABASE_name"],
                 db_user=os.environ['DATABASE_user'],
                 db_password=os.environ['DATABASE_password'],
                 db_host=os.environ['DATABASE_host'],
                 db_port=os.environ['DATABASE_port']):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

    def execute_query(self, query, params=()):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            self.conn.commit()
            return result

    def init_database(self):
        query = """
        CREATE TABLE IF NOT EXISTS communes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            population INTEGER NOT NULL,
            code_region VARCHAR(255) NOT NULL,
            code_departement VARCHAR(255) NOT NULL,
            siren VARCHAR(255) NOT NULL,
            code_epci VARCHAR(255) NOT NULL,
            codes_postaux VARCHAR(255) NOT NULL,
            rent_average FLOAT NOT NULL
            rating FLOAT NOT NULL

        );
        """
        self.execute_query(query)

    def get_communes(self, department: str, surface: float, rent_max: float) -> List[Commune]:
        query = """
        SELECT * FROM communes WHERE code_departement = %s AND surface_area = %s AND rent_average <= %s
        """
        self.execute_query(query, (department, surface, rent_max))
        results = self.cursor.fetchall()
        return [Commune(*row) for row in results]

    def save_commune(
        self,
        name: str,
        population: int,
        code_region: str,
        code_departement: str,
        siren: str,
        code_epci: str,
        codes_postaux: List[str],
        rent_average: float,
        rating: float,
    ):
        query = """
        INSERT INTO communes (name, population, code_region, code_departement, siren, code_epci, codes_postaux, rent_average, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        self.cur.execute(
            query,
            (
                name,
                population,
                code_region,
                code_departement,
                siren,
                code_epci,
                codes_postaux,
                rent_average,
                rating,
            ),
        )
        self.conn.commit()
