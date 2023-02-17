def commune_serializer(commune):
    return {
        'name': commune.name,
        'rating': commune.rating,
        'average_rent': commune.average_rent,
    }