import re
from typing import Optional, List
import httpx

from services.search_by_city import search_items_by_city
from services.search_by_filter import search_items_by_filter
from services.search_by_quality import search_items_by_quality
from services.search_service import search_items
from services.general_search import general_search_items


locations = ["Thetford", "Bridgewatch", "Lymhurst", "Martlock", "Fort Sterling", "Caerleon"]

TIERS = [1, 2, 3, 4, 5, 6, 7, 8]

async def get_prices(q: str, tier: Optional[int] = None, quality: Optional[int] = None, city: Optional[str] = None):
    data = search_items(q)
    item_id = data[0]["item_id"]
    #print(f"{data}")

    item_id = re.sub(r"^T\d+_", "", item_id)
    quality_id = f"&qualities={quality}" if quality is not None else ""
    tier_id = f"T{tier}_" if tier else "T4_"
    cities = [city] if city is not None else locations

    if tier:
        return await search_items_by_filter(q, item_id, tier_id, quality_id, cities)
    elif city:
        return await search_items_by_city(q, item_id, quality_id, TIERS, cities)
    elif quality:
        return await search_items_by_quality(q, item_id, quality_id, TIERS, cities)
    else:
        return await general_search_items(q, item_id, quality_id, TIERS, cities)



