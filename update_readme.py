import os
import subprocess
import json

def download_dataset_metadata(username, dataset_name):
    kaggle_dir = os.path.join(os.path.expanduser('~'), '.kaggle')
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)

    kaggle_json_path = os.path.join(kaggle_dir, 'kaggle.json')

    if not os.path.exists(kaggle_json_path):
        print("Error: kaggle.json file not found in .kaggle directory.")
        return

    # Download dataset metadata using Kaggle API
    command = f'kaggle datasets metadata {username}/{dataset_name}'
    subprocess.run(command, shell=True)

def extract_metadata():
    with open('dataset-metadata.json') as file:
        metadata = json.load(file)
        return metadata.get('totalViews', 0), metadata.get('totalDownloads', 0)

def update_readme(views, downloads):
    with open('README.md', 'r') as file:
        readme = file.read()

    # Update badges
    updated_readme = readme.replace(
        '[![Total Views](http://img.shields.io/badge/Total%20Views-%s-blue)](#)'
        % '<totalViews>',
        '[![Total Views](http://img.shields.io/badge/Total%20Views-%s-blue)](#)' % views
    ).replace(
        '[![Total Downloads](http://img.shields.io/badge/Total%20Downloads-%s-brightgreen)](#)'
        % '<totalDownloads>',
        '[![Total Downloads](http://img.shields.io/badge/Total%20Downloads-%s-brightgreen)](#)' % downloads
    )

    with open('README.md', 'w') as file:
        file.write(updated_readme)

if __name__ == "__main__":
    username = 'ronaldonyango'
    dataset_name = 'global-suicide-rates-1990-to-2022'
    
    download_dataset_metadata(username, dataset_name)
    views, downloads = extract_metadata()
    update_readme(views, downloads)
