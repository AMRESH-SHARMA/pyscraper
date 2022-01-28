from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def scrape_pages(url):
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	browser.get(url)
	see_more=True
	while see_more:
		try:
			see_more=browser.find_element(By.CLASS_NAME, 'loadlist')
			see_more.click()
		except:
			see_more=False
		time.sleep(5)
	source=browser.page_source
	soup=BeautifulSoup(source,'lxml')
	lists=soup.find_all('li',{'class':'list-item view-r'})
	currenttime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	file_name = f"output/Sulekha_{url_text.split('/')[-2]}_{url_text.split('/')[-1]}_{currenttime}.csv"
	fields = ['Name', 'Phone', 'Address','City',"Industry","Pincode"]
	out_file = open(file_name,'w', newline='')
	csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
	csvwriter.writeheader()
	details={}
	ctr=0
	for li in lists:
		ctr+=1
		try:
			name=li.get('data-name')
		except:
			name='Not Found'
		try:

			phone=li.get('data-bvn')
		except:
			phone='Not Found'
		try:

			address=li.find('address').text
		except:
			address='Not Found'
		try:
			city = li.get('data-city')
		except:
			city = url.split('/')[-1]
		try:
			industry = li.find('p',{'class': 'icon-tag f-icon'}).text
		except:
			industry = url.split('/')[-2].replace('-', ' ')
		try:
			pin = li.get('data-pincode')
		except:
			pin = url.split('/')[-1]
		details['Name']=name
		details['Phone']=phone
		details['Address']=address
		details['City'] = city
		details['Industry'] = industry
		details['Pincode'] = pin
		try:
			csvwriter.writerow(details)
			print(ctr)
			print(details['Name'])
		except:
			print(ctr)
			print('Error in writing')


with open('input.txt', 'r') as input_file:
	url_list = input_file.read().splitlines()
	x = 1
	for url_text in url_list:
		url_text.replace('\n', '')
		print(f"URL {x}: {url_text}, Scraping Started")
		scrape_pages(url_text)
		print(f"URL {x}: {url_text}, Scraping Completed")
		x += 1