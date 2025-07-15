from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from services.api_service import get_prices
from services.search_service import search_items

server = FastAPI()

# Lista de origens permitidas (exemplo com frontend local e Vercel)
origins = [
    "http://localhost:3000",  # seu Next.js local
    "https://seuapp.vercel.app"  # versão deployada se quiser
]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # <- quem pode acessar
    allow_credentials=True,
    allow_methods=["*"],              # <- permite GET, POST, etc.
    allow_headers=["*"],              # <- permite headers como Authorization, etc.
)

@server.get("/market/price/{item_id}")
async def get_item_prices(item_id: str, tier: Optional[int] = Query(None), quality: Optional[int] = Query(None), city: Optional[str] = Query(None)):

    result = await get_prices(item_id, tier, quality, city)
    return result

@server.get("/search")
def search(q: str = Query(..., description="Nome parcial do item")):
    return search_items(q)