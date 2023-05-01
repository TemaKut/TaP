from fastapi import FastAPI

from app.api import api_router


app = FastAPI(debug=True, title='TaP', version='Alpha')

app.include_router(api_router)
