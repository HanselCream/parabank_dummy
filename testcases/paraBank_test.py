import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from time import sleep
import allure
import pytest
from pages.paraBank_page import ParaBankPage
from allure_commons.types import AttachmentType
from utilities.data_generator import generate_random_name 

#  pytest --alluredir=allure-results
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
        self.pb.attach_screenshot("Test Registration")
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
        self.pb.verify_welcome_message_element()
        self.attach_screenshot("Welcome Message")
        sleep(2)
        with allure.step("Verify welcome message after registration"):
            assert self.pb.is_element_visible(self.pb.Locators.SHOW_OVERVIEW), "Welcome message not visible after registration"
            self.pb.click_on_logout()

    @pytest.mark.register
    @allure.title("Test Registration with Invalid Data")
    def test_register_user_with_invalid_data(self):
        self.pb.click_register()
        self.pb.add_customer_details(
            first_name="Jane", 
            last_name="Doe",
            address="456 Oak St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-5678",
            ssn="",
            username="",
            password=""
        )
        self.attach_screenshot("After Register")
        self.pb.click_register_button()
        with allure.step("Verify error message for invalid registration"):
            sleep(5)
            assert self.pb.get_element(self.pb.Locators.ERROR_USERNAME).is_displayed(), "Error message not found"

    @pytest.mark.login
    @allure.title("Test Valid Credentials")
    @allure.description("Logs in with valid credentials and verifies that the account overview is visible.")
    def test_valid_login(self):
        self.pb.valid_login()
        with allure.step("Verify successful login"):
            self.attach_screenshot("Valid Login")    
            assert self.pb.is_element_visible(self.pb.Locators.SHOW_OVERVIEW), "Login failed, welcome message not visible"
