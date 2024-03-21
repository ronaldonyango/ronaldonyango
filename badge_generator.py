from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By

def update_readme(readme_file_path, badge_id, new_badge):
    new_file_content = ''
    line_id = f'![kaggle-badge-{badge_id}]'
    badge_found = False

    with open(readme_file_path, 'r', encoding='utf-8') as f:
        lines = [line for line in f]

    for i in range(0, len(lines)):
        if line_id in lines[i]:
            lines[i] = new_badge
            badge_found = True
            break

    new_file_content = ''.join(lines) if len(lines) > 0 else new_badge

    if not badge_found:
        raise Exception(str(f"Badge {badge_id} not found in {readme_file_path}"))

    with open(readme_file_path, 'w', encoding='utf-8') as f:
        f.write(new_file_content)

def create_badge(badge_id, badge_value, badge_name='Downloads', badge_color='orange'):
    badge_url = (f'https://img.shields.io/badge/{badge_name}'
                 f'-{badge_value}-{badge_color}')
    markdown = (f'![kaggle-badge-{badge_id}]({badge_url})\n')
    return markdown

def get_download_count(kaggle_url: str):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(kaggle_url)
    time.sleep(3)
    downloads_element = driver.find_element(
        By.XPATH,
        '//*[@id="site-content"]//div[@class="sc-fMeROS hbTLrg"]//h5[@class="sc-fmKFGs sc-cUPRRX eLkEvR llGCIX"]'
    )
    download_count = downloads_element.get_attribute("textContent").strip()
    return download_count

def main():
    readme_file_path = "README.md" # relative to root directory
    url = 'https://www.kaggle.com/datasets/ronaldonyango/global-suicide-rates-1990-to-2022'
    badge_id = 1
    download_count = get_download_count(url)
    badge_markdown = create_badge(badge_id, download_count)
    update_readme(readme_file_path, badge_id, badge_markdown)

main()
