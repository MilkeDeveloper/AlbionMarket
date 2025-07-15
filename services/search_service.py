import json
from fastapi import HTTPException
from typing import List

with open("metadata/items.json", "r", encoding="utf-8") as f:
    items_data = json.load(f)


def search_items(query: str, lang: str = "PT-BR") -> List[dict]:
    query = query.lower()
    results = []

    for item in items_data:
        if not item or not isinstance(item, dict):
            continue  # ignora valores nulos ou inválidos

        localized = item.get("LocalizedNames", {})
        if not isinstance(localized, dict):
            continue

        name = localized.get(lang)
        if name and query in name.lower():
            results.append({
                "item_id": item.get("UniqueName", "UNKNOWN"),
                "name": name
            })

    if not results:
        raise HTTPException(status_code=404, detail="Nenhum item encontrado.")

    return results