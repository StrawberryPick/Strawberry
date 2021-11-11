# scraper.py
from selenium import webdriver
from parsel import Selector
import time


class ScrapeReview:

    options = webdriver.ChromeOptions()
    options.add_argument('--hl=en')

    __chromedrive_path = 'chromedriver.exe' # use the path to the driver you downloaded from previous steps


    def __init__(self, URL):

        self.url = URL
        self.__driver = webdriver.Chrome(self.__chromedrive_path,
                                         chrome_options=self.options)
        self.__driver.get(self.url)
        
        time.sleep(20)

        data = self.__driver.find_element_by_xpath(
            '//div[@class="PPCwl"]/div/div[@class="jANrlb"]/div[contains(@class, "caption")]')\
            .get_attribute("textContent")\
            .replace(u'\xa0', u'')\
            .split(" ")[:-1]

        self.num_review = int("".join(data))
        self.results = list()


    def scrollingDown(self, maxData=300):

        assert maxData <= 300, "Your request data is too big"

        i = 0
        list_of_review = list()

        while (len(list_of_review) < self.num_review) and (i < (maxData // 10)):
            list_of_review = self.__driver.find_elements_by_xpath(
                '//div/div[@data-review-id]/div[contains(@class, "content")]')
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
                'review_id': el.xpath('.//div/div[@id]').attrib["id"],
                'date': el.xpath('.//div/div/span[contains(@class, "date")]/text()').extract_first(''),
                'rating': len(el.xpath('.//div/div/span/img[contains(@class, "active")]')),
                'body': el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
            })

        return self.results

scrapeObject = ScrapeReview("https://www.google.com/maps/place/Yrj%C3%B6l%C3%A4n+marjatila/@61.5727455,18.8113669,6z/data=!4m11!1m2!2m1!1spick+your+own+farm+list+Finland!3m7!1s0x468ed5492ac3ad73:0x2761843ae6ee82fc!8m2!3d61.5728671!4d23.2938096!9m1!1b1!15sCh9waWNrIHlvdXIgb3duIGZhcm0gbGlzdCBGaW5sYW5kWiEiH3BpY2sgeW91ciBvd24gZmFybSBsaXN0IGZpbmxhbmSSAQRmYXJtmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVJ4WjNSTFIyZEJSUkFC?hl=en&hl=en")
scrapeObject.scrollingDown(50)
results = scrapeObject.getReviewData()

print(results)
