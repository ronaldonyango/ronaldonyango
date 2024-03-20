import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Set up the Kaggle API
api = KaggleApi()
api.authenticate_with_token(os.environ.get('KAGGLE_API_TOKEN'))

# Function to fetch dataset stats
def get_dataset_stats(dataset_name):
    dataset = api.dataset_metadata(dataset_name)
    views = dataset.view_count
    downloads = dataset.download_count
    return views, downloads

# Example usage
dataset_name = "ronaldonyango/global-suicide-rates-1990-to-2022"
views, downloads = get_dataset_stats(dataset_name)
print(f"Views: {views}, Downloads: {downloads}")
