# /https://www.thivien.net

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import string
import random
import csv

GECKO_DRIVER_PATH = '/snap/bin/geckodriver'

# Khởi tạo Firefox WebDriver ở chế độ headless
options = Options()
options.headless = True  # Chạy ở chế độ headless (ẩn trình duyệt)
service = Service(GECKO_DRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

# Variables
poem_types = [3, 6, 7, 13, 14, 15, 16, 17, 18, 19, 20]
genres = ['ngungontutuyet', 'thatngontutuyet', 'thatngonbatcu', 'lucbat', 'songthatlucbat', 'thomoibonchu', 'thomoinamchu', 'thomoisauchu', 'thomoibaychu', 'thomoitamchu', 'tudo']
BASE_URL = "https://www.thivien.net"
poems_dataset = []
counter = 0

for idx, poem_type in enumerate(poem_types, start=0):
    for letter in string.ascii_lowercase:
        page = 1
        while True:
            url = f"https://www.thivien.net/searchpoem.php?Title={letter}&PoemType={poem_type}&ViewType=1&Country=2&Page={page}"
            print(url)

            driver.get(url)
            time.sleep(1)

            # Kiểm tra nếu bị chặn bởi CAPTCHA
            while "xác nhận không phải máy" in driver.page_source.lower():
                print("🔒 CAPTCHA phát hiện! Vui lòng giải quyết thủ công...")
                time.sleep(random.uniform(15, 20))
                driver.get(url)
                time.sleep(random.uniform(1))
                

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            poem_links = soup.find_all("h4", class_="list-item-header")
            if len(poem_links) < 1: break
            else: page = page + 1

            for idx, h4_tag in enumerate(poem_links, start=1):
                a_tag = h4_tag.find('a')
                if a_tag:
                    poem_url = BASE_URL + a_tag['href']
                    if all(poem['URL'] != poem_url for poem in poems_dataset):
                        driver.get(poem_url)
                        time.sleep(random.uniform(2, 3))

                        # Kiểm tra nếu bị chặn bởi CAPTCHA
                        while "xác nhận không phải máy" in driver.page_source.lower():
                            print("🔒 CAPTCHA phát hiện! Vui lòng giải quyết thủ công...")                    
                            time.sleep(random.uniform(15, 20))
                            driver.get(poem_url)
                            time.sleep(random.uniform(2, 5))

                        poem_soup = BeautifulSoup(driver.page_source, "html.parser")
                        content_tag = poem_soup.find("div", class_="poem-content")

                        poem_title = poem_soup.find("header", class_="page-header").find("h1").get_text(strip=True)
                        poem_genre = genres[idx]
                        poem_content = content_tag.get_text("\n", strip=True) if content_tag else False
                        
                        if poem_content:
                            counter = counter + 1
                            print((counter, poem_title))
                            poems_dataset.append({
                                'Content': poem_content,
                                'Title': poem_title,
                                'Genre': poem_genre,
                                'URL': poem_url
                            })


with open('dataset_crawled/poems_dataset_1.csv', mode='w', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['Content', 'Title', 'Genre', 'URL']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for poem in poems_dataset:
        writer.writerow(poem)

driver.quit()
print("Data crawled successfully!")