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
    code: int

    def get_commune_by_code(self, code: int):
        query = """
        SELECT * FROM communes WHERE code = %s
        """
        self.execute_query(query, (code,))
        results = self.cursor.fetchall()
        return [Commune(*row) for row in results]
    