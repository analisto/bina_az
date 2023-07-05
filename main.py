%%time
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import requests
# Warnings
from warnings import filterwarnings
filterwarnings('ignore')
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_mortgage(link_soup):
    try:
        mortgage_divs = link_soup.findAll('div', class_='product-properties__i')
        if len(mortgage_divs) > 5:
            mortgage_div = mortgage_divs[5].find('span', class_='product-properties__i-value')
            if mortgage_div:
                mortgage = mortgage_div.text.strip()
                return mortgage
    except Exception:
        pass
    return None

def extract_property_info(url, page):
    try:
        link_soup = BeautifulSoup(session.get(url, verify=False).text, 'html.parser')

        # Extract the full phone number
        phone_number_a = link_soup.find('div', class_='product-phones__list-i').find('a')
        phone_number = phone_number_a['href'].replace('tel:', '').replace('-', '').replace(' ', '') if phone_number_a else None

        # Extract the owner name
        owner_name = extract_owner_name(link_soup)

        # Extract the owner category
        owner_category = extract_owner_category(link_soup)

        # Extract other information
        category = extract_category(link_soup)
        floor = extract_floor(link_soup)
        area = extract_area(link_soup)
        room_count = extract_room_count(link_soup)
        description = extract_description(link_soup)
        mortgage = extract_mortgage(link_soup)
        price, currency = extract_price(link_soup)

        # Create a DataFrame with the extracted information
        data = {
            'page': [page],
            'url': [url],
            'phone number': [phone_number],
            'owner name': [owner_name],
            'owner category': [owner_category],
            'category': [category],
            'floor': [floor],
            'area': [area],
            'room count': [room_count],
            'description': [description],
            'mortgage': [mortgage],
            'price': [price],
            'currency': [currency]
        }
        df = pd.DataFrame(data)
        return df

    except Exception:
        return None


# Selenium settings
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
driver = webdriver.Chrome(options=chrome_options)

df_list = []  # List to store the dataframes
page = 1  # Initialize the page number

# Create a session object with SSL certificate verification disabled
session = requests.Session()
session.verify = False

while True:
    url = f'https://bina.az/alqi-satqi?page={page}'
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find_all('div', class_='items-i')

    if not content:
        break  # No more content found on the page, stop scraping

    for item in content:
        link = item.find('a')['href']
        link_url = f'https://bina.az{link}'
        link_soup = BeautifulSoup(session.get(link_url, verify=False).text, 'html.parser')

        # Extract property information
        df = extract_property_info(link_url, page)
        if df is not None:
            df_list.append(df)

        print(f"Scraping page {page} - Property URL: {link_url}")
        page += 1

driver.quit()  # Close the WebDriver

# Combine all the extracted dataframes into a single dataframe
final_df = pd.concat(df_list, ignore_index=True)

# Save the dataframe to a CSV file
final_df.to_csv('property_data_2.csv', index=False)
final_df.to_parquet(r"property_data_2.parquet") 
print('Scraping complete!')
