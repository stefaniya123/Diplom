# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.cards import APPROVED_CARD


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("http://localhost:8080")
        print("Загружена страница:", self.driver.title)
        print("URL:", self.driver.current_url)

    def select_debit(self):
        wait = WebDriverWait(self.driver, 30)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Купить']]"))
        )
        button.click()

        # Ждём появления первого поля формы
        wait.until(
            EC.presence_of_element_located((By.XPATH, "(//input[@class='input__control'])[1]"))
        )

    def fill_card_number(self, number):
        wait = WebDriverWait(self.driver, 25)
        card_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Номер карты']/following::input[@class='input__control']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_field)
        card_field.clear()
        card_field.send_keys(number)

    def fill_month(self, month):
        month_field = self.driver.find_element(By.XPATH, "//span[text()='Месяц']/following::input[@class='input__control']")
        month_field.clear()
        month_field.send_keys(month)

    def fill_year(self, year):
        year_field = self.driver.find_element(By.XPATH, "//span[text()='Год']/following::input[@class='input__control']")
        year_field.clear()
        year_field.send_keys(year)

    def fill_owner(self, owner):
        owner_field = self.driver.find_element(By.XPATH, "//span[text()='Владелец']/following::input[@class='input__control']")
        owner_field.clear()
        owner_field.send_keys(owner)

    def fill_cvc(self, cvc):
        cvc_field = self.driver.find_element(By.XPATH, "//span[text()='CVC/CVV']/following::input[@class='input__control']")
        cvc_field.clear()
        cvc_field.send_keys(cvc)

    def submit(self):
        wait = WebDriverWait(self.driver, 30)  # Создаём локальный wait
        submit_button = wait.until(  # Используем локальный wait, а не self.wait
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_view_extra.button_theme_alfa-on-white"))
        )
        # Прокручиваем к кнопке
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
        # Нажимаем через JavaScript
        self.driver.execute_script("arguments[0].click();", submit_button)

    def wait_for_success_message(self):
        wait = WebDriverWait(self.driver, 25)
        return wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//div[contains(@class, 'notification_status_ok')]//div[contains(@class, 'notification_content')]"))
        )

    def wait_for_error_message(self):
        wait = WebDriverWait(self.driver, 25)
        return wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'notification_status_error')]"))
        )

    # В тесте используйте конкретное ожидание
    def test_debit_payment_success(browser):
        page = MainPage(browser)
        page.open()
        page.select_debit()
        page.fill_card_number(APPROVED_CARD)
        page.fill_month("08")
        page.fill_year("26")
        page.fill_owner("Ivan Ivanov")
        page.fill_cvc("999")
        page.submit()

        # Ждём именно успешное сообщение
        message = page.wait_for_success_message()
        assert "Операция одобрена Банком." in message.text