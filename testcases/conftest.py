import os
import time
import pytest
import allure
import requests
from selenium import webdriver
from allure_commons.types import AttachmentType

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# ✅ Adds CLI option: --browser_name
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")


# ✅ Optional: Stop all tests if the site is down
@pytest.fixture(scope="session", autouse=True)
def check_app_up():
    try:
        r = requests.get("https://parabank.parasoft.com/")
        if r.status_code != 200:
            pytest.exit("❌ Parabank site is not reachable. Aborting test run.")
    except Exception as e:
        pytest.exit(f"❌ Failed to connect to Parabank: {e}")


# ✅ Setup fixture for class-scoped Selenium driver
@pytest.fixture(scope="class")
def setup(request):
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_name == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.get("https://parabank.parasoft.com/")
    driver.implicitly_wait(10)
    driver.maximize_window()

    request.cls.driver = driver
    yield
    driver.quit()


# ✅ Allure: attach screenshot after each test
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        driver = getattr(item.cls, "driver", None)
        if driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=AttachmentType.PNG)
