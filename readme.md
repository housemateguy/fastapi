French FastAPI Application
==========================

This is a French FastAPI application that allows users to retrieve data on French municipalities and their average apartment rental prices.

Requirements
------------

-   Docker
-   Docker Compose

Installation
------------

1.  Clone the repository:


```bash
git clone https://github.com/housemateguy/french-fastapi-app.git
```

1.  Navigate to the project directory:


```bash
cd french-fastapi-app
```

1.  Build the Docker image:


```bash
docker build -t french-fastapi-app 
```

1.  Start the application:


```bash
docker-compose up
```

The application should now be running at [http://localhost:8000](http://localhost:8000/).

API Endpoints
-------------

### `GET /municipalities`

This API endpoint allows you to retrieve a list of municipalities based on specified filters.

API URL
-------

```bash
http://localhost:8000/municipalities
```

Parameters
----------

| Parameter | Required | Description |
| --- | --- | --- |
| `department` | Yes | The department ID of the municipality |
| `rent` | Yes | The maximum monthly rent for the municipality |
| `surface` | Yes | The minimum surface area for the municipality |
| `limit` | No | The maximum number of results to return per page (default: 10) |
| `page` | No | The page number to return (default: 1) |

Example Request
---------------

```bash
GET http://localhost:8000/municipalities?department=64&rent=800&surface=50&limit=10&page=1
```

Example Response
----------------

```json
{
    "success": true,
    "data": [
        {
            "name": "Aast",
            "rating": 0.0,
            "average_rent": 8.051633453
        },
        {
            "name": "Abère",
            "rating": 0.0,
            "average_rent": 9.146075334
        },
        {
            "name": "Abidos",
            "rating": 0.0,
            "average_rent": 10.36230193
        },
        {
            "name": "Abitain",
            "rating": 0.0,
            "average_rent": 7.852653875
        },
        {
            "name": "Abos",
            "rating": 0.0,
            "average_rent": 10.36230193
        },
        {
            "name": "Accous",
            "rating": 0.0,
            "average_rent": 8.556396081
        },
        {
            "name": "Agnos",
            "rating": 0.0,
            "average_rent": 8.556396081
        },
        {
            "name": "Ahaxe-Alciette-Bascassan",
            "rating": 0.0,
            "average_rent": 8.016452223
        },
        {
            "name": "Ahetze",
            "rating": 3.6,
            "average_rent": 12.23298268
        },
        {
            "name": "Aïcirits-Camou-Suhast",
            "rating": 0.0,
            "average_rent": 7.75765635
        }
    ]
}
```
