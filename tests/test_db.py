import pytest
import allure
import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_chrome_options():
    """Настройка ChromeOptions для работы в CI"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")           # Обязательно для CI
    options.add_argument("--disable-dev-shm-usage") # Обязательно для CI
    options.add_argument("--headless=new")         # Безголовый режим
    options.add_argument("--disable-gpu")          # Для стабильности
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-background-timer-throttling")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='app',
            user='app',
            password='pass'
        )
        return connection
    except Error as e:
        pytest.fail(f"Не удалось подключиться к БД: {e}")


def clear_db_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payment_entity")
    cursor.execute("DELETE FROM credit_request_entity")
    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080")
    yield driver
    driver.quit()


# ─────────────── ТЕСТЫ ───────────────

@allure.feature("Проверка данных в БД")
@allure.story("Оплата по карте")
@allure.title("После успешной оплаты создаётся запись в payment_entity со статусом APPROVED")
def test_payment_db_success_record(driver):
    clear_db_tables()

    buy_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
    )
    driver.execute_script("arguments[0].click();", buy_button)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']")))

    inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
    inputs[0].send_keys("4444 4444 4444 4441")
    inputs[1].send_keys("08")
    inputs[2].send_keys("26")
    inputs[3].send_keys("иван")
    inputs[4].send_keys("999")

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Продолжить')]"))
    )
    continue_button.click()

    WebDriverWait(driver, 25).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
    )

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, status, transaction_id
        FROM payment_entity
        ORDER BY created DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    assert row is not None
    amount, status, transaction_id = row
    assert amount == 4500000
    assert status == "APPROVED"
    assert transaction_id is not None


# Для DECLINED в оплате — уведомление ОБЯЗАТЕЛЬНО появляется!
@allure.feature("Проверка данных в БД")
@allure.story("Оплата по карте")
@allure.title("После неуспешной оплаты создаётся запись в payment_entity со статусом DECLINED")
def test_payment_db_decline_record(driver):
    clear_db_tables()

    buy_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button_size_m.button_theme_alfa-on-white"))
    )
    driver.execute_script("arguments[0].click();", buy_button)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Оплата по карте']")))

    inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
    inputs[0].send_keys("4444 4444 4444 4442")  # DECLINED
    inputs[1].send_keys("08")
    inputs[2].send_keys("26")
    inputs[3].send_keys("иван")
    inputs[4].send_keys("999")

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Продолжить')]"))
    )
    continue_button.click()

    # ❌ Уведомления об ошибке НЕТ — ждём завершения операции
    WebDriverWait(driver, 25).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.button_disabled"))
    )

    # Проверка БД
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT amount, status, transaction_id
        FROM payment_entity
        ORDER BY created DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    assert row is not None, "Запись в payment_entity не создана"
    amount, status, transaction_id = row
    assert amount == 4500000
    assert status == "DECLINED"
    assert transaction_id is not None

# Для кредита — НЕТ уведомления при DECLINED!
@allure.feature("Проверка данных в БД")
@allure.story("Покупка в кредит")
@allure.title("После успешной покупки в кредит создаётся запись в credit_request_entity со статусом APPROVED")
def test_credit_db_success_record(driver):
    clear_db_tables()

    credit_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Купить в кредит')]"))
    )
    driver.execute_script("arguments[0].click();", credit_button)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']")))

    inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
    inputs[0].send_keys("4444 4444 4444 4441")
    inputs[1].send_keys("08")
    inputs[2].send_keys("26")
    inputs[3].send_keys("иван")
    inputs[4].send_keys("999")

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Продолжить')]"))
    )
    continue_button.click()

    # ✅ Успешный кредит — уведомление есть
    WebDriverWait(driver, 25).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.notification.notification_status_ok .notification__title"))
    )

    conn = get_db_connection()
    cursor = conn.cursor()
    # 🔥 ЗАПРАШИВАЕМ `status`, а не `bank_id`!
    cursor.execute("""
        SELECT status, bank_id
        FROM credit_request_entity
        ORDER BY created DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    assert row is not None
    status, bank_id = row
    assert status == "APPROVED"
    assert bank_id is not None


@allure.feature("Проверка данных в БД")
@allure.story("Покупка в кредит")
@allure.title("После неуспешной покупки в кредит создаётся запись в credit_request_entity со статусом DECLINED")
def test_credit_db_decline_record(driver):
    clear_db_tables()

    credit_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Купить в кредит')]"))
    )
    driver.execute_script("arguments[0].click();", credit_button)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Кредит по данным карты']")))

    inputs = driver.find_elements(By.CSS_SELECTOR, "input.input__control")
    inputs[0].send_keys("4444 4444 4444 4442")
    inputs[1].send_keys("08")
    inputs[2].send_keys("26")
    inputs[3].send_keys("иван")
    inputs[4].send_keys("999")

    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Продолжить')]"))
    )
    continue_button.click()

    # ❌ Для кредита DECLINED — НЕТ уведомления!
    # Вместо этого ждём, что кнопка перестала быть disabled
    WebDriverWait(driver, 25).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.button_disabled"))
    )

    conn = get_db_connection()
    cursor = conn.cursor()
    # 🔥 ЗАПРАШИВАЕМ `status`, а не `bank_id`!
    cursor.execute("""
        SELECT status, bank_id
        FROM credit_request_entity
        ORDER BY created DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    assert row is not None
    status, bank_id = row
    assert status == "DECLINED"
    assert bank_id is not None