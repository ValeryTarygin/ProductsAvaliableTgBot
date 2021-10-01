from config import DRIVERPATH, URL
from selenium import webdriver
from db import find_all_search, process_product


class ParseProducts:
    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVERPATH)
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


            products = self.driver.find_elements_by_class_name("catalog-item-in")
            for product in products:
                text_for_analysis = product.text
                for search_model in search_models:
                     if text_for_analysis.find(search_model.title) >= 0 and (text_for_analysis.find('Купить') >= 0 or text_for_analysis.find('Оформить заказ') >= 0):
                        try: 
                            product_for_get_id = product.find_element_by_css_selector('.compare-item.compare-item--list.hidden-mv')
                            id = product_for_get_id.get_attribute('data-product-id')
                            name_class = 'product_url_{}'.format(id)
                            product_for_url = product.find_element_by_class_name(name_class)
                            product_href = product_for_url.get_attribute('href')
                            await process_product(text_for_analysis, product_href, search_model.chatid, self.bot)      
                        except SomeSpecificException:
                            continue
                                   
                        
                


         