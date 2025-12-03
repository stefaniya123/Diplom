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
        driver = self.driver

        # === ШАГ 1: Ждём кнопку "Купить" (гарантия, что страница загрузилась) ===

        buy_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
        )

        # Прокручиваем и кликаем
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
        driver.execute_script("arguments[0].click();", buy_button)

        # === ШАГ 2: Ждём появления формы "Оплата по карте" ===
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

    

