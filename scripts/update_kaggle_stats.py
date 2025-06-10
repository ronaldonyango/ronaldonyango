import os
import json
import requests
from slugify import slugify

def get_kaggle_stats():
    datasets = [
        {"slug": "ronaldonyango/global-suicide-rates-1990-to-2022", "name": "Global Suicide Rates"},
        # Add more datasets here
    ]
    
    stats = {}
    headers = {
        "Authorization": f"Bearer {os.getenv('KAGGLE_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    for dataset in datasets:
        try:
            url = f"https://www.kaggle.com/api/v1/datasets/view/{dataset['slug']}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            name_key = slugify(dataset['name'])
            
            stats[f"{name_key}-views"] = data.get('totalViews', 0)
            stats[f"{name_key}-downloads"] = data.get('totalDownloads', 0)
            
            print(f"Processed {dataset['name']}: {stats[f'{name_key}-views']} views")
            
        except Exception as e:
            print(f"Error processing {dataset['name']}: {str(e)}")
            stats[f"{slugify(dataset['name'])}-views"] = "N/A"
            stats[f"{slugify(dataset['name'])}-downloads"] = "N/A"
    
    # Write outputs for GitHub Actions
    with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
        print(f{'stats': json.dumps(stats)}, file=f)

if __name__ == "__main__":
    get_kaggle_stats()