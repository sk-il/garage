from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import os
import random


# My regular SELENIUM functions
def get_driver(wait=3):
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


def get_links_list(profile_links_path, profiles_path):
    new_links = pd.read_csv(profile_links_path, usecols=['link'])

    if os.path.isfile(profiles_path):
        old_links = pd.read_csv(profiles_path, usecols=['link', 'name'])
        old_links.dropna(inplace=True)
    else:
        old_links = []

    return list(new_links.loc[~new_links['link'].isin(old_links['link']), 'link'])


file_name = 'profiles.csv'
url = 'https://www.linkedin.com/login'

username = ''
password = ''

profile_links_path = 'profile_links_clean.csv'
profiles_path = 'profiles.csv'
links = get_links_list(profile_links_path, profiles_path)
print(len(links))

driver = get_driver()
driver.get(url)

selenium_by('id', 'username', driver).send_keys(username)
selenium_by('id', 'password', driver).send_keys(password)
selenium_by('text', 'Sign in', driver, tag_name='button').click()

data = []

for link in links:
    print(link)
    driver.get(link)
    sleep(random.randint(30, 60))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()

    try:
        headline = soup.find('div', {'class': 'text-body-medium break-words'}).text.strip()
    except:
        headline = None
    try:
        place = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'}).text.strip()
    except:
        place = None
    try:
        company_link = soup.find('a', {'data-field': 'experience_company_logo'})['href']
    except:
        company_link = None
    try:
        company_name = soup.find('span', {
            'class': 'GrpjSuTnJuVIZvqQGOlBpxLRnnyFpfCYJCw hoverable-link-text break-words text-body-small t-black'}).text.strip()
    except:
        company_name = None
    try:
        position = soup.find('div', {'class': 'display-flex flex-wrap align-items-center full-height'}).text.strip()
    except:
        position = None
    try:
        education = soup.find('span', {
            'class': 'pv-text-details__right-panel-item-text hoverable-link-text break-words text-body-small t-black'}).text.strip()
    except:
        education = None

    profile_data = {
        'link': link,
        'name': name,
        'headline': headline,
        'place': place,
        'company_link': company_link,
        'company_name': company_name,
        'position': position,
        'education': education,
    }

    data.append(profile_data)

    # Save results every 10
    if len(data) == 10 or link == links[-1]:
        df = pd.DataFrame(data)

        # Add header if file doesn't exist
        header = not os.path.isfile(file_name)
        df.to_csv(file_name, mode='a', header=header, index=False)

        data = []