from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import time
import random
import helper

class DataHandler:
    def __init__(self, driver_type="firefox", num_processes=1):
        self.num_processes = num_processes
        self.base_url = "https://www.thivien.net"
        self.driver_type = driver_type
        self.driver_path = {
            "firefox": "/usr/local/bin/geckodriver",
            "chrome": "C:/Webdriver/chromedriver-win64/chromedriver.exe"
        }
        
        self.authors_not_in_thivien = pd.read_csv('authors_not_in_thivien.csv')["Author"].to_list()
        self.authors_in_thivien = pd.read_csv('authors_in_thivien.csv')["Author"].to_list()
    
    def get_driver(self):
        if self.driver_type == "firefox":
            options = FirefoxOptions()
            service = FirefoxService(self.driver_path["firefox"])
            return webdriver.Firefox(service=service, options=options)
        else:
            options = ChromeOptions()
            service = ChromeService(self.driver_path["chrome"])
            return webdriver.Chrome(service=service, options=options)

    def convert_poem_genre(self, genre):
      if genre.lower() == "thơ mới bốn chữ": target = "Bốn chữ"
      elif genre.lower() == "thơ mới năm chữ": target = "Năm chữ"
      elif genre.lower() == "thơ mới sáu chữ": target = "Sáu chữ"
      elif genre.lower() == "thơ mới bảy chữ": target = "Bảy chữ"
      elif genre.lower() == "thơ mới tám chữ": target = "Tám chữ"
      elif genre.lower() == "thơ tự do": target = "Tự do"
      else: target = genre
      return target
    
    def fix_data(self, df, process_i):
      driver = self.get_driver()
      request_count = 0

      for index, poem in df.iterrows():
        if not pd.isna(poem["Genre"]): 
          print(f"P{process_i} - {index} - Existed")
          continue

        if request_count > 24:
          print(f"P{process_i} has a break time after 24 requests...")
          request_count = 0
          # driver.quit()
          # driver = get_driver()
          time.sleep(random.uniform(60, 120))

        if str(poem['Author']).lower() in self.authors_not_in_thivien:
          print(f"E1: P{process_i} - {index} - Author not found: {str(poem['Author']).lower()}")
          continue
        elif str(poem['Author']).lower() not in self.authors_in_thivien:
          # SEARCH AUTHOR
          driver.get(f"https://www.thivien.net/searchpoem.php?Author={str(poem['Author']).lower()}&ViewType=1&Country=2")
          request_count += 1
          helper.delay()
          author_soup = BeautifulSoup(driver.page_source, "html.parser")
          poems_of_author = author_soup.find_all("h4", class_="list-item-header")
          if len(poems_of_author) < 1:
            print(f"E2: P{process_i} - {index} - Author not found: {str(poem['Author']).lower()}")
            self.authors_not_in_thivien.append(str(poem['Author']).lower())
            continue
          else: self.authors_in_thivien.append(str(poem['Author']).lower())

        # SEARCH AUTHOR AND POEM
        url = f"https://www.thivien.net/searchpoem.php?Title={str(poem['Title']).lower()}&Author={str(poem['Author']).lower()}&ViewType=1&Country=2"
        driver.get(url)
        request_count += 1
        helper.delay()

        # Kiểm tra nếu bị chặn bởi CAPTCHA
        while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
          if "tần suất quá cao" in driver.page_source.lower():
            print("🔒 Bị chặn truy cập!!!")
            time.sleep(random.uniform(180, 240))
            ## Change proxy
            driver.quit()
            driver = self.get_driver()
          else:
            print("🔒 Phát hiện CAPTCHA!!!")
            time.sleep(random.uniform(60, 65))
          driver.get(url)
          request_count += 1
          helper.delay()
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        poem_links = soup.find_all("h4", class_="list-item-header")
        if len(poem_links) < 1:
          print(f"E3: P{process_i} - {index} - Empty - {url}")
          continue
        
        a_tag = None
        for idx, h4_tag in enumerate(poem_links, start=1):
          a_tg = h4_tag.find('a')
          if a_tg.get_text().lower() == str(poem["Title"]).lower():
            a_tag = a_tg
            break
        if a_tag:
          poem_url = self.base_url + a_tag['href']
          driver.get(poem_url)
          request_count += 1
          helper.delay()

          # Kiểm tra nếu bị chặn bởi CAPTCHA
          while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
            if "tần suất quá cao" in driver.page_source.lower():
              print("🔒 Bị chặn truy cập!!!")
              time.sleep(random.uniform(180, 240))
              ## Change proxy
              driver.quit()
              driver = self.get_driver()
            else:
              print("🔒 Phát hiện CAPTCHA!!!")
              time.sleep(random.uniform(60, 65))
            driver.get(url)
            request_count += 1
            helper.delay()

          poem_soup = BeautifulSoup(driver.page_source, "html.parser")
          summary_section = poem_soup.find("div", class_="summary-section")
          if summary_section:
            poem_genre = summary_section.find("a").get_text()
            content_tag = poem_soup.find("div", class_="poem-content")

            df.at[index, "Genre"] = self.convert_poem_genre(poem_genre)
            df.at[index, "Edited"] = BeautifulSoup(content_tag.find('p').decode_contents().replace("<br/>", "\n"), "html.parser").get_text()

            print(f"OK: P{process_i} - {index} - {poem['Title']} - {url}")
          else: 
            print(f"E4: P{process_i} - {index} - Empty - {url}")
        else: 
          print(f"E5: P{process_i} - {index} - Empty - {url}")

      driver.quit()
      print(f"P{process_i} - Data handled successfully!")
      return [
        df,
        pd.DataFrame(self.authors_in_thivien, columns=["Author"]),
        pd.DataFrame(self.authors_not_in_thivien, columns=["Author"])
      ]

    def handle(self, file_name):
        file_df = pd.read_csv(f'{file_name}.csv')
        print(f"==> Handling dataset... File: {file_name}.csv | Shape: {file_df.shape}")
        file_df['Genre'] = file_df['Genre'].astype('object')
        df_parts = helper.split_df(file_df, self.num_processes)
        
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            results = list(executor.map(self.fix_data, df_parts, range(self.num_processes)))

        df_results = [item[0] for item in results]
        df = pd.concat(df_results, ignore_index=True)
        df.to_csv(f"{file_name}_handled.csv", index=False, encoding="utf-8")
        
        ait_results = [item[1] for item in results]
        ait = pd.concat(ait_results, ignore_index=True).drop_duplicates()
        ait.to_csv("authors_in_thivien.csv", index=False, encoding="utf-8")
        
        anit_results = [item[2] for item in results]
        anit = pd.concat(anit_results, ignore_index=True).drop_duplicates()
        anit.to_csv("authors_not_in_thivien.csv", index=False, encoding="utf-8")
        
# if __name__ == "__main__":
#     scraper = PoemScraper(file_name="poems_dataset_proc0", driver_type="firefox", num_processes=1)
#     scraper.main()
