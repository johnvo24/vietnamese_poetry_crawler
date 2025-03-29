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

class DataCrawler:
  def __init__(self, driver_type="firefox", num_processes=1):
    self.num_processes = num_processes
    self.base_url = "https://www.thivien.net"
    self.driver_type = driver_type
    self.driver_path = {
        "firefox": "/snap/bin/geckodriver",
        "chrome": "C:/Webdriver/chromedriver-win64/chromedriver.exe"
    }
    
    self.poems_dataset_processed = pd.read_csv('handled_dataset/poems_dataset_processed.csv')
    self.authors_in_thivien = pd.read_csv('authors_in_thivien.csv')
    self.authors_for_searching = pd.merge(self.poems_dataset_processed, self.authors_in_thivien, on='Author', how='outer')
    self.authors_for_searching['Author'] = self.authors_for_searching['Author'].str.lower()
    self.authors_for_searching = self.authors_for_searching.sort_values(by=['Title'], ascending=False).drop_duplicates(subset=['Author'], keep='first')
  
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
  
  def crawl_data(self, start_author_, amount_, df_target_):
    data = []
    driver = self.get_driver()
    request_count = 0
    poem_count = 0
    started = False

    for _, author_row in self.authors_for_searching.iterrows():
      author = str(author_row['Author'])
      if not started:
        if author != start_author_:
          continue
        else:
          started = True 
      if request_count > 24:
        print(f"has a break time after 24 requests...")
        request_count = 0
        time.sleep(random.uniform(60, 120))
      
      # SEARCH AUTHOR WITH POEM
      author_url = f"https://www.thivien.net/searchpoem.php??Title={str(author_row['Title']).lower()}&Author={author}&ViewType=1&Country=2"
      driver.get(author_url)
      request_count += 1
      helper.delay()

      # Kiểm tra nếu bị chặn bởi CAPTCHA
      while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
        if "tần suất quá cao" in driver.page_source.lower():
          print("🔒 Bị chặn truy cập!!!")
          time.sleep(random.uniform(180, 240))
          ## Change proxy
          # driver.quit()
          # driver = self.get_driver()
        else:
          print("🔒 Phát hiện CAPTCHA!!!")
          time.sleep(random.uniform(60, 65))
        driver.get(author_url)
        request_count += 1
        helper.delay()

      author_soup = BeautifulSoup(driver.page_source, "html.parser")
      poems_of_author = author_soup.find_all("div", class_="list-item-detail")
      if len(poems_of_author) < 1:
        print(f"E1: Author not found: {author}")
        continue

      print(f"#####: Author: {author}")
      for poem in poems_of_author:
        a_tag = poem.find_all("a")[2]
        if a_tag.get_text().lower() != author: continue
        poem_author = a_tag.get_text()

        # SEARCH AUTHOR WITH AUTHOR URL
        driver.get(f"{self.base_url}/{a_tag['href']}")
        request_count +=1
        helper.delay()

        # Kiểm tra nếu bị chặn bởi CAPTCHA
        while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
          if "tần suất quá cao" in driver.page_source.lower():
            print("🔒 Bị chặn truy cập!!!")
            time.sleep(random.uniform(180, 240))
            ## Change proxy
            # driver.quit()
            # driver = self.get_driver()
          else:
            print("🔒 Phát hiện CAPTCHA!!!")
            time.sleep(random.uniform(60, 65))
          driver.get(f"{self.base_url}/{a_tag['href']}")
          request_count += 1
          helper.delay()
        
        # GET POEM
        author_page_soup = BeautifulSoup(driver.page_source, "html.parser")
        poem_group_lists = author_page_soup.find_all("div", class_="poem-group-list")

        translated_poem_group_title = [h4 for h4 in author_page_soup.find_all("h4", class_="poem-group-title") if "thơ dịch" in h4.get_text().lower()]
        if translated_poem_group_title: source_line_limit = translated_poem_group_title[0].sourceline;
        else: source_line_limit = 99999
        print(f"Line limit: {source_line_limit}")

        for poem_group_list in poem_group_lists:
          if poem_group_list.sourceline > source_line_limit: 
            print(f"WN: The line limit has been reached at {source_line_limit}.")
            break

          poem_tag_list = poem_group_list.find_all('a')
          for poem_tag in poem_tag_list:
            poem_title = poem_tag.get_text()
            if (poem_title.lower() in self.poems_dataset_processed["Title"].to_list()) or (poem_title in df_target_["Title"].to_list()): 
              print(f"E: {author} - {poem_title} is already!")
              continue

            poem_url = f"{self.base_url}/{poem_tag['href']}"
            driver.get(poem_url)
            request_count +=1
            helper.delay(5, 10)

            # Kiểm tra nếu bị chặn bởi CAPTCHA
            while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
              if "tần suất quá cao" in driver.page_source.lower():
                print("🔒 Bị chặn truy cập!!!")
                time.sleep(random.uniform(180, 240))
                ## Change proxy
                # driver.quit()
                # driver = self.get_driver()
              else:
                print("🔒 Phát hiện CAPTCHA!!!")
                time.sleep(random.uniform(60, 65))
              driver.get(poem_url)
              request_count += 1
              helper.delay()

            poem_soup = BeautifulSoup(driver.page_source, "html.parser")
            summary_section = poem_soup.find("div", class_="summary-section")
            if summary_section and summary_section.find("a"):
              poem_genre = summary_section.find("a").get_text()
              content_tag = poem_soup.find("div", class_="poem-content")
              if content_tag:
                data.append({
                    'Original': "",
                    'Edited': BeautifulSoup(content_tag.find('p').decode_contents().replace("<br/>", "\n"), "html.parser").get_text(),
                    'Title': poem_title,
                    'Genre': self.convert_poem_genre(poem_genre),
                    'Author': poem_author,
                    'URL': poem_url
                })
                poem_count += 1
                print(f"OK: {poem_count} - {author} - {poem_title}")
                if poem_count >= amount_:
                  driver.quit()
                  print(f"Data crawled successfully!")
                  return pd.DataFrame(data=data)
        break

    driver.quit()
    print(f"Data crawled successfully!")
    return pd.DataFrame(data=data)

  def start(self, start_author, num_loop=10, amount=250):
    print(f"==> Crawling dataset... ")
    start_author_ = start_author
    data_0 = []
    for i in range(0, num_loop):
      print(f"############### LOOP {i+1} ###############")
      try:
        data_0 = pd.read_csv(f"handled_dataset/poems_dataset_processed_0.csv")
      except ValueError:
        pass
      print(f"Dataset: {len(data_0)}")

      if len(data_0) > 0:
        start_author_ = str(data_0.iloc[-1]['Author']).lower()
      else:
        data_0 = pd.DataFrame(data=[])
      
      result = self.crawl_data(start_author_=start_author_, amount_=amount, df_target_=data_0)

      df = helper.merge_dataframes([data_0, result])
      df.to_csv(f"handled_dataset/poems_dataset_processed_0.csv", index=False, encoding="utf-8")
      print("ZZZ... Waiting for saving dataset")
      helper.delay(30, 35)
      
crawler = DataCrawler(driver_type="firefox", num_processes=1)
crawler.start(start_author='hư vô', num_loop=10, amount=500)
