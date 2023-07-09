import time
import pandas as pd
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from concurrent.futures import ThreadPoolExecutor

def extract_price(link_soup):
    try:
        price_div = link_soup.find('div', class_='product-price__i product-price__i--bold')
        if price_div:
            price_val = price_div.find('span', class_='price-val')
            price_cur = price_div.find('span', class_='price-cur')
            if price_val and price_cur:
                price = re.sub(r'\s+', '', price_val.text.strip())  # Remove whitespace from the price value
                currency = price_cur.text.strip()
                return price, currency
    except Exception:
        pass
    return None, None


def extract_owner_category(link_soup):
    try:
        owner_category_div = link_soup.find('div', class_='product-owner__info-region')
        if owner_category_div:
            owner_category = owner_category_div.text.strip()
            return owner_category
    except Exception:
        pass
    return None


def extract_owner_name(link_soup):
    try:
        owner_name_div = link_soup.find('div', class_='product-owner__info-name')
        if owner_name_div:
            owner_name = owner_name_div.text.strip()
            return owner_name
    except Exception:
        pass
    return None


def extract_phone_number(link_soup):
    try:
        phone_number_div = link_soup.find('div', class_='product-phones__list-i')
        phone_number_a = phone_number_div.find('a') if phone_number_div else None
        phone_number = phone_number_a['href'].replace('tel:', '').replace('-', '').replace(' ', '') if phone_number_a else None
        return phone_number
    except Exception:
        pass
    return None


def extract_category(link_soup):
    try:
        category_div = link_soup.find('div', class_='product-properties__i').find('span', class_='product-properties__i-value')
        if category_div:
            category = category_div.text.strip()
            return category
    except Exception:
        pass
    return None


def extract_floor(link_soup):
    try:
        floor_div = link_soup.findAll('div', class_='product-properties__i')[1].find('span', class_='product-properties__i-value')
        if floor_div:
            floor = floor_div.text.strip()
            return floor
    except Exception:
        pass
    return None


def extract_area(link_soup):
    try:
        area_div = link_soup.findAll('div', class_='product-properties__i')[2].find('span', class_='product-properties__i-value')
        if area_div:
            area = area_div.text.strip()
            return area
    except Exception:
        pass
    return None


def extract_room_count(link_soup):
    try:
        room_count_div = link_soup.findAll('div', class_='product-properties__i')[3].find('span', class_='product-properties__i-value')
        if room_count_div:
            room_count = room_count_div.text.strip()
            return room_count
    except Exception:
        pass
    return None


def extract_description(link_soup):
    try:
        description_div = link_soup.findAll('div', class_='product-properties__i')[4].find('span', class_='product-properties__i-value')
        if description_div:
            description = description_div.text.strip()
            return description
    except Exception:
        pass
    return None


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


def extract_property_info(url, item_id):
    try:
        # Chrome settings
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(2)

        # Wait for the phone number element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-phones__btn-value')))

        # Find the element using XPath
        element = driver.find_element(By.CLASS_NAME, 'product-phones__btn-value')
        element.click()   # Click the button

        # Wait for the updated phone number element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-phones__list-i')))

        # Get the updated HTML after clicking the button
        updated_html = driver.page_source

        # Parse the updated HTML
        link_soup = BeautifulSoup(updated_html, 'html.parser')

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

        driver.quit()  # Close the WebDriver

        # Create a DataFrame with the extracted information
        data = {
            'item_id': [item_id],
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

async def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    df_list = []  # List to store the dataframes

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        async def process_item(item):
            link = 'https://bina.az' + item.a['href']
            item_id = item['data-item-id']
            df = await loop.run_in_executor(executor, extract_property_info, link, item_id)
            if df is not None:
                df['page'] = page  # Add the 'page' column with the page number
                df_list.append(df)

        for page in range(1, 2323):
            print(f"Scraping page {page}...")
            url = f'https://bina.az/alqi-satqi?page={page}'
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            content = soup.find_all('div', class_='items-i')

            tasks = [process_item(item) for item in content]
            await asyncio.gather(*tasks)

            driver.quit()  # Close the WebDriver

    # Concatenate all dataframes in the list
    final_df = pd.concat(df_list, ignore_index=True)

    # Process the final_df as desired
    final_df.to_csv(r"final_df.csv", sep=',', encoding='utf-8', header='true')
    final_df.to_parquet(r"final_df.parquet")
    final_df.to_excel('final_df.xlsx', engine='xlsxwriter')
    print(final_df)


# Run the main function
# ===>>> 16:24 08.07.2023 Baku,Azerbaijan
# ===>>> 08:51 09.07.2023 Baku,Azerbaijan

# [26852 rows x 14 columns]
# Execution time: 59161.54390025139 seconds

start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")