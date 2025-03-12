from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import random
import helper

NUM_PROCESSES = 2                                   # <==== CHANGE IT
GECKO_DRIVER_PATH = '/snap/bin/geckodriver'
FILE_NAME = 'poems_dataset_proc0_3'
BASE_URL = "https://www.thivien.net"
file_df = pd.read_csv(f'{FILE_NAME}.csv')
authors_not_in_thivien = pd.read_csv('authors_not_in_thivien.csv')["Author"].to_list()
authors_in_thivien = pd.read_csv('authors_in_thivien.csv')["Author"].to_list()

def get_firefox_driver():
	options = Options()
	options.headless = True
	service = Service(GECKO_DRIVER_PATH)
	return webdriver.Firefox(service=service, options=options)

def convert_poem_genre(genre):
	if genre.lower() == "thơ mới bốn chữ": target = "Bốn chữ"
	elif genre.lower() == "thơ mới năm chữ": target = "Năm chữ"
	elif genre.lower() == "thơ mới sáu chữ": target = "Sáu chữ"
	elif genre.lower() == "thơ mới bảy chữ": target = "Bảy chữ"
	elif genre.lower() == "thơ mới tám chữ": target = "Tám chữ"
	elif genre.lower() == "thơ tự do": target = "Tự do"
	else: target = genre
	return target

def fix_data(df, process_i):
	driver = get_firefox_driver()
	request_count = 0

	for index, poem in df.iterrows():
		if not pd.isna(poem["Genre"]): 
			print(f"P{process_i} - {index} - Existed")
			continue

		if str(poem['Author']).lower() in authors_not_in_thivien:
			print(f"ER01: P{process_i} - {index} - Author not found: {str(poem['Author']).lower()}")
			continue
		elif str(poem['Author']).lower() not in authors_in_thivien:
			# SEARCH AUTHOR
			driver.get(f"https://www.thivien.net/searchpoem.php?Author={str(poem['Author']).lower()}&ViewType=1&Country=2")
			request_count += 1
			time.sleep(random.uniform(5, 8))
			author_soup = BeautifulSoup(driver.page_source, "html.parser")
			poems_of_author = author_soup.find_all("h4", class_="list-item-header")
			if len(poems_of_author) < 1:
				print(f"ER02: P{process_i} - {index} - Author not found: {str(poem['Author']).lower()}")
				authors_not_in_thivien.append(str(poem['Author']).lower())
				continue
			else: authors_in_thivien.append(str(poem['Author']).lower())
			
		if request_count%20 == 0 and request_count > 0:
			print("Rotate proxy after 15 requests...")
			# driver.quit()
			# driver = get_firefox_driver()
			time.sleep(random.uniform(80, 120))

		# SEARCH AUTHOR AND POEM
		url = f"https://www.thivien.net/searchpoem.php?Title={str(poem['Title']).lower()}&Author={str(poem['Author']).lower()}&ViewType=1&Country=2"
		driver.get(url)
		request_count += 1
		time.sleep(random.uniform(5, 8))

		# Kiểm tra nếu bị chặn bởi CAPTCHA
		while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
			if "tần suất quá cao" in driver.page_source.lower():
				print("🔒 Bị chặn truy cập!!!")
				time.sleep(random.uniform(300, 360))
			else:
				print("🔒 Phát hiện CAPTCHA!!!")
				time.sleep(random.uniform(60, 65))
			## Change proxy
			# driver.quit()
			# driver = get_firefox_driver()
			driver.get(url)
			request_count += 1
			time.sleep(random.uniform(5, 8))
		
		html = driver.page_source
		soup = BeautifulSoup(html, "html.parser")
		
		poem_links = soup.find_all("h4", class_="list-item-header")
		if len(poem_links) < 1:
			print(f"ER03: P{process_i} - {index} - Empty - {url}")
			continue
		
		a_tag = None
		for idx, h4_tag in enumerate(poem_links, start=1):
			a_tg = h4_tag.find('a')
			if a_tg.get_text().lower() == str(poem["Title"]).lower():
				a_tag = a_tg
				break
		if a_tag:
			poem_url = BASE_URL + a_tag['href']
			driver.get(poem_url)
			request_count += 1
			time.sleep(random.uniform(2, 4))

			# Kiểm tra nếu bị chặn bởi CAPTCHA
			while "xác nhận không phải máy" in driver.page_source.lower() or "tần suất quá cao" in driver.page_source.lower():
				if "tần suất quá cao" in driver.page_source.lower():
					print("🔒 Bị chặn truy cập!!!")
					time.sleep(random.uniform(300, 360))
				else:
					print("🔒 Phát hiện CAPTCHA!!!")
					time.sleep(random.uniform(60, 65))
				## Change proxy
				# driver.quit()
				# driver = get_firefox_driver()
				driver.get(url)
				request_count += 1
				time.sleep(random.uniform(5, 8))

			poem_soup = BeautifulSoup(driver.page_source, "html.parser")
			summary_section = poem_soup.find("div", class_="summary-section")
			if summary_section:
				poem_genre = summary_section.find("a").get_text()
				content_tag = poem_soup.find("div", class_="poem-content")

				df.at[index, "Genre"] = convert_poem_genre(poem_genre)
				df.at[index, "Edited"] = BeautifulSoup(content_tag.find('p').decode_contents().replace("<br/>", "\n"), "html.parser").get_text()

				print(f"P{process_i} - {index} - {poem['Title']} - {url}")
			else: 
				print(f"ER04: P{process_i} - {index} - Empty - {url}")
		else: 
			print(f"ER05: P{process_i} - {index} - Empty - {url}")

	driver.quit()
	print(f"P{process_i} - Data handled successfully!")
	return df
	

def main():
	print(f"DATA SHAPE: {file_df.shape}")
	file_df['Genre'] = file_df['Genre'].astype('object')
	df_parts = helper.split_df(file_df, NUM_PROCESSES)

	with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
		df_results = list(executor.map(fix_data, df_parts, range(NUM_PROCESSES)))

	df = pd.concat(df_results, ignore_index=True)
	df.to_csv(f"{FILE_NAME}_handled.csv", index=False, encoding="utf-8")
	
if __name__ == "__main__":
	main()