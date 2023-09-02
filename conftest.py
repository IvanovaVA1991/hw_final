import pytest, yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # импорт сервиса для хрома
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager  # импорт модулей для firwfox и chrome
import requests

with open('./testdata.yaml') as f:
    testdata = yaml.safe_load(f)
    browser = testdata['browser']


@pytest.fixture(scope='session')  # фикстура  с параметром, будет действовать всю сессию
def browser():  # инициализация
    if browser == 'firefox':
        service = Service(executable_path=GeckoDriverManager().install())  # автоматически скачивать  и устанавливать нужный вебдрайвер менеджер
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)  # инициализация драввйреа
        yield driver
        driver.quit()  # закрытие браузера

@pytest.fixture()
def login():   # залогиниться с использованием логина и пароля
    obj_data = requests.post(url=testdata['url2'], data={'username': testdata['login'], 'password': testdata['passwd']}) # сложили в переменную объект ответа
    token = obj_data.json()['token']  # достали токен из ответа
    return token
