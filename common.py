import os
import allure
import pytest
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Проверка URL: {expected_url}")
    def check_url(self, expected_url):
        assert self.driver.current_url == expected_url
        logging.info(
            f"Проверка URL: Ожидаемый URL - {expected_url}, "
            f"текущий URL - {self.driver.current_url}"
        )


class SbisHomePage(BasePage):
    URL = "https://sbis.ru/"

    @allure.step("Переход в раздел 'Контакты'.")
    def go_to_contacts(self):
        header_menu = self.driver.find_element(
            By.CLASS_NAME,
            "sbisru-Header__menu.ws-flexbox.ws-align-items-center"
        )
        contacts_link = header_menu.find_element(By.LINK_TEXT, "Контакты")
        contacts_link.click()
        logging.info("Переход на страницу 'Контакты' выполнен.")


@pytest.fixture
def browser():
    download_folder = os.path.join(os.path.dirname(__file__), 'downloads')

    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_folder,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'profile.default_content_settings.popups': 0
    })
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--safebrowsing-disable-download-protection')
    chrome_options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def close_cookie_message(driver, class_name):
    try:
        close_cookie_message = driver.find_element(By.CLASS_NAME, class_name)
        if close_cookie_message.is_displayed():
            close_cookie_message.click()
        logging.info("Закрытие сообщения о куки выполнено.")
    except NoSuchElementException:
        pass
