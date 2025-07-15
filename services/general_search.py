import re
from typing import Optional
import httpx

from services.search_service import search_items


async def general_search_items(q: str, itemID, quality: Optional[str], tiers: Optional[list[int]], cities: Optional[list[str]]):
    data = search_items(q)
    item_name = None
    base_src = "https://render.albiononline.com/v1/item/"

    try:
        base_item_id = re.sub(r"^T\d+_", "", itemID)
        all_prices = {}

        async with httpx.AsyncClient() as client:
            for tier in tiers:
                item_id = f"T{tier}_{base_item_id}"
                url = f"https://west.albion-online-data.com/api/v2/stats/prices/{item_id}.json?locations={','.join(cities)}{quality}"
                resp = await client.get(url)

                if resp.status_code == 200:
                    entries = resp.json()

                    for entry in entries:
                        city = entry["city"]
                        price = entry["sell_price_min"]
                        quality = entry["quality"]
                        date = entry["sell_price_min_date"]
                        current_item_id = entry["item_id"]  # <- importante: use esse ID real

                        if price > 0:
                            # busca o nome correto com base no item_id da entrada
                            item_name = next((item["name"] for item in data if item["item_id"] == current_item_id), None)

                            if item_name is None:
                                continue # se não achou, pula o item

                            if city not in all_prices:
                                all_prices[city] = []

                            # adiciona o preço do tier naquela cidade
                            all_prices[city].append({
                                "city": city,
                                "name": item_name,
                                "image": base_src + f"{item_id}",
                                "tier": tier,
                                "quality": quality,
                                "item_id": item_id,
                                "price": price,
                                "date": date
                            })

        if not all_prices:
            return {"item": base_item_id, "message": "Sem preços disponíveis"}

        # ordena os preços por tier em cada cidade
        formatted = []
        for city, entries in all_prices.items():
            sorted_prices = sorted(entries, key=lambda x: x["tier"])
            formatted.append({
                "city": city,
                "prices": sorted_prices
            })

        return {
            "item": base_item_id,
            "cities": formatted
        }

    except Exception as e:
        return {"error": f"Erro: {str(e)}"}