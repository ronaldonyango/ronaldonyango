from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def update_readme(readme_file_path, badge_id, new_badge):
    """
    Updates the README file with the new badge.
    """
    line_id = f'![kaggle-badge-{badge_id}]'
    badge_found = False
    new_file_content = []

    # Open README and update badge
    with open(readme_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line_id in line:
                # Replace old badge with new badge
                line = new_badge
                badge_found = True
            new_file_content.append(line)

    if not badge_found:
        raise Exception(f"Badge {badge_id} not found in {readme_file_path}")

    # Update README
    with open(readme_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_file_content)

def create_badge(badge_id, badge_value, badge_name='Downloads', badge_color='orange'):
    """
    Creates a Markdown badge with the given values.
    """
    badge_url = f'https://img.shields.io/badge/{badge_name}-{badge_value}-{badge_color}'
    markdown = f'![kaggle-badge-{badge_id}]({badge_url})\n'
    return markdown

def get_download_count(kaggle_url):
    """
    Scrapes the download count from the given Kaggle dataset URL.
    """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(kaggle_url)
    time.sleep(3)  # Wait for the page to load

    # Find the download count element
    downloads_element = driver.find_element(By.XPATH, '//h5[contains(@class, "eLkEvR")]')
    download_count = downloads_element.text

    driver.quit()
    return download_count

def main():
    readme_file_path = "README.md"  # Relative to root directory
    kaggle_url = 'https://www.kaggle.com/datasets/ronaldonyango/global-suicide-rates-1990-to-2022'
    badge_id = 1  # Each badge must be given a unique id

    download_count = get_download_count(kaggle_url)
    badge_markdown = create_badge(badge_id, download_count)
    update_readme(readme_file_path, badge_id, badge_markdown)

if __name__ == "__main__":
    main()
