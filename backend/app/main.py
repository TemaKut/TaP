from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router


app = FastAPI(debug=True, title='TaP', version='Alpha')

# Подключение роутеров API
app.include_router(api_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
