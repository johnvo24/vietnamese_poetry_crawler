# https://poem.tkaraoke.com

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import csv
from concurrent.futures import ProcessPoolExecutor

GECKO_DRIVER_PATH = '/snap/bin/geckodriver'

# Variables
BASE_URL = "https://poem.tkaraoke.com"
NUM_PROCESSES = 4                                   # <==== CHANGE IT
poem_id_init = 10000
step = int(126999/NUM_PROCESSES)

def crawl_poems(process_i):
    # Khởi tạo Firefox WebDriver ở chế độ headless
    options = Options()
    options.headless = True  # Chạy ở chế độ headless (ẩn trình duyệt)
    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)

    poems_dataset = []
    counter = 0

    poem_id = poem_id_init + process_i*step
    while poem_id < poem_id_init + (process_i+1)*step-1:
        poem_url = BASE_URL + f"/{poem_id}/.html"
        poem_id = poem_id + 1

        driver.get(poem_url)
        time.sleep(0.001)

        page_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        title_tag = page_soup.find("h2", class_="h2-title-poem")
        if not title_tag:
            continue
        poem_title = title_tag.get_text(strip=True)
        counter = counter + 1
        print(f"P{process_i}|{counter} - {poem_id} - {poem_url} - {poem_title}")

        div_author = page_soup.find("div", class_="div-author-poem")
        poem_author = div_author.find("a").get_text(strip=True)
        poem_content = div_author.find_next_sibling().get_text("\n", strip=True)

        poems_dataset.append({
            'Content': poem_content,
            'Title': poem_title,
            'Genre': "",
            'Author': poem_author,
            'URL': poem_url
        })


    with open(f"dataset_crawled/poems_dataset_proc{process_i}.csv", mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['Content', 'Title', 'Genre', 'Author', 'URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for poem in poems_dataset:
            writer.writerow(poem)

    driver.quit()
    print(f"PROCESS {process_i} - Data crawled successfully!")

with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
    for i in range(NUM_PROCESSES):
        executor.submit(crawl_poems, i)
        