from testpage import OperationsHelper
import time
import yaml
import requests
import logging


with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)


def test_step1(browser):
    logging.info('Test1 Starting')  # лог
    testpage = OperationsHelper(browser)  # создание экзепляра класса OperationsHelper с передачей браузера
    testpage.go_to_site()  # открываем страницу
    testpage.enter_login('test')  # вводим логин
    testpage.enter_pass('test')  # вводим пароль
    testpage.click_login_button()  # кликаем кнопку
    assert testpage.get_error_text() == '401'


def test_step2(browser):
    testpage = OperationsHelper(browser)  # создание экзепляра класса OperationsHelper с передачей браузера
    testpage.go_to_site()  # открываем страницу
    testpage.enter_login(f"{testdata['login']}")  # вводим логин
    testpage.enter_pass(f"{testdata['passwd']}")  # вводим пароль
    testpage.click_login_button()  # кликаем кнопку
    testpage.click_contact_button()
    testpage.enter_name(f"{testdata['name']}")
    testpage.enter_email(f"{testdata['email']}")
    testpage.enter_content(f"{testdata['content1']}")
    time.sleep(testdata['sleep_time'])
    testpage.click_contact_us_button()
    time.sleep(testdata['sleep_time'])
    assert testpage.get_alert_text() == 'Form successfully submitted'


def test_api_create_post(login):
    obj_data = requests.post(url=testdata['url2'], data={'username': testdata['login'], 'password': testdata['passwd']})
    token = obj_data.json()['token']
    post = requests.post(url=testdata['url1'], headers={'X-Auth-Token': token}, params={'title': testdata['title'], 'description': testdata['description'], 'content': testdata['content']})
    my_post = post.json()['description']
    assert 'beautiful' in my_post

