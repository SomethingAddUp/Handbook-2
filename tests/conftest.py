from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from POM.ecommerce import SwagLabs

@pytest.fixture
def driver(request):
    service = Service(ChromeDriverManager().install())

    chrome_options = Options()
    prefs = { "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.saucedemo.com/")
    if request.node.get_closest_marker('login'):
        SwagLabs(driver).login("standard_user", "secret_sauce")

    yield driver
    driver.quit()
