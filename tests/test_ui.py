import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestSuccessfulPurchase(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("http://localhost:8080")

    def test_successful_card_purchase(self):
        """Тест для покупки по карте"""
        driver = self.driver

        # === ШАГ 1: Ждём кнопку "Купить" ===
        buy_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
        driver.execute_script("arguments[0].click();", buy_button)

        # === ШАГ 2: Ждём формы "Оплата по карте" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
        )

        # === ШАГ 3: Заполняем поля ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("08")                   # Месяц
        inputs[2].send_keys("26")                   # Год
        inputs[3].send_keys("иван")                 # Владелец
        inputs[4].send_keys("999")                  # CVC

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём, пока кнопка станет disabled и изменит текст на "Отправляем запрос в Банк..." ===
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "button.button_view_extra.button_size_m.button_theme_alfa-on-white.button_disabled .button__text"),
                "Отправляем запрос в Банк..."
            )
        )

        # === ШАГ 6: Ждём появления уведомления "Успешно Операция одобрена банком" ===
        title_element = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
        )
        assert title_element.text.strip() == "Успешно", f"Неверный заголовок: '{title_element.text}'"

        content_element = driver.find_element(By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__content")
        assert "Операция одобрена Банком." in content_element.text.strip(), f"Неверное содержимое: '{content_element.text}'"


    def test_successful_credit_purchase(self):
        """Тест для покупки в кредит"""
        driver = self.driver

        # === ШАГ 1: Ждём и нажимаем кнопку "Купить в кредит" ===
        # Ищем кнопку по тексту "Купить в кредит"
        credit_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
        driver.execute_script("arguments[0].click();", credit_button)

        # === ШАГ 2: Ждём формы "Кредит по данным карты" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
        )

        # === ШАГ 3: Заполняем поля (такие же, как и в первом тесте) ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("08")                   # Месяц
        inputs[2].send_keys("26")                   # Год
        inputs[3].send_keys("иван")                 # Владелец
        inputs[4].send_keys("999")                  # CVC

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" (та же логика) ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём, пока кнопка станет disabled и изменит текст на "Отправляем запрос в Банк..." ===
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "button.button_view_extra.button_size_m.button_theme_alfa-on-white.button_disabled .button__text"),
                "Отправляем запрос в Банк..."
            )
        )

        # === ШАГ 6: Ждём появления уведомления "Успешно Операция одобрена банком" ===
        title_element = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
        )
        assert title_element.text.strip() == "Успешно", f"Неверный заголовок: '{title_element.text}'"

        content_element = driver.find_element(By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__content")
        assert "Операция одобрена Банком." in content_element.text.strip(), f"Неверное содержимое: '{content_element.text}'"


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()