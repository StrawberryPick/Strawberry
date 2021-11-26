# rainPredictionScraper.py

from selenium import webdriver
import time

import datetime as dt
import json as js

class RainPredictionScraper:
	url_form = "https://www.foreca.fi/{}/{}/details/"
	__chromedrive_path = '../chromedriver.exe'


	def __init__(self, city, country="Finland"):
		self.city = city
		self.country = country

		self.url = self.url_form.format(country, city)
		self.today = dt.datetime.utcnow()
		self.__driver = webdriver.Chrome(self.__chromedrive_path)
		self.result = {
			"city": city,
			"country": country,
			"createdAt": self.today.strftime("%Y-%m-%dT%H:%M:%S"),
			"data": list()
		}


	def downloadData(self, date):
		url = self.url + date
		self.__driver.get(url)

		rainClass = self.__driver.find_elements_by_xpath('//div[@class="p" or @class="sff"]')[1:]
		hourClass = self.__driver.find_elements_by_xpath('//div[@class="h"]/p')
		tempClass = self.__driver.find_elements_by_xpath('//div[@class="t warm" or @class="t cold"]')
		moistureClass = self.__driver.find_elements_by_xpath('//div[@class="rh"]')[1:]

		total_rain_id, chance_rain_06_18, chance_rain_18_06 = 0, 7, 20
		if len(rainClass) < 27:
			chance_rain_06_18, chance_rain_18_06 = [
				i + 1 for i in range(len(rainClass[1:])) if ("%" in rainClass[i+1].text)
			]

		data = dict()
		data["date"] = date
		data["sunHour"] = self.__driver.find_element_by_xpath('//p[@class="daylen"]').text
		data["sunUp"] = self.__driver.find_element_by_xpath('//p[@class="sunup"]').text
		data["sunDown"] = self.__driver.find_element_by_xpath('//p[@class="sundown"]').text
	
		
		numContent = len(rainClass)

		i = 0
		h = 0
		t = 0
		m = 0
		data['data'] = list()
		while i < numContent:
			# print(i)
			if i == total_rain_id:
				data["totalRain"] = rainClass[i].text
				pass
			elif i == chance_rain_06_18:
				data["chance_rain_06_18"] = rainClass[i].text
				pass
			elif i == chance_rain_18_06:
				data["chance_rain_18_06"] = rainClass[i].text
				pass
			else:
				data['data'].append({
					"hour":hourClass[h].text,
					"rainAmount": rainClass[i].text,
					"temperature": tempClass[t].text,
					"moisture": moistureClass[m].text
					})
				h += 1
				t += 1
				m += 1
			i += 1

		self.result['data'].append(data)

		return True
	
	def getData(self):
		return self.result

	def closeAll(self):
		self.__driver.close()

	def saveData(self, path):
		fileName = f"{self.country}_{self.city}_{self.today.strftime('%Y%m%d')}.json"

		fp = open(path + fileName, "w")
		js.dump(self.result, fp)
