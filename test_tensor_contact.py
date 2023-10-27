import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def check_url(self, expected_url):
        assert self.driver.current_url == expected_url


class SbisHomePage(BasePage):
    URL = "https://sbis.ru/"

    def go_to_contacts(self):
        header_menu = self.driver.find_element(
            By.CLASS_NAME,
            "sbisru-Header__menu.ws-flexbox.ws-align-items-center"
        )
        contacts_link = header_menu.find_element(By.LINK_TEXT, "Контакты")
        contacts_link.click()


class TensorPage(BasePage):
    def click_tensor_banner(self):
        tensor_banner = self.driver.find_element(
            By.CLASS_NAME,
            "sbisru-Contacts__logo-tensor"
        )
        tensor_banner.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def check_strength_in_people_block(self):
        try:
            self.driver.find_element(
                By.CSS_SELECTOR,
                'div.tensor_ru-Index__block4-content.tensor_ru-Index__card'
            )
        except NoSuchElementException:
            raise AssertionError("Блок 'Сила в людях' не найден на странице.")

    def go_to_strength_in_people_details(self):
        try:
            close_cookie_message = self.driver.find_element(
                By.CLASS_NAME,
                'tensor_ru-CookieAgreement__close'
            )
            close_cookie_message.click()
        except NoSuchElementException:
            pass

        strength_in_people_block = self.driver.find_element(
            By.XPATH,
            "//div[@class='tensor_ru-Index__block4-content "
            "tensor_ru-Index__card']"
        )
        details_link = strength_in_people_block.find_element(
            By.XPATH,
            ".//a[@href='/about']"
        )
        details_link.click()


class StrengthInPeopleDetailsPage(BasePage):
    def go_to_work_section(self):
        work_section = self.driver.find_element(By.LINK_TEXT, "Работаем")
        work_section.click()

    def check_photo_dimensions(self):
        photo_block = self.driver.find_element(
            By.XPATH,
            "//div[@class='tensor_ru-container "
            "tensor_ru-section tensor_ru-About__block3']"
        )
        photos = photo_block.find_elements(By.TAG_NAME, "img")

        first_photo = photos[0]
        reference_width = int(first_photo.get_attribute("width"))
        reference_height = int(first_photo.get_attribute("height"))

        for photo in photos[1:]:
            width = int(photo.get_attribute("width"))
            height = int(photo.get_attribute("height"))

            if width != reference_width or height != reference_height:
                assert False, (
                    f"Размеры фотографий не совпадают: "
                    f"({reference_width}, {reference_height}) и "
                    f"({width}, {height})"
                    )


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_tensor_contact_scenario(browser):
    sbis_home = SbisHomePage(browser)
    sbis_home.driver.get(SbisHomePage.URL)
    sbis_home.go_to_contacts()

    tensor_page = TensorPage(browser)
    tensor_page.click_tensor_banner()
    tensor_page.check_url("https://tensor.ru/")
    tensor_page.check_strength_in_people_block()
    tensor_page.go_to_strength_in_people_details()

    strength_in_people_details = StrengthInPeopleDetailsPage(browser)
    strength_in_people_details.check_url("https://tensor.ru/about")
    strength_in_people_details.check_photo_dimensions()


if __name__ == "__main__":
    pytest.main([__file__])
