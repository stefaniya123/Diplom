import pytest
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

@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()