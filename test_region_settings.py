import logging

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import BasePage, SbisHomePage, browser

root_logger = logging.getLogger()

MY_REGION = "г. Москва"

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


class SbisContactsPage(BasePage):
    @allure.step("Проверка региона и наличия списка партнеров")
    def check_region_and_partners(self, expected_region):
        region_element = self.driver.find_element(
            By.XPATH,
            '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]'
        )
        current_region = region_element.text
        assert current_region == MY_REGION, (
            f"Ожидаемый регион: {current_region}, "
            f"Фактический регион: {MY_REGION}"
        )
        logging.info(
            f"Проверка региона: Ожидаемый регион - {current_region}, "
            f"фактический регион - {MY_REGION}"
        )

        contacts_list = self.driver.find_element(
            By.CSS_SELECTOR, '#contacts_list')
        address_elements = contacts_list.find_elements(
            By.CSS_SELECTOR, '.sbisru-Contacts-List__item')
        assert len(address_elements) > 0, "Адреса отсутствуют"
        logging.info("Проверка наличия списка партнеров выполнена.")

    @allure.step("Изменение региона на Камчатский край")
    def change_region_to_kamchatka(self, expected_region):

        contacts_list = self.driver.find_element(
            By.CSS_SELECTOR, '#contacts_list')
        address_elements_before = contacts_list.find_elements(
            By.CSS_SELECTOR, '.sbisru-Contacts-List__item')
        address_count_before = len(address_elements_before)

        region_dropdown = self.driver.find_element(
            By.CLASS_NAME, "sbis_ru-Region-Chooser")
        region_dropdown.click()
        logging.info("Клик по ссылке выбора региона выполнен.")

        wait = WebDriverWait(self.driver, 10)
        region_panel = wait.until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "sbis_ru-Region-Panel__container"))
        )

        kamchatka_option = region_panel.find_element(
            By.XPATH,
            '//li[@class="sbis_ru-Region-Panel__item"]'
            '/span[text()="41 Камчатский край"]'
        )
        kamchatka_option.click()
        logging.info("Клик по региону Камчатский край выполнен.")

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_contains("kamchatskij-kraj"))

        region_element = self.driver.find_element(
            By.XPATH,
            '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]'
        )
        selected_region = region_element.text
        assert selected_region == "Камчатский край", (
            f"Ожидаемый регион: Камчатский край, "
            f"Фактический регион: {selected_region}"
        )
        logging.info(
            f"Проверка региона: Ожидаемый регион: Камчатский край, "
            f"Фактический регион: {selected_region}"
        )

        address_elements_after = contacts_list.find_elements(
            By.CSS_SELECTOR, '.sbisru-Contacts-List__item')
        address_count_after = len(address_elements_after)
        assert address_count_after > 0, "Адреса отсутствуют"
        logging.info("Проверка наличия списка партнеров выполнена.")
        assert address_count_after != address_count_before, (
            "Количество элементов в списке адресов не изменилось")
        logging.info(
            f"Смена региона привела к изменению списка адресов. "
            f"Количество до: {address_count_before}, "
            f"количество после: {address_count_after}"
        )

        current_url = self.driver.current_url
        expected_url = "https://sbis.ru/contacts/41-kamchatskij-kraj"
        assert current_url.startswith(expected_url), (
            f"Неверный URL. Ожидается начало: {expected_url}")
        logging.info("Проверка URL.")

        current_title = self.driver.title
        assert "Камчатский край" in current_title, "Неверный Title"
        logging.info("Проверка title.")

        region_element = self.driver.find_element(
            By.XPATH,
            '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]'
        )
        current_region = region_element.text
        assert current_region == "Камчатский край", (
            f"Ожидаемый регион: Камчатский край, "
            f"Фактический регион: {current_region}"
        )
        logging.info(
            f"Проверка региона: Ожидаемый регион: Камчатский край, "
            f"Фактический регион: {current_region}"
        )


def test_sbis_contacts_scenario(browser):
    sbis_home = SbisHomePage(browser)
    sbis_home.driver.get(SbisHomePage.URL)
    sbis_home.go_to_contacts()

    contacts_page = SbisContactsPage(browser)
    contacts_page.check_region_and_partners("Ярославская обл.")
    contacts_page.change_region_to_kamchatka("Камчатский край")


if __name__ == "__main__":
    pytest.main([__file__, "--alluredir=./allure-results"])
