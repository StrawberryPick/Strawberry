# getLink.py
# import selenium.common.exceptions.ElementClickInterceptedException as clickException
from selenium import webdriver
from parsel import Selector
import time

options = webdriver.ChromeOptions()
options.add_argument('--hl=en')

chromedrive_path = 'chromedriver.exe' # use the path to the driver you downloaded from previous steps

driver = webdriver.Chrome(chromedrive_path, chrome_options=options)

url = "https://www.google.com/maps/search/pick+your+own+farm+list/@45.1588331,-62.6316842,3z/data=!3m1!4b1"

driver.get(url)

time.sleep(10)
farm_list = list()
j = 0
while j < 50:
	j += 1
	# data = driver.find_elements_by_xpath(
	# 	'//div[@class="V0h1Ob-haAclf OPZbO-KE6vqe o0s21d-HiaYvf"]/a')\
	# 	.get_attribute('href')
	list_of_review= list()
	i = 0
	while (len(list_of_review) < 20) and (i < 5):

	    list_of_review = driver.find_elements_by_xpath(
	        '//div[@class="V0h1Ob-haAclf OPZbO-KE6vqe o0s21d-HiaYvf"]')
	    if not list_of_review:
	    	j = 50
	    	break
	    scrolling_element = list_of_review[-1]

	    driver.execute_script('arguments[0].scrollIntoView(true);',
	                                 scrolling_element)

	    time.sleep(2)
	    i += 1

	data = driver.find_elements_by_xpath(
		'//div[@class="V0h1Ob-haAclf OPZbO-KE6vqe o0s21d-HiaYvf"]/a')
	if not data:
		break
	data = [eachFarm.get_attribute("href") for eachFarm in data]
	print(f"Page {j}, we have {len(data)} farms")
	try:
		button = driver.find_elements_by_xpath('//div[@class="punXpd"]/button')[1]
		button.click()
		time.sleep(5)
	except:
		print("process end")
	farm_list += data
for each_link in farm_list:
	driver.get(each_link+"&hl=en")
	title = driver.find_element_by_xpath('//div[@class="x3AX1-LfntMc-header-title-ij8cu"]/div/h1/span').get_attribute("textContent")
	avg_rating = driver.find_element_by_xpath('//span[@class="aMPvhf-fI6EEc-KVuj8d"]').get_attribute("textContent")
	print(title, avg_rating)
	time.sleep(3)
	driver.find_element_by_xpath('//button[@class="Yr7JMd-pane-hSRGPd"]').click()
	time.sleep(3)
	
	# print()