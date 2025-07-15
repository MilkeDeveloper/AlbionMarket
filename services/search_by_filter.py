
from collections import defaultdict
from typing import Optional

import httpx

from services.search_service import search_items


async def search_items_by_filter(q: str, itemID: Optional[str], tier_id: Optional[str], quality: Optional[str], city: Optional[list[...]]):
    idata = search_items(q)
    item_name = ""
    base_src = "https://render.albiononline.com/v1/item/"

    url = f"https://west.albion-online-data.com/api/v2/stats/prices/{tier_id}{itemID}.json?locations={','.join(city)}{quality}"
    try:
        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            if response.status_code != 200:
                return {"error": "Falha ao buscar os dados do item"}

            data = response.json()

            # Nome do item correspondente
            item_name = next(
                (item["name"] for item in idata if f"{tier_id}{itemID}" == item["item_id"]),
                "Nome Desconhecido"
            )

            # Agrupar por cidade
            grouped_by_city = defaultdict(list)

            for entry in data:
                if entry["sell_price_min"] > 0:
                    city = entry["city"]
                    grouped_by_city[city].append({
                        "name": item_name,
                        "image": base_src + f"{tier_id}{itemID}",
                        "city": city,
                        "tier": str(tier_id).replace("_", ""),
                        "price": entry["sell_price_min"],
                        "quality": entry["quality"],
                        "sell_price_date": entry["sell_price_min_date"]
                    })

            if not grouped_by_city:
                return {"item_id": itemID, "message": "Sem preços disponíveis no momento"}

            # Construir estrutura final
            return {
                "item": f"{tier_id}{itemID}",
                "cities": [
                    {
                        "city": city,
                        "prices": sorted(prices, key=lambda x: (x["quality"], x["price"]))
                    }
                    for city, prices in grouped_by_city.items()
                ]
            }

    except Exception as e:
        return {"error": f"Erro ao processar requisição: {str(e)}"}