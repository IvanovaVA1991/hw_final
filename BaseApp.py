from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import logging


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://test-stand.gb.ru"
        self.url1 = 'https://test-stand.gb.ru/api/posts'

    def find_element(self, locator, time=10):  # метод поиска элементов, передаем путь, время ожидания
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator), message=f'Cant find element by locator {locator}')  # ждать, пока не появится элемент, если не находится, то выходит ошибка Can't find element by locator {locator}
        except:
            logging.exception('Find element exception')
            element = None
        return element

    def get_element_property(self, locator, property):
        element = self.find_element(locator)
        if element:
            return element.element.value_of_css_property(property)
        else:
            logging.error(f'Property {property} not found in element with locator {locator}')
            return None

    def go_to_site(self):  # метод для открытия сайта
        try:
            start_browsing = self.driver.get(self.base_url)
        except:
            logging.exception('Exception with open site')
            start_browsing = None
        return start_browsing

    def get_alert_text(self):
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            logging.exception('Exception with alert')
            return None

    def get_content_post(self, token):
        try:
            response = requests.get(url=self.url1, headers={'X-Auth-Token': token}, params={"owner": "notMe"})  # get запрос c хедером, содержащим токен авторизации в параметре "X-Auth-Token"
            content_var = [item['content'] for item in response.json()['data']]  # через генератор создали список постов (сам контент)
            return content_var  # возвращаем список постов
        except:
            logging.exception('No posts found')
            return None