import logging
from time import sleep
import allure
from base.BaseDriver import BaseDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType
from utilities.utils import custom_logger


class ParaBankPage(BaseDriver):
    log = custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    # Strings
    userName = "qwe"
    password = "qwe"

    # Locators
    class Locators:
        REGISTER = (By.XPATH, "//a[text()='Register']")
        REGISTER_BUTTON = (By.XPATH, "//input[@value='Register']")
        FIRST_NAME = (By.ID, "customer.firstName")
        LAST_NAME = (By.ID, "customer.lastName")
        ADDRESS = (By.ID, "customer.address.street")
        CITY = (By.ID, "customer.address.city")
        STATE = (By.ID, "customer.address.state")
        ZIP_CODE = (By.ID, "customer.address.zipCode")
        PHONE = (By.ID, "customer.phoneNumber")
        SSN = (By.ID, "customer.ssn")
        USERNAME = (By.ID, "customer.username")
        PASSWORD = (By.ID, "customer.password")
        CONFIRM_PASSWORD = (By.ID, "repeatedPassword")
        SIGNING_UP_TITLE = (By.CLASS_NAME, "title") # REGISTER BUTTON BEFORE
        WELCOME_MESSAGE = (By.XPATH, "//h1[contains(text(),'Welcome')]")
        WELCOME_MESSAGE_ELEMENT = (By.XPATH, "//p[contains(text(),'Your account was created successfully. You are now logged in.')]")

        # LOGIN
        VALID_USERNAME = (By.NAME, "username")
        VALID_PASSWORD = (By.NAME, "password")
        LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
        SHOW_OVERVIEW = (By.XPATH, "//h1[normalize-space()='Accounts Overview']")

        # Error message elements
        ERROR_FIRSTNAME = (By.ID, "customer.firstName.errors")
        ERROR_LASTNAME = (By.ID, "customer.lastName.errors")
        ERROR_ADDRESS = (By.ID, "customer.address.street.errors")
        ERROR_CITY = (By.ID, "customer.address.city.errors")
        ERROR_STATE = (By.ID, "customer.address.state.errors")
        ERROR_ZIP_CODE = (By.ID, "customer.address.zipCode.errors")
        ERROR_SSN = (By.ID, "customer.ssn.errors")
        ERROR_USERNAME = (By.ID, "customer.username.errors")
        ERROR_PASSWORD = (By.ID, "customer.password.errors")
        ERROR_CONFIRM_PASSWORD = (By.ID, "repeatedPassword.errors")

    # -------- Test Case 1: Valid registration --------
    @allure.step("Clicking on Register link")
    def click_register(self):
        self.click_on_element(self.Locators.REGISTER)
        try:
            self.wait_for_element(self.Locators.REGISTER_BUTTON, timeout=15)
            assert self.is_element_visible(self.Locators.REGISTER_BUTTON), "Register form not visible"
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Register Page Load Failure", attachment_type=AttachmentType.PNG)
            allure.attach(str(e), name="Timeout Exception", attachment_type=AttachmentType.TEXT)
            assert False, f"Register page did not load: {e}"

        

    @allure.step("Adding customer details: {first_name} {last_name}")
    def add_customer_details(self, first_name, last_name, address, city, state, zip_code, phone, ssn, username, password):
        self.get_element(self.Locators.FIRST_NAME).send_keys(first_name)
        self.get_element(self.Locators.LAST_NAME).send_keys(last_name)
        self.get_element(self.Locators.ADDRESS).send_keys(address)
        self.get_element(self.Locators.CITY).send_keys(city)
        self.get_element(self.Locators.STATE).send_keys(state)
        self.get_element(self.Locators.ZIP_CODE).send_keys(zip_code)
        self.get_element(self.Locators.PHONE).send_keys(phone)
        self.get_element(self.Locators.SSN).send_keys(ssn)
        self.get_element(self.Locators.USERNAME).send_keys(username)
        self.get_element(self.Locators.PASSWORD).send_keys(password)
        self.get_element(self.Locators.CONFIRM_PASSWORD).send_keys(password)
        # self.get_element(self.Locators.REGISTER_BUTTON).click()

    @allure.step("Clicking on Register button and verifying welcome message")
    def click_register_button(self):
    
        self.wait_for_element(self.Locators.REGISTER_BUTTON)
        assert self.is_element_visible(self.Locators.REGISTER_BUTTON), "Register button not visible"
        self.scroll_highlight_element(self.get_element(self.Locators.REGISTER_BUTTON))
        self.click_on_element(self.Locators.REGISTER_BUTTON)
        sleep(2) 

    @allure.step("Verifying welcome message")
    def verify_welcome_message_element(self):
        try:
            self.wait_for_element(self.Locators.WELCOME_MESSAGE_ELEMENT, timeout=15)
            element = self.get_element(self.Locators.WELCOME_MESSAGE_ELEMENT)
            self.wait.until(EC.visibility_of(element))
            self.scroll_highlight_element(element)
            allure.attach(self.driver.get_screenshot_as_png(), name="Welcome Message", attachment_type=AttachmentType.PNG)
            assert element.is_displayed(), "Welcome message element not visible"
            assert element.text.strip() != "", "Welcome message is empty"
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Welcome Message Failure", attachment_type=AttachmentType.PNG)
            allure.attach(str(e), name="Exception", attachment_type=AttachmentType.TEXT)
            assert False, f"Failed to verify welcome message: {e}"


