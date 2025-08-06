from fastapi import FastAPI
from app.db.database import async_engine, Base
from app.routers import atletas
from app.routers import categoria, centro_treinamento
from fastapi_pagination import add_pagination


import asyncio 

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(atletas.router, prefix="/atletas", tags=["Atletas"])
app.include_router(categoria.router, prefix="/categorias", tags=["Categorias"])
app.include_router(centro_treinamento.router, prefix="/centros", tags=["Centro de Treinamento"])

add_pagination(app)