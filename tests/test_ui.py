
import unittest
import allure
from allure_commons.types import AttachmentType
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

    def tearDown(self):
        # Делаем скриншот только если тест упал
        if hasattr(self, '_outcome') and self._outcome.errors:
            try:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=AttachmentType.PNG
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")
        self.driver.quit()

    # ───────────────────────────────────────
    # ✅ УСПЕШНЫЕ ПОКУПКИ
    # ───────────────────────────────────────

    @allure.feature("Оплата по карте")
    @allure.story("Успешная оплата")
    @allure.title("Успешная покупка по карте с корректными данными")
    def test_successful_card_purchase(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить'"):
            buy_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            driver.execute_script("arguments[0].click();", buy_button)

        with allure.step("Дождаться формы 'Оплата по карте'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
            )

        with allure.step("Заполнить форму корректными данными"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("08")
            inputs[2].send_keys("26")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Дождаться состояния 'Отправляем запрос в Банк...'"):
            WebDriverWait(driver, 15).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "button.button_view_extra.button_size_m.button_theme_alfa-on-white.button_disabled .button__text"),
                    "Отправляем запрос в Банк..."
                )
            )

        with allure.step("Проверить успешное уведомление"):
            title_element = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
            )
            assert title_element.text.strip() == "Успешно"
            content_element = driver.find_element(By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__content")
            assert "Операция одобрена Банком." in content_element.text.strip()

    @allure.feature("Покупка в кредит")
    @allure.story("Успешная оплата")
    @allure.title("Успешная покупка в кредит с корректными данными")
    def test_successful_credit_purchase(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить в кредит'"):
            credit_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
            driver.execute_script("arguments[0].click();", credit_button)

        with allure.step("Дождаться формы 'Кредит по данным карты'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
            )

        with allure.step("Заполнить форму корректными данными"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("08")
            inputs[2].send_keys("26")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Дождаться состояния 'Отправляем запрос в Банк...'"):
            WebDriverWait(driver, 15).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "button.button_view_extra.button_size_m.button_theme_alfa-on-white.button_disabled .button__text"),
                    "Отправляем запрос в Банк..."
                )
            )

        with allure.step("Проверить успешное уведомление"):
            title_element = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
            )
            assert title_element.text.strip() == "Успешно"
            content_element = driver.find_element(By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__content")
            assert "Операция одобрена Банком." in content_element.text.strip()

    # ───────────────────────────────────────
    # ❌ ВАЛИДАЦИЯ ПУСТЫХ ПОЛЕЙ
    # ───────────────────────────────────────

    @allure.feature("Оплата по карте")
    @allure.story("Валидация формы")
    @allure.title("Ошибка при отправке формы с пустыми полями (покупка по карте)")
    def test_invalid_card_fields(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить'"):
            buy_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            driver.execute_script("arguments[0].click();", buy_button)

        with allure.step("Дождаться формы 'Оплата по карте'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
            )

        with allure.step("Оставить все поля пустыми и нажать 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить сообщения об ошибках под каждым полем"):
            error_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
            )
            self.assertEqual(len(error_elements), 5)

            expected_errors = [
                "Неверный формат",
                "Неверный формат",
                "Неверный формат",
                "Поле обязательно для заполнения",
                "Неверный формат"
            ]
            for i, err in enumerate(error_elements):
                self.assertEqual(err.text.strip(), expected_errors[i])

    @allure.feature("Покупка в кредит")
    @allure.story("Валидация формы")
    @allure.title("Ошибка при отправке формы с пустыми полями (покупка в кредит)")
    def test_invalid_credit_fields(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить в кредит'"):
            credit_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
            driver.execute_script("arguments[0].click();", credit_button)

        with allure.step("Дождаться формы 'Кредит по данным карты'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
            )

        with allure.step("Оставить все поля пустыми и нажать 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить сообщения об ошибках под каждым полем"):
            error_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
            )
            self.assertEqual(len(error_elements), 5)

            expected_errors = [
                "Неверный формат",
                "Неверный формат",
                "Неверный формат",
                "Поле обязательно для заполнения",
                "Неверный формат"
            ]
            for i, err in enumerate(error_elements):
                self.assertEqual(err.text.strip(), expected_errors[i])

    # ───────────────────────────────────────
    # ⏳ ВАЛИДАЦИЯ ИСТЕКШЕГО СРОКА
    # ───────────────────────────────────────

    @allure.feature("Оплата по карте")
    @allure.story("Валидация срока действия")
    @allure.title("Ошибка 'Истёк срок действия карты' при вводе года 24 (покупка по карте)")
    def test_expired_year_card(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить'"):
            buy_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            driver.execute_script("arguments[0].click();", buy_button)

        with allure.step("Дождаться формы 'Оплата по карте'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
            )

        with allure.step("Заполнить форму с истекшим годом (24)"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("10")
            inputs[2].send_keys("24")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить ошибку под полем 'Год'"):
            error_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@class='input__sub' and text()='Истёк срок действия карты']"))
            )
            self.assertEqual(error_element.text.strip(), "Истёк срок действия карты")

    @allure.feature("Покупка в кредит")
    @allure.story("Валидация срока действия")
    @allure.title("Ошибка 'Истёк срок действия карты' при вводе года 24 (покупка в кредит)")
    def test_expired_year_credit(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить в кредит'"):
            credit_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
            driver.execute_script("arguments[0].click();", credit_button)

        with allure.step("Дождаться формы 'Кредит по данным карты'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
            )

        with allure.step("Заполнить форму с истекшим годом (24)"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("10")
            inputs[2].send_keys("24")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить ошибку под полем 'Год'"):
            error_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@class='input__sub' and text()='Истёк срок действия карты']"))
            )
            self.assertEqual(error_element.text.strip(), "Истёк срок действия карты")

    # ───────────────────────────────────────
    # 🐞 ТЕСТЫ-БАГИ (ожидают ошибку, но падают при некорректной)
    # ───────────────────────────────────────

    @allure.feature("Оплата по карте")
    @allure.story("Баг: Некорректная ошибка при будущей дате")
    @allure.title("Ожидается 'Истёк срок...', но получаем 'Неверно указан срок...' (11/25, покупка по карте)")
    def test_wrong_expiry_date_card(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить'"):
            buy_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            driver.execute_script("arguments[0].click();", buy_button)

        with allure.step("Дождаться формы 'Оплата по карте'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
            )

        with allure.step("Ввести будущую дату: месяц=11, год=25"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("11")
            inputs[2].send_keys("25")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить, что появилась ОЖИДАЕМАЯ ошибка 'Истёк срок...' под 'Годом'"):
            error_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
            )
            self.assertGreater(len(error_elements), 0, "Ошибки не появилось")

            for i, err in enumerate(error_elements):
                if err.text.strip() == "Истёк срок действия карты":
                    if i == 2:  # ошибка под "Годом"
                        return  # всё хорошо
                    else:
                        self.fail(f"Ошибка 'Истёк срок...' под полем {i+1}, а не под 'Годом'")
            all_texts = [e.text.strip() for e in error_elements]
            self.fail(f"Ожидалась 'Истёк срок...', но получено: {all_texts}")

    @allure.feature("Покупка в кредит")
    @allure.story("Баг: Некорректная ошибка при будущей дате")
    @allure.title("Ожидается 'Истёк срок...', но получаем 'Неверно указан срок...' (11/25, покупка в кредит)")
    def test_wrong_expiry_date_credit(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить в кредит'"):
            credit_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
            driver.execute_script("arguments[0].click();", credit_button)

        with allure.step("Дождаться формы 'Кредит по данным карты'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
            )

        with allure.step("Ввести будущую дату: месяц=11, год=25"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4441")
            inputs[1].send_keys("11")
            inputs[2].send_keys("25")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Проверить, что появилась ОЖИДАЕМАЯ ошибка 'Истёк срок...' под 'Годом'"):
            error_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.input__sub"))
            )
            self.assertGreater(len(error_elements), 0, "Ошибки не появилось")

            for i, err in enumerate(error_elements):
                if err.text.strip() == "Истёк срок действия карты":
                    if i == 2:  # ошибка под "Годом"
                        return  # всё хорошо
                    else:
                        self.fail(f"Ошибка 'Истёк срок...' под полем {i+1}, а не под 'Годом'")
            all_texts = [e.text.strip() for e in error_elements]
            self.fail(f"Ожидалась 'Истёк срок...', но получено: {all_texts}")

    # ───────────────────────────────────────
    #  БАГ: НЕКОРРЕКТНАЯ ОБРАБОТКА КАРТЫ 4444 4444 4444 4442
    # ───────────────────────────────────────

    @allure.feature("Оплата по карте")
    @allure.story("Баг: Некорректная обработка отказа банка")
    @allure.title("Карта 4444 4444 4444 4442 должна вызывать ошибку, но вызывает успех (покупка по карте)")
    def test_card_4442_should_reject_but_approves(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить'"):
            buy_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)
            driver.execute_script("arguments[0].click();", buy_button)

        with allure.step("Дождаться формы 'Оплата по карте'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']"))
            )

        with allure.step("Заполнить форму данными карты 4444 4444 4444 4442"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4442")
            inputs[1].send_keys("08")
            inputs[2].send_keys("26")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Дождаться появления ЛЮБОГО уведомления"):
            notification = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification"))
            )

        with allure.step("Проверить, что уведомление — НЕ об успехе, а об ошибке"):
            notification_class = notification.get_attribute("class")

            if "notification_status_ok" in notification_class:
                title = notification.find_element(By.CSS_SELECTOR, ".notification__title").text.strip()
                content = notification.find_element(By.CSS_SELECTOR, ".notification__content").text.strip()
                self.fail(
                    f"Ожидалось уведомление об ОШИБКЕ, но получено об УСПЕХЕ!\n"
                    f"Заголовок: '{title}'\n"
                    f"Содержимое: '{content}'"
                )

            # Если дошли сюда — уведомление не 'ok', проверим, что оно 'error'
            assert "notification_status_error" in notification_class, \
                f"Уведомление не является ни 'ok', ни 'error'. Классы: {notification_class}"

            title = notification.find_element(By.CSS_SELECTOR, ".notification__title").text.strip()
            content = notification.find_element(By.CSS_SELECTOR, ".notification__content").text.strip()

            assert title == "Ошибка", f"Неверный заголовок ошибки: '{title}'"
            assert "Ошибка! Банк отказал в проведении операции." in content, \
                f"Неверное содержимое ошибки: '{content}'"

    @allure.feature("Покупка в кредит")
    @allure.story("Баг: Некорректная обработка отказа банка")
    @allure.title("Карта 4444 4444 4444 4442 должна вызывать ошибку, но вызывает успех (покупка в кредит)")
    def test_credit_4442_should_reject_but_approves(self):
        driver = self.driver

        with allure.step("Нажать кнопку 'Купить в кредит'"):
            credit_button = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and contains(., 'Купить в кредит')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", credit_button)
            driver.execute_script("arguments[0].click();", credit_button)

        with allure.step("Дождаться формы 'Кредит по данным карты'"):
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']"))
            )

        with allure.step("Заполнить форму данными карты 4444 4444 4444 4442"):
            inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
            inputs[0].send_keys("4444 4444 4444 4442")
            inputs[1].send_keys("08")
            inputs[2].send_keys("26")
            inputs[3].send_keys("иван")
            inputs[4].send_keys("999")

        with allure.step("Нажать кнопку 'Продолжить'"):
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//button[contains(@class, 'button_view_extra') and contains(@class, 'button_size_m') and contains(@class, 'button_theme_alfa-on-white') and not(contains(@class, 'button_disabled')) and contains(., 'Продолжить')]"))
            )
            continue_button.click()

        with allure.step("Дождаться появления ЛЮБОГО уведомления"):
            notification = WebDriverWait(driver, 25).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification"))
            )

        with allure.step("Проверить, что уведомление — НЕ об успехе, а об ошибке"):
            notification_class = notification.get_attribute("class")

            if "notification_status_ok" in notification_class:
                title = notification.find_element(By.CSS_SELECTOR, ".notification__title").text.strip()
                content = notification.find_element(By.CSS_SELECTOR, ".notification__content").text.strip()
                self.fail(
                    f"Ожидалось уведомление об ОШИБКЕ, но получено об УСПЕХЕ!\n"
                    f"Заголовок: '{title}'\n"
                    f"Содержимое: '{content}'"
                )

            assert "notification_status_error" in notification_class, \
                f"Уведомление не является ни 'ok', ни 'error'. Классы: {notification_class}"

            title = notification.find_element(By.CSS_SELECTOR, ".notification__title").text.strip()
            content = notification.find_element(By.CSS_SELECTOR, ".notification__content").text.strip()

            assert title == "Ошибка", f"Неверный заголовок ошибки: '{title}'"
            assert "Ошибка! Банк отказал в проведении операции." in content, \
                f"Неверное содержимое ошибки: '{content}'"
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()