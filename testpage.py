from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging
import yaml
import requests


class TestSearchLocators:  # класс для хранения локаторов
    ids = dict()
    with open("./locators.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():  # обращаемся к ключам в файле с локаторами из раздела   'xpath'
        ids[locator] = (By.XPATH, locators["xpath"][locator])
    for locator in locators["css"].keys():  # обращаемся к ключам в файле с локаторами из раздела   'xpath'
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationsHelper(BasePage):  # класс OperationsHelper наследуется от BasePage

    def enter_text_into_field(self, locator, word, description=None):
        if description:  # если есть description
            element_name = description  # кладем в переменную
        else:  # если нет description
            element_name = locator  # локатор в имя переменной
            logging.debug(f'Send {word} to element {element_name}')
        field = self.find_element(locator)  # ищем элемент
        if not field:  # если не нашли, выводим ошибку
            logging.error(f"Element {locator} not found")
            return False
        try:  # если нашли, очищаем и заполняем
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f'Exception while operate with {locator}')
            return False
        return True

    def click_button(self, locator, description=None):
        if description:  # если есть description
            element_name = description  # кладем в переменную
        else:  # если нет description
            element_name = locator  # локатор в имя переменной
        button = self.find_element(locator)  # ищем элемент
        if not button:  # если не нашли, выводим ошибку
            return False
        try:
            button.click()
        except:
            logging.exception('Exception with click')
            return False
        logging.debug(f'Clicked {element_name} button')
        return True

    def get_text_from_element(self, locator, description=None):
        if description:  # если есть description
            element_name = description  # кладем в переменную
        else:  # если нет description
            element_name = locator  # локатор в имя переменной
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f"Exception while get text from {element_name}")
            return None
        logging.debug(f'We found text {text} in field {element_name}')
        return text


    def enter_login(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word, description='login_form')


    def enter_pass(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word, description='password_form')


    def enter_name(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_NAME_FIELD'], word, description='enter_name')


    def enter_email(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_EMAIL_FIELD'], word, description='enter_emai')


    def enter_content(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_CONTENT_FIELD'], word, description='enter_content')

    # get text


    def get_error_text(self):
        self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'], description='error label')



    def click_contact_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_CONTACT'], description='contact')


    def click_contact_us_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_US_BUTTON'], description='send')


    def click_login_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'], description='login')
