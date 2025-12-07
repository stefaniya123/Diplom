import unittest
from selenium import webdriver
from selenium.common import TimeoutException
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


    def test_invalid_card_fields(self):
        """Тест: попытка отправить форму с пустыми полями (покупка по карте)"""
        driver = self.driver

        # === ШАГ 1: Ждём и нажимаем кнопку "Купить" ===
        buy_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
        driver.execute_script("arguments[0].click();", buy_button)

        # === ШАГ 2: Ждём формы "Оплата по карте" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
        )

        # === ШАГ 3: НЕ ЗАПОЛНЯЕМ ПОЛЯ — оставляем их пустыми ===

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления сообщений об ошибках под каждым полем ===
        error_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
        )

        # Проверяем количество ошибок (должно быть 5)
        self.assertEqual(len(error_elements), 5, "Должно быть 5 сообщений об ошибках")

        # Проверяем текст каждого сообщения
        expected_error_texts = [
            "Неверный формат",     # Номер карты
            "Неверный формат",     # Месяц
            "Неверный формат",     # Год
            "Поле обязательно для заполнения",  # Владелец
            "Неверный формат"      # CVC
        ]

        for i, error_element in enumerate(error_elements):
            actual_text = error_element.text.strip()
            expected_text = expected_error_texts[i]
            self.assertEqual(actual_text, expected_text,
                             f"Ошибка в поле {i+1}: ожидается '{expected_text}', получено '{actual_text}'")


    def test_invalid_credit_fields(self):
        """Тест: попытка отправить форму с пустыми полями (покупка в кредит)"""
        driver = self.driver

        # === ШАГ 1: Ждём и нажимаем кнопку "Купить в кредит" ===
        credit_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
        driver.execute_script("arguments[0].click();", credit_button)

        # === ШАГ 2: Ждём формы "Кредит по данным карты" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
        )

        # === ШАГ 3: НЕ ЗАПОЛНЯЕМ ПОЛЯ — оставляем их пустыми ===

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления сообщений об ошибках под каждым полем ===
        error_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
        )

        # Проверяем количество ошибок (должно быть 5)
        self.assertEqual(len(error_elements), 5, "Должно быть 5 сообщений об ошибках")

        # Проверяем текст каждого сообщения
        expected_error_texts = [
            "Неверный формат",     # Номер карты
            "Неверный формат",     # Месяц
            "Неверный формат",     # Год
            "Поле обязательно для заполнения",  # Владелец
            "Неверный формат"      # CVC
        ]

        for i, error_element in enumerate(error_elements):
            actual_text = error_element.text.strip()
            expected_text = expected_error_texts[i]
            self.assertEqual(actual_text, expected_text,
                             f"Ошибка в поле {i+1}: ожидается '{expected_text}', получено '{actual_text}'")

    def test_expired_year_card(self):
        """Тест: истекший год (покупка по карте)"""
        driver = self.driver

        # === ШАГ 1: Ждём и нажимаем кнопку "Купить" ===
        buy_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
        driver.execute_script("arguments[0].click();", buy_button)

        # === ШАГ 2: Ждём формы "Оплата по карте" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
        )

        # === ШАГ 3: Заполняем поля с истекшим годом ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("10")                   # Месяц
        inputs[2].send_keys("24")                   # Год (истекший)
        inputs[3].send_keys("иван")                 # Владелец
        inputs[4].send_keys("999")                  # CVC

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления сообщения с текстом "Истёк срок действия карты" ===
        year_error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='input__sub' and text()='Истёк срок действия карты']"))
        )

        # Проверяем текст сообщения
        actual_text = year_error_element.text.strip()
        expected_text = "Истёк срок действия карты"
        self.assertEqual(actual_text, expected_text,
                         f"Ожидалось сообщение '{expected_text}', получено '{actual_text}'")


    def test_expired_year_credit(self):
        """Тест: истекший год (покупка в кредит)"""
        driver = self.driver

        # === ШАГ 1: Ждём и нажимаем кнопку "Купить в кредит" ===
        credit_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
        driver.execute_script("arguments[0].click();", credit_button)

        # === ШАГ 2: Ждём формы "Кредит по данным карты" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
        )

        # === ШАГ 3: Заполняем поля с истекшим годом ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("10")                   # Месяц
        inputs[2].send_keys("24")                   # Год (истекший)
        inputs[3].send_keys("иван")                 # Владелец
        inputs[4].send_keys("999")                  # CVC

        # === ШАГ 4: Нажимаем КНОПКУ "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления сообщения с текстом "Истёк срок действия карты" ===
        year_error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='input__sub' and text()='Истёк срок действия карты']"))
        )

        # Проверяем текст сообщения
        actual_text = year_error_element.text.strip()
        expected_text = "Истёк срок действия карты"
        self.assertEqual(actual_text, expected_text,
                         f"Ожидалось сообщение '{expected_text}', получено '{actual_text}'")

    def test_wrong_expiry_date_card(self):
        """
        ТЕСТ НА БАГ:
        При вводе месяца=11 и года=25 (валидная будущая дата)
        ОЖИДАЕТСЯ: отсутствие ошибки или ошибка "Истёк срок действия карты" под полем "Год"
        ФАКТИЧЕСКИ: появляется ошибка "Неверно указан срок действия карты" под полем "Месяц"
        ТЕСТ ДОЛЖЕН УПАСТЬ!
        """
        driver = self.driver

        # === ШАГ 1: Нажимаем кнопку "Купить" ===
        buy_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
        driver.execute_script("arguments[0].click();", buy_button)

        # === ШАГ 2: Ждём форму "Оплата по карте" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
        )

        # === ШАГ 3: Вводим данные с "валидной" датой 11/25 ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("11")  # Месяц
        inputs[2].send_keys("25")  # Год (2025 — будущее!)
        inputs[3].send_keys("иван")  # Владелец
        inputs[4].send_keys("999")  # CVC

        # === ШАГ 4: Нажимаем "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления ЛЮБОЙ ошибки ===
        error_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
        )

        # Проверяем, что есть хотя бы одна ошибка
        self.assertGreater(len(error_elements), 0,
                           "Не появилось ни одной ошибки. Ожидалась ошибка 'Истёк срок действия карты'")

        # Проверяем текст каждой ошибки
        for i, error in enumerate(error_elements):
            actual_text = error.text.strip()
            # Если найдена ошибка "Истёк срок действия карты" — это хорошо, но она должна быть под "Годом"
            if actual_text == "Истёк срок действия карты":
                # Проверим, что она под полем "Год" (индекс 2)
                if i == 2:
                    # Это корректное поведение — тест пройдет
                    return  # Выходим из теста, всё ок
                else:
                    # Ошибка "Истёк срок..." появилась не под "Годом" — это тоже баг
                    self.fail(
                        f"Ошибка 'Истёк срок действия карты' появилась под полем {i + 1}, а не под 'Годом'. Текст: '{actual_text}'")

        # Если мы дошли сюда — значит, ни одна ошибка не равна "Истёк срок действия карты"
        # Собираем все тексты ошибок для отчёта
        all_error_texts = [e.text.strip() for e in error_elements]
        self.fail(f"Ожидалась ошибка 'Истёк срок действия карты', но появилась другая: {all_error_texts}")

    def test_wrong_expiry_date_credit(self):
        """
        ТЕСТ НА БАГ (покупка в кредит):
        При вводе месяца=11 и года=25 (валидная будущая дата)
        ОЖИДАЕТСЯ: отсутствие ошибки или ошибка "Истёк срок действия карты" под полем "Год"
        ФАКТИЧЕСКИ: появляется ошибка "Неверно указан срок действия карты" под полем "Месяц"
        ТЕСТ ДОЛЖЕН УПАСТЬ!
        """
        driver = self.driver

        # === ШАГ 1: Нажимаем кнопку "Купить в кредит" ===
        credit_button = WebDriverWait(driver, 25).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
        driver.execute_script("arguments[0].click();", credit_button)

        # === ШАГ 2: Ждём форму "Кредит по данным карты" ===
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
        )

        # === ШАГ 3: Вводим данные с "валидной" датой 11/25 ===
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
        inputs[0].send_keys("4444 4444 4444 4442")  # Номер карты
        inputs[1].send_keys("11")  # Месяц
        inputs[2].send_keys("25")  # Год (2025 — будущее!)
        inputs[3].send_keys("иван")  # Владелец
        inputs[4].send_keys("999")  # CVC

        # === ШАГ 4: Нажимаем "Продолжить" ===
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
        )
        continue_button.click()

        # === ШАГ 5: Ждём появления ЛЮБОЙ ошибки ===
        error_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
        )

        # Проверяем, что есть хотя бы одна ошибка
        self.assertGreater(len(error_elements), 0,
                           "Не появилось ни одной ошибки. Ожидалась ошибка 'Истёк срок действия карты'")

        # Проверяем текст каждой ошибки
        for i, error in enumerate(error_elements):
            actual_text = error.text.strip()
            # Если найдена ошибка "Истёк срок действия карты" — это хорошо, но она должна быть под "Годом"
            if actual_text == "Истёк срок действия карты":
                # Проверим, что она под полем "Год" (индекс 2)
                if i == 2:
                    # Это корректное поведение — тест пройдет
                    return  # Выходим из теста, всё ок
                else:
                    # Ошибка "Истёк срок..." появилась не под "Годом" — это тоже баг
                    self.fail(
                        f"Ошибка 'Истёк срок действия карты' появилась под полем {i + 1}, а не под 'Годом'. Текст: '{actual_text}'")

        # Если мы дошли сюда — значит, ни одна ошибка не равна "Истёк срок действия карты"
        # Собираем все тексты ошибок для отчёта
        all_error_texts = [e.text.strip() for e in error_elements]
        self.fail(f"Ожидалась ошибка 'Истёк срок действия карты', но появилась другая: {all_error_texts}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()