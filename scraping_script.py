import time
import pandas as pd
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import aiohttp

async def extract_property_info(url, session):
    try:
        async with session.get(url) as response:
            content = await response.text()

        link_soup = BeautifulSoup(content, 'html.parser')

        phone_number_a = link_soup.find('div', class_='product-phones__list-i').find('a')
        phone_number = (
            phone_number_a['href'].replace('tel:', '').replace('-', '').replace(' ', '')
            if phone_number_a
            else None
        )

        owner_name = extract_owner_name(link_soup)
        owner_category = extract_owner_category(link_soup)
        category = extract_category(link_soup)
        floor = extract_floor(link_soup)
        area = extract_area(link_soup)
        room_count = extract_room_count(link_soup)
        description = extract_description(link_soup)
        mortgage = extract_mortgage(link_soup)
        price, currency = extract_price(link_soup)

        data = {
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


def extract_price(link_soup):
    try:
        price_div = link_soup.find('div', class_='product-price__i product-price__i--bold')
        if price_div:
            price_val = price_div.find('span', class_='price-val')
            price_cur = price_div.find('span', class_='price-cur')
            if price_val and price_cur:
                price = re.sub(r'\s+', '', price_val.text.strip())
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


# async def main():
#     urls = []

#     # Starting link extraction loop
#     for page in range(1, 3):
#         print(f"Scraping page {page}...")
#         url = f'https://bina.az/alqi-satqi?page={page}'
#         urls.append(url)

#     df_list = []
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.ensure_future(extract_property_info(url, session))
#             tasks.append(task)

#         property_data = await asyncio.gather(*tasks)

#         for data in property_data:
#             if data is not None:
#                 df_list.append(data)

#     # Concatenate all dataframes in the list
#     final_df = pd.concat(df_list, ignore_index=True)

#     # Process the final_df as desired
#     # ...

#     print(final_df)


# # Selenium settings
# chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
# driver = webdriver.Chrome(options=chrome_options)
# driver.quit()  # Close the WebDriver

# # Run the main function
# start_time = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")
async def main():
    urls = []

    # Starting link extraction loop
    for page in range(1, 3):
        print(f"Scraping page {page}...")
        url = f'https://bina.az/alqi-satqi?page={page}'
        urls.append(url)

    df_list = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(extract_property_info(url, session))
            tasks.append(task)

        property_data = await asyncio.gather(*tasks)

        for data in property_data:
            if data is not None:
                df_list.append(data)

    # Check the extracted data
    for df in df_list:
        print(df)

    # Concatenate all dataframes in the list
    final_df = pd.concat(df_list, ignore_index=True)

    # Process the final_df as desired
    print(final_df)

# ... (previous code)

# Run the main function
start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")