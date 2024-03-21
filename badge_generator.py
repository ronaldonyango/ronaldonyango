def update_readme(readme_file_path, badge_id, new_badge):
    new_file_content = ''
    # id used to identify position of badge
    line_id = f'![kaggle-badge-{badge_id}]'
    badge_found = False

    # open readme and update badge
    with open(readme_file_path, 'r', encoding='utf-8') as f:
        # get all lines in readme
        lines = [line for line in f]
        for i in range(0, len(lines)):
            if line_id in lines[i]:
                # replace old badge with new badge
                lines[i] = new_badge
                badge_found = True
                break
        # concatenate lines
        new_file_content = ''.join(lines) if len(lines) > 0 else new_badge

    if not badge_found:
        raise Exception(
            str(f"Badge {badge_id} not found in {readme_file_path}"))
    # update readme
    with open(readme_file_path, 'w', encoding='utf-8') as f:
        f.write(new_file_content)


def create_badge(badge_id, badge_value,
                 badge_name='Downloads', badge_color='orange'):
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
        '//*[@id="site-content"]/div[2]/div/div[5]/div[6]/div[2]/div[1]/div/div[3]/h1')
    download_count = downloads_element.get_attribute("textContent")
    return (download_count)


def main():
    readme_file_path = "README.md"  # relative to root directory
    # change this url
    url = 'https://www.kaggle.com/datasets/ronaldonyango/global-suicide-rates-1990-to-2022'
    badge_id = 1  # each badge must be given a unique id
    x = get_download_count(url)
    y = create_badge(badge_id, x)
    update_readme(readme_file_path, badge_id, y)


main()
