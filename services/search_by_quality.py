import re
from collections import defaultdict
from typing import Optional

import httpx

from services.search_service import search_items


async def search_items_by_quality(q: str, itemID: Optional[str], quality: Optional[str], tiers: Optional[list[int]], city: Optional[list[str]]):
    idata = search_items(q)
    base_src = "https://render.albiononline.com/v1/item/"
    base_item_id = re.sub(r"^T\d+_", "", itemID or "")
    all_prices = defaultdict(list)
    item_name = "Nome Desconhecido"

    print(f"Filtro tiers recebido: {tiers}")

    if not city:
        city = ["Thetford", "Lymhurst", "Bridgewatch", "Martlock", "Fort Sterling", "Caerleon"]
    if not tiers:
        tiers = [1, 2, 3, 5, 7, 8]  # ou todos tiers que desejar

    try:
        async with httpx.AsyncClient() as client:

            # Prepara nomes por tier
            item_names = {}
            for tier_id in tiers:
                item_id = f"T{tier_id}_{base_item_id}"
                item_names[tier_id] = next(
                    (item["name"] for item in idata if item["item_id"] == item_id),
                    "Nome Desconhecido"
                )

            for tier_id in tiers:
                item_id = f"T{tier_id}_{base_item_id}"
                url = f"https://west.albion-online-data.com/api/v2/stats/prices/{item_id}.json?locations={','.join(city)}"
                if quality:
                    url += f"&qualities={quality}" # assegure que quality já vem com &qualities=...

                response = await client.get(url)
                if response.status_code != 200:
                    continue

                data = response.json()

                for entry in data:
                    if entry["sell_price_min"] > 0:
                        if quality is not None or str(entry["quality"]) == str(quality):
                            all_prices[entry["city"]].append({
                                "name": item_names.get(tier_id, "Nome Desconhecido"),
                                "image": base_src + item_id,
                                "city": entry["city"],
                                "price": entry["sell_price_min"],
                                "tier": tier_id,
                                "quality": entry["quality"],
                                "sell_price_date": entry["sell_price_min_date"]
                            })

        if not all_prices:
            return {"item_id": itemID, "message": "Sem preços disponíveis no momento"}

        return {
            "item": base_item_id,
            "cities": [
                {
                    "city": city,
                    "prices": sorted(prices, key=lambda x: (x["tier"], x["quality"], x["price"]))
                }
                for city, prices in all_prices.items()
            ]
        }

    except Exception as e:
        return {"error": f"Erro ao processar requisição: {str(e)}"}