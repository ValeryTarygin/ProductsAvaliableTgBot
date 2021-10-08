from config import DRIVERPATH
from selenium import webdriver
from db import find_all_search, process_product

import os

class ParseProducts:
    def __init__(self, url, bot=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = find_all_search()

        for page in range(1, 2):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))

            try:
                products = self.driver.find_elements_by_class_name("catalog-item-in")
                for product in products:
                    text_for_analysis = product.text.lower()
                    for search_model in search_models:
                        if text_for_analysis.find(search_model.title.lower()) >= 0 and (text_for_analysis.find('купить') >= 0 or text_for_analysis.find('оформить') >= 0):
                            try: 
                                product_for_get_id = product.find_element_by_css_selector('.compare-item.compare-item--list.hidden-mv')
                                id = product_for_get_id.get_attribute('data-product-id')
                                name_class = 'product_url_{}'.format(id)
                                product_for_url = product.find_element_by_class_name(name_class)
                                product_href = product_for_url.get_attribute('href')
                                await process_product(text_for_analysis, product_href, search_model.chatid, self.bot)      
                            except:
                                continue
            except:
                continue
                                   
class ParseProductsDns:
    def __init__(self, url, bot=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_models = find_all_search()

        for page in range(1, 2):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))

            try:
                products = self.driver.find_elements_by_xpath("//div[@class='hype-landing-products__item hype-landing-products__item']");
                for product in products:
                    text_for_analysis = product.text.lower()
                    class_with_href = product.find_element_by_css_selector('.hype-landing-products__item-title');
                    product_href = class_with_href.get_attribute('href')
                    for search_model in search_models:
                        if text_for_analysis.find(search_model.title.lower()) >= 0:
                             await process_product(text_for_analysis, product_href, search_model.chatid, self.bot)  
            except:
                continue         
                        
                


         