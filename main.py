import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
driver = webdriver.Chrome(options=chrome_options)

data = []

# Define a function to extract the owner name
def extract_owner_name(link_soup):
    owner_name_div = link_soup.find('div', class_='product-owner__info-name')
    if owner_name_div:
        owner_name = owner_name_div.text.strip()
        return owner_name
    else:
        return None

# Define a function to extract the owner category
def extract_owner_category(link_soup):
    owner_category_div = link_soup.find('div', class_='product-owner__info-category')
    if owner_category_div:
        owner_category = owner_category_div.text.strip()
        return owner_category
    else:
        return None

# Define a function to extract the full phone number
def extract_phone_number(button_parent):
    phone_number_div = button_parent.find('div', class_='product-phones__btn-value')
    if phone_number_div:
        phone_number = phone_number_div.text.strip()
        return phone_number
    else:
        return None

for page in range(1, 3):
    url = f'https://bina.az/alqi-satqi?page={page}'
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find_all('div', class_='items-i')

    for item in content:
        link = 'https://bina.az' + item.a['href']
        link = link.rstrip(':')  # Remove the trailing colon from the link

        driver.get(link)
        time.sleep(2)

        link_soup = BeautifulSoup(driver.page_source, 'html.parser')
        button_div = link_soup.find('div', class_='product-phones__btn-title')
        if button_div and button_div.text == 'Nömrəni göstər':
            button_parent = button_div.find_parent('div', class_='js-show-phones product-phones__btn')
            print(f"Button parent: {button_parent}")
            if button_parent is not None:
                try:
                    button_parent.click()  # Click the button

                    # Wait for the phone number element to be visible
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-phones__btn-value')))

                    # Extract the owner name and category
                    owner_name = extract_owner_name(link_soup)
                    owner_category = extract_owner_category(link_soup)

                    # Extract the full phone number
                    phone_number = extract_phone_number(button_parent)

                    data.append({'link': link, 'number': phone_number, 'owner_name': owner_name, 'owner_category': owner_category})
                except Exception as e:
                    print(f"Error occurred while processing {link}: {str(e)}")
                    data.append({'link': link, 'number': None, 'owner_name': None, 'owner_category': None})
            else:
                print("Button parent is None")
                data.append({'link': link, 'number': None, 'owner_name': None, 'owner_category': None})
        else:
            print("Button div not found")
            data.append({'link': link, 'number': None, 'owner_name': None, 'owner_category': None})

driver.quit()

# Create DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)