# -------- Test Case 2: Valid login --------
    error_invalid_credentials = (By.XPATH,"//p[@class='error']")

    @allure.step("Validating login with valid credentials")
    def valid_login(self):
        self.get_element(self.Locators.VALID_USERNAME).send_keys(self.userName)
        self.get_element(self.Locators.VALID_PASSWORD).send_keys(self.password)
        self.click_on_element(self.Locators.LOGIN_BUTTON)
        landing_page= self.get_element((By.NAME, "showOverview"))
        sleep(2)
        if self.is_element_visible(self.Locators.error_invalid_credentials):
                error_text = self.get_element(self.Locators.error_invalid_credentials).text
                allure.attach(error_text, name="Login Error", attachment_type=AttachmentType.TEXT)
                assert False, f"Login failed: {error_text}"

        assert self.is_element_visible(self.Locators.SHOW_OVERVIEW), "Login failed, welcome message not visible"
            
    # -------- Test Case 3: Invalid registration --------
    @allure.step("Verifying error messages for required fields")
    def verify_error_if_else(self):
        error_fields = {
            "First Name": self.Locators.ERROR_FIRSTNAME,
            "Last Name": self.Locators.ERROR_LASTNAME,
            "Address": self.Locators.ERROR_ADDRESS,
            "City": self.Locators.ERROR_CITY,
            "State": self.Locators.ERROR_STATE,
            "Zip Code": self.Locators.ERROR_ZIP_CODE,
            "SSN": self.Locators.ERROR_SSN,
            "Username": self.Locators.ERROR_USERNAME,
            "Password": self.Locators.ERROR_PASSWORD,
            "Confirm Password": self.Locators.ERROR_CONFIRM_PASSWORD
        }
        for field, locator in error_fields.items():
            element = self.get_element(locator)
            if element and element.is_displayed():
                self.scroll_highlight_element(element)
                error_text = element.text.strip()
                print(f"{field} error text: '{error_text}'")
                allure.attach(self.driver.get_screenshot_as_png(), name=f"{field} Error Screenshot",
                            attachment_type=AttachmentType.PNG)
                allure.attach(error_text, name=f"{field} Error", attachment_type=AttachmentType.TEXT)
                assert error_text, f"{field} error message is empty"
            else:
                print(f"{field} error NOT displayed")
                allure.attach(f"No error found", name=f"{field} Error", attachment_type=AttachmentType.TEXT)
                assert False, f"{field} error not displayed as expected"



