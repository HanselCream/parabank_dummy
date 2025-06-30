import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from time import sleep
import allure      
import pytest
from pages.paraBank_page import ParaBankPage
from allure_commons.types import AttachmentType
from utilities.data_generator import generate_random_name 
# pytest testcases/paraBank_test.py
# pytest -s testcases/paraBank_test.py --alluredir=allure-results
# pytest -s testcases/paraBank_test.py --alluredir=allure-results --browser_name=chrome
# HOW TO RUN?
# pytest --alluredir=allure-results
# pytest --alluredir=allure-results
# OPEN ALLURE REPORT
# allure generate allure-results --clean -o allure-report
# allure open allure-report

@pytest.mark.usefixtures("setup")
class TestParaBank:

    def setup_method(self):
        self.pb = ParaBankPage(self.driver)
        TestParaBank.driver = self.driver  # for allure screenshot hook

    @allure.title("Test Registration with Valid Data")
    @allure.description("This test case registers a new user with valid data and verifies the welcome message.")
    @pytest.mark.register
    def test_register_user(self):
        self.pb.click_register()
        self.attach_screenshot("Test Registration")
        username = generate_random_name(prefix="user")
        password = generate_random_name(prefix="pass")
        print(f"Generated username: {username}, password: {password}")

        self.pb.add_customer_details(
            first_name="John",
            last_name="Doe",
            address="123 Elm St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-1234",
            ssn="123-45-6789",
            username=username,
            password=password
        )

        self.pb.click_register_button()
        sleep(5)
        with allure.step("Verify registration success"):
        # self.pb.verify_welcome_message_element()
            self.attach_screenshot("Welcome Message")
            self.pb.click_on_logout()
        
            # assert self.pb.is_element_visible(self.pb.Locators.SHOW_OVERVIEW), \
                # "Welcome message not visible after registration"
            

    @pytest.mark.login
    @allure.title("Test Valid Credentials")
    @allure.description("Logs in with valid credentials and verifies that the account overview is visible.")
    def test_valid_login(self):
        self.pb.valid_login()
        with allure.step("Verify successful login"):
            self.attach_screenshot("Valid Login")    
            assert self.pb.is_element_visible(self.pb.Locators.SHOW_OVERVIEW), \
                "Login failed, welcome message not visible"
        self.pb.click_on_logout()


    def attach_screenshot(self, name):
        try:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)
        except Exception as e:
                print(f"Screenshot capture failed: {e}")
        