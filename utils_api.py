import requests, time

BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"
LIMIT = 100

def collecter_tout(dataset_id, select=None, where=None, group_by=None, pause=0.2):
    """Récupère tous les enregistrements d'un dataset en paginant."""
    url, records, offset = f"{BASE_URL}/{dataset_id}/records", [], 0
    
    while True:
        params = {"limit": LIMIT, "offset": offset}
        if select: params["select"] = select
        if where: params["where"] = where
        if group_by: params["group_by"] = group_by
        
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        records.extend(data.get("results", []))
        
        if len(records) >= data.get("total_count", 0): 
            break
            
        offset += LIMIT
        time.sleep(pause)
        
    return records