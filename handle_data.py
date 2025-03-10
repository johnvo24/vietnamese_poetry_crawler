from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import random
import helper

NUM_PROCESSES = 4                                   # <==== CHANGE IT
GECKO_DRIVER_PATH = '/snap/bin/geckodriver'
FILE_NAME = 'poems_dataset_proc0_0'
BASE_URL = "https://www.thivien.net"
file_df = pd.read_csv(f'{FILE_NAME}.csv')


def convert_poem_genre(genre):
    if genre.lower() == "thơ mới bốn chữ": target = "Bốn chữ"
    elif genre.lower() == "thơ mới năm chữ": target = "Năm chữ"
    elif genre.lower() == "thơ mới sáu chữ": target = "Sáu chữ"
    elif genre.lower() == "thơ mới bảy chữ": target = "Bảy chữ"
    elif genre.lower() == "thơ mới tám chữ": target = "Tám chữ"
    else: target = genre
    return target

def fix_data(df, process_i):
    # Khởi tạo Firefox WebDriver ở chế độ headless
    options = Options()
    options.headless = True  # Chạy ở chế độ headless (ẩn trình duyệt)
    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    # Đọc dữ liệu

    for index, poem in df.iterrows():
        if not pd.isna(poem["Genre"]): continue

        url = f"https://www.thivien.net/searchpoem.php?Title={str(poem['Title']).lower()}&Author={str(poem['Author']).lower()}&ViewType=1&Country=2"
        driver.get(url)
        time.sleep(random.uniform(3, 7))

        # Kiểm tra nếu bị chặn bởi CAPTCHA
        while "xác nhận không phải máy" in driver.page_source.lower():
            print("🔒 Phát hiện CAPTCHA!!!")
            time.sleep(random.uniform(60, 65))
            driver.get(url)
            time.sleep(random.uniform(3, 7))
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        poem_links = soup.find_all("h4", class_="list-item-header")
        if len(poem_links) < 1:
            print(f"P{process_i} - Empty - {url}")
            continue
        
        for idx, h4_tag in enumerate(poem_links, start=1):
            a_tag = h4_tag.find('a')
            if a_tag:
                poem_url = BASE_URL + a_tag['href']
                driver.get(poem_url)
                time.sleep(random.uniform(1, 4))

                # Kiểm tra nếu bị chặn bởi CAPTCHA
                while "xác nhận không phải máy" in driver.page_source.lower():
                    print("🔒 Phát hiện CAPTCHA!!!")
                    time.sleep(random.uniform(30, 35))
                    driver.get(url)
                    time.sleep(random.uniform(1, 4))

                poem_soup = BeautifulSoup(driver.page_source, "html.parser")
                summary_section = poem_soup.find("div", class_="summary-section")
                if summary_section:
                    poem_genre = summary_section.find("a").get_text()
                    content_tag = poem_soup.find("div", class_="poem-content")

                    df.at[index, "Genre"] = convert_poem_genre(poem_genre)
                    df.at[index, "Edited"] = BeautifulSoup(content_tag.find('p').decode_contents().replace("<br/>", "\n"), "html.parser").get_text()

                    print(f"P{process_i} - {index} - {poem['Title']} - {url}")
                else: 
                    print(f"P{process_i} - Empty - {url}")
            else: 
                print(f"P{process_i} - Empty - {url}")

    driver.quit()
    print(f"P{process_i} - Data handled successfully!")
    return df
    

def main():
    df_parts = helper.split_df(file_df, 4)

    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        df_results = list(executor.map(fix_data, df_parts, range(NUM_PROCESSES)))

    df = pd.concat(df_results, ignore_index=True)
    df.to_csv(f"{FILE_NAME}_handled.csv", index=False, encoding="utf-8")
    
if __name__ == "__main__":
    main()