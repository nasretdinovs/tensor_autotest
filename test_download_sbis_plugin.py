import logging
import os
import re
import time

import allure
import pytest
import requests
from selenium.webdriver.common.by import By

from common import BasePage, browser, close_cookie_message
from utility.utils import remove_files_in_directory

root_logger = logging.getLogger()

logging.basicConfig(
    filename="test_log.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
root_logger.addHandler(console_handler)


class DownloadSBISPluginPage(BasePage):
    SBIS_URL = "https://sbis.ru/"
    DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'downloads')

    def get_file_size(self, file_path):
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        else:
            return 0

    @allure.step("Переход на страницу загрузки СБИС.")
    def go_to_download_sbis(self):
        driver = self.driver
        driver.get(self.SBIS_URL)
        footer = driver.find_element(
            By.CSS_SELECTOR, ".sbisru-Footer.sbisru-Header__scheme--default")

        close_cookie_message(self.driver, 'sbis_ru-CookieAgreement__close')
        download_link = footer.find_element(By.LINK_TEXT, "Скачать СБИС")
        download_link.click()
        time.sleep(2)
        logging.info("Переход на страницу загрузки СБИС выполнен")

    @allure.step("Загрузка плагина СБИС.")
    def download_sbis_plugin(self):
        driver = self.driver

        time.sleep(2)
        vertical_tabs = driver.find_element(
            By.XPATH,
            '//div[contains(@class, "sbis_ru-VerticalTabs__left")]'
        )
        sbis_plugin_button = vertical_tabs.find_element(
            By.XPATH,
            '//div[@class="controls-TabButton__caption" and '
            'text()="СБИС Плагин"]'
        )
        driver.execute_script("arguments[0].click();", sbis_plugin_button)
        logging.info("Выбран раздел 'СБИС Плагин'")

        time.sleep(2)
        tabcontrol = driver.find_element(
            By.CLASS_NAME, "controls-TabControl-tabButtons")
        windows_tab = tabcontrol.find_element(
            By.XPATH,
            '//span[contains(@class, '
            '"sbis_ru-DownloadNew-innerTabs__title--default") and '
            'text()="Windows"]'
        )
        windows_tab.click()

        logging.info("Выбрана платформа 'Windows'")

        switchable_area = self.driver.find_element(
            By.CLASS_NAME, "ws-SwitchableArea__item")
        exe_link = switchable_area.find_element(
            By.XPATH, '//a[contains(text(), "Exe")]')

        download_url = exe_link.get_attribute("href")
        downloaded_file_path = os.path.join(
            self.DOWNLOAD_PATH, "sbisplugin-setup-web.exe")

        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Ошибка при скачивании файла: {str(e)}")

        with open(downloaded_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        logging.info("Файл успешно скачан")
        assert os.path.exists(
            downloaded_file_path), f"Файл не найден: {downloaded_file_path}"
        return downloaded_file_path


@allure.feature("Загрузка плагина СБИС")
@allure.story("Загрузка плагина для Windows")
@allure.severity(allure.severity_level.NORMAL)
def test_download_sbis_plugin(browser):
    download_page = DownloadSBISPluginPage(browser)
    download_page.go_to_download_sbis()
    download_folder = os.path.join(os.path.dirname(__file__), 'downloads')
    remove_files_in_directory(download_folder)
    downloaded_file = download_page.download_sbis_plugin()

    switchable_area = download_page.driver.find_element(
        By.CLASS_NAME, "ws-SwitchableArea__item")
    exe_link = switchable_area.find_element(
        By.XPATH, '//a[contains(text(), "Exe")]')
    exe_link_text = exe_link.text
    size_match = re.search(r'(\d+(\.\d+)?)\s+МБ', exe_link_text)
    if size_match:
        expected_size_mb = float(size_match.group(1))
    else:
        raise AssertionError(
            "Не удалось извлечь размер из текста ссылки на файл Exe")

    downloaded_size = download_page.get_file_size(
        downloaded_file) / (1024 * 1024)

    assert (
        abs(downloaded_size - expected_size_mb) < 0.01
    ), f"Неверный размер файла: {downloaded_size} МБ"
    logging.info(
        f"Размер файла совпадает с ожидаемым: {round(downloaded_size, 2)} МБ")
    remove_files_in_directory(download_folder)


if __name__ == "__main__":
    pytest.main([__file__, "--alluredir=./allure-results"])
