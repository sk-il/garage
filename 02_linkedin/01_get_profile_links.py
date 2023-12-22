from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import csv


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


file_name = 'profile_links.csv'
url = 'https://www.linkedin.com/login'

username = ''
password = ''

driver = get_driver()
driver.get(url)

selenium_by('id', 'username', driver).send_keys(username)
selenium_by('id', 'password', driver).send_keys(password)
selenium_by('text', 'Sign in', driver, tag_name='button').click()
selenium_by('class_name', 'search-global-typeahead__input', driver).send_keys('Data Analyst')
selenium_by('class_name', 'search-global-typeahead__input', driver).send_keys(Keys.ENTER)


while True:
    n_pages = int(input('Select filters and give me number of pages: '))
    if n_pages == 0:
        break

    for n in range(n_pages):
        profile_links = []

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        links = soup.find_all('a', {'class': 'app-aware-link'}, href=True)

        for link in links:
            if r'/in/' in link['href']:
                link = link['href'].split('?')[0]
                profile_links.append(link)

        profile_links = list(set(profile_links))

        with open(file_name, 'a') as f:
            wr = csv.writer(f, delimiter="\n")
            wr.writerow(profile_links)

        selenium_by('something', 'Next', driver, tag_name='button', something='aria-label').click()
        sleep(5)
