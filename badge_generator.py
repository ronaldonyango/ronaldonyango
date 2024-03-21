import requests
from bs4 import BeautifulSoup

def get_download_count(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the element containing the download count
        downloads_element = soup.find('h5', class_='sc-fmKFGs sc-cUPRRX eLkEvR llGCIX')
        if downloads_element:
            download_count = downloads_element.text.strip()
            return download_count
        else:
            raise Exception("Download count element not found on the page")
    else:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")

def main():
    readme_file_path = "README.md" # relative to root directory
    url = 'https://www.kaggle.com/datasets/ronaldonyango/global-suicide-rates-1990-to-2022'
    badge_id = 1
    download_count = get_download_count(url)
    badge_markdown = create_badge(badge_id, download_count)
    update_readme(readme_file_path, badge_id, badge_markdown)

main()
