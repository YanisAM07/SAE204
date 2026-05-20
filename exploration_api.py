import requests, json

BASE_URL = "https://data.ameli.fr/api/explore/v2.1/catalog/datasets"

def explorer(dataset_id, nb=2):
    resp = requests.get(f"{BASE_URL}/{dataset_id}/records", params={"limit": nb})
    data = resp.json()
    
    print(f"\n{'='*60}")
    print(f"Dataset : {dataset_id}")
    print(f"Total : {data.get('total_count', 0)} enregistrements")
    
    if data.get('results'):
        print(f"Champs : {list(data['results'][0].keys())}")
        print(json.dumps(data['results'][0], indent=2, ensure_ascii=False))

DATASETS = [
    "demographie-secteurs-conventionnels",
    "demographie-exercices-liberaux",
    "demographie-effectifs-et-les-densites",
    "demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans",
    "honoraires",
    "prescriptions",
    "patientele"
]

for ds in DATASETS:
    explorer(ds)