from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import os.path


# My regular SELENIUM functions
def get_driver(wait=30):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(wait)
    driver.maximize_window()
    return driver


def selenium_by(by, value, driver, tag_name='*', something='', first=True):
    if by == 'id':
        elements = driver.find_elements(By.ID, value=value)
    elif by == 'name':
        elements = driver.find_elements(By.NAME, value=value)
    elif by == 'xpath':
        elements = driver.find_elements(By.XPATH, value=value)
    elif by == 'link_text':
        elements = driver.find_elements(By.LINK_TEXT, value=value)
    elif by == 'partial_link_text':
        elements = driver.find_elements(By.PARTIAL_LINK_TEXT, value=value)
    elif by == 'tag_name':
        elements = driver.find_elements(By.TAG_NAME, value=value)
    elif by == 'class_name':
        elements = driver.find_elements(By.CLASS_NAME, value=value)
    elif by == 'css_selector':
        elements = driver.find_elements(By.CSS_SELECTOR, value=value)
    elif by == 'text':
        elements = driver.find_elements(By.XPATH, f'//{tag_name}[contains(text(), "{value}")]')
    elif by == 'something':
        elements = driver.find_elements(By.XPATH, f'//{tag_name}[@{something}="{value}"]')
    elif by == 'something_contains':
        elements = driver.find_elements(By.XPATH, f'//{tag_name}[contains(@{something}, "{value}")]')

    if first:
        return elements[0]
    else:
        return elements


# Scrapping fields from boardgames list
def get_boardgames_list(first_page, last_page, driver, file_path):
    base_url = "https://boardgamegeek.com/browse/boardgame"

    for page in range(first_page, last_page + 1):
        url = f"{base_url}/page/{page}"
        driver.get(url)
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        games_list = []

        # Extract the table rows
        rows = soup.find_all('tr', id='row_')

        for row in rows:
            # Extract data from each row
            columns = row.find_all('td')
            rank = columns[0].text.strip()
            title_element = columns[2].find('a')
            title = title_element.text.strip()
            game_link = 'https://boardgamegeek.com' + title_element['href']
            year = columns[2].find('span').text.strip(' ()') if columns[2].find('span') is not None else None
            description = columns[2].find('p').text.strip() if columns[2].find('p') is not None else None
            geek_rating = columns[4].text.strip()
            avg_rating = columns[5].text.strip()
            num_voters = columns[6].text.strip()
            price = columns[9].find('a').text.strip() if columns[9].find('a') is not None else None

            game_data = {
                'rank': rank,
                'title': title,
                'link': game_link,
                'year': year,
                'description': description,
                'geek_rating': geek_rating,
                'avg_rating': avg_rating,
                'num_voters': num_voters,
                'price': price
            }

            games_list.append(game_data)

        print(page, len(games_list))

        if len(games_list) == 0:
            if not os.path.isfile('raw/missed_pages.csv'):
                with open('missed_pages.csv', 'w') as f:
                    f.write(f'{str(page)}')
            else:
                with open('missed_pages.csv', 'a') as f:
                    f.write(f'\n{str(page)}')
        else:
            df = pd.DataFrame(games_list)
            # Add header if file doesn't exist
            header = not os.path.isfile(file_path)
            df.to_csv(file_path, mode='a', header=header, index=False)



def main(username, password, file_path, first_page, last_page):
    driver = get_driver()
    driver.get('https://boardgamegeek.com/browse/boardgame')

    # Log in for full access
    selenium_by('text', 'Sign In', driver, tag_name='button', first=True).click()
    selenium_by('id', 'inputUsername', driver).send_keys(username)
    selenium_by('id', 'inputPassword', driver).send_keys(password)
    selenium_by('text', 'Sign In', driver, tag_name='button').click()
    sleep(5)

    get_boardgames_list(first_page, last_page, driver, file_path)

    if os.path.isfile('raw/missed_pages.csv'):
        with open('raw/missed_pages.csv', 'r') as f:
            for line in f:
                sleep(2)
                missed_page = int(line.strip())
                get_boardgames_list(missed_page, missed_page, driver, file_path)


username = ''
password = ''
file_path = r'raw\boardgames_list.csv'

main(username, password, file_path, 1, 1501)
