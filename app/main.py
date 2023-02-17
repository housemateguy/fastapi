from app.api.routes import routes
from fastapi import FastAPI

app = FastAPI()

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)