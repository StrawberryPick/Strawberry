# scraper.py
from selenium import webdriver
from parsel import Selector
import time
import datetime as dt
import json as js
import os

script_dir = os.path.dirname(__file__)
print(script_dir)
class ScrapeReview:
    searchURL = "https://www.google.com/maps/search/"

    options = webdriver.ChromeOptions()
    options.add_argument('--hl=fi')

    __chromedrive_path = 'chromedriver.exe' # use the path to the driver you downloaded from previous steps

    def __init__(self, searchString):
        self.url = self.searchURL + "+".join(searchString.split(" "))

        self.__driver = webdriver.Chrome(self.__chromedrive_path,
                                         chrome_options=self.options)

        self.__driver.get(self.url)
        self.farmList = list()        
        self.results = list()
        self.num_review = 0
        time.sleep(10)

    def getFarmsLinks(self, maxPages):
        j = 0
        while j < maxPages:
            j += 1

            listOfReview= list()
            i = 0
            while (len(listOfReview) < 20) and (i < 5):

                listOfReview = self.__driver.find_elements_by_xpath(
                    f'//div[contains(@class,"OPZbO-KE6vqe")]')
                if (not listOfReview):
                    j = maxPages
                    break
                scrolling_element = listOfReview[-1]

                self.__driver.execute_script(
                    'arguments[0].scrollIntoView(true);', scrolling_element)

                time.sleep(2)
                i += 1

            data = self.__driver.find_elements_by_xpath(
                f'//div[contains(@class,"OPZbO-KE6vqe")]/a')
            if not data:
                break
            data = [eachFarm.get_attribute("href") for eachFarm in data]
            print(f"Page {j}, we have {len(data)} farms")
            try:
                button = self.__driver.find_elements_by_xpath(
                    '//div[@class="punXpd"]/button')[1]
                button.click()
                time.sleep(5)
            except:
                print("process end")
                break
            self.farmList += data

    def scrollingDown(self, maxData=300):

        assert maxData <= 500, "Your request data is too big"

        i = 0
        list_of_review = list()

        while (len(list_of_review) < self.num_review) and (i < (maxData // 10)):
            list_of_review = self.__driver.find_elements_by_xpath(
                '//div[@class="aopO7e-clz4Ic"]')[2:]
            if not list_of_review:
                time.sleep(3)
                continue

            scrolling_element = list_of_review[-1]
            self.__driver.execute_script('arguments[0].scrollIntoView(true);',
                                         scrolling_element)

            time.sleep(3)
            i += 1


    def getReviewData(self, reset=False):
        if (self.results) and (not reset):
            return self.results

        page_content = self.__driver.page_source
        response = Selector(page_content)

        self.results = []

        for el in response.xpath('//div/div[@data-review-id]/div[contains(@class, "content")]'):
            self.results.append({
                'title': el.xpath('.//div[contains(@class, "title")]/span/text()').extract_first(''),
                # 'review_id': el.xpath('.//div/div[@id]').attrib["id"],
                'date': el.xpath('.//div/div/span[contains(@class, "date")]/text()').extract_first(''),
                'rating': len(el.xpath('.//div/div/span/img[contains(@class, "active")]')),
                'body': el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
            })

        return self.results


    def downloadData(self, folderPath="data/"):
        # print()
        for i, eachLink in enumerate(self.farmList):

            self.__driver.get(eachLink + "&hl=en")
            try: 
                farmName = self.__driver.find_element_by_xpath(
                    '//div[@class="x3AX1-LfntMc-header-title-ij8cu"]/div/h1/span')\
                    .get_attribute("textContent")

                avgRating = self.__driver.find_element_by_xpath(
                    '//span[@class="aMPvhf-fI6EEc-KVuj8d"]')\
                    .get_attribute("textContent")

                print(farmName, avgRating)

                time.sleep(2)
                self.__driver.find_element_by_xpath('//button[@class="Yr7JMd-pane-hSRGPd"]').click()
                time.sleep(3)

                numReview = self.__driver.find_element_by_xpath(
                    '//div[@class="PPCwl"]/div/div[@class="jANrlb"]/div[contains(@class, "caption")]')\
                    .get_attribute("textContent")\
                    .replace(u'\xa0', u'')\
                    .split(" ")[:-1]

                numReview = int("".join(numReview))
                self.num_review = numReview

                self.scrollingDown(500)
                data = self.getReviewData(reset=True)

                jsonOutput = {
                    "farmName": farmName,
                    "avgRating": avgRating,
                    "numReview": numReview,
                    "createdAt": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    "data": data
                }
                fp = open(f"{folderPath}{i:03}.json", "w")
                js.dump(jsonOutput, fp)


                print(farmName, "has", len(data), "reviews")
            except Exception as e:
                 print(e)
# scrapeObject = ScrapeReview("https://www.google.com/maps/place/Yrj%C3%B6l%C3%A4n+marjatila/@61.5727455,18.8113669,6z/data=!4m11!1m2!2m1!1spick+your+own+farm+list+Finland!3m7!1s0x468ed5492ac3ad73:0x2761843ae6ee82fc!8m2!3d61.5728671!4d23.2938096!9m1!1b1!15sCh9waWNrIHlvdXIgb3duIGZhcm0gbGlzdCBGaW5sYW5kWiEiH3BpY2sgeW91ciBvd24gZmFybSBsaXN0IGZpbmxhbmSSAQRmYXJtmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJ4WjNSTFIyZEJSUkFC?hl=en&hl=en")
# scrapeObject.scrollingDown(50)
# results = scrapeObject.getReviewData()

# print(results)
searchObject1 = ScrapeReview("mansikkatila valitse oma listasi")
print("Something wrong")
searchObject1.getFarmsLinks(50)
searchObject1.downloadData(folderPath="./code/data/Finland/")