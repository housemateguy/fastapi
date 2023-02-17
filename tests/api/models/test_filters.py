from models.filters import Filters

def test_filters_model():
    filters_data = {
        "department": "64",
        "surface": 50,
        "max_rent": 800
    }
    filters = Filters(**filters_data)
    assert filters.department == "64"
    assert filters.surface == 50
    assert filters.max_rent == 800
