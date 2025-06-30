import inspect 
from time import sleep
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger, DEBUG
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException

class BaseDriver:
    def __init__(self, driver):
        self.driver = driver
        
# scroll to element
    def page_scroll_to_element(self, elements):
        for element in elements:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            sleep(1)

# get Elements
    def get_element(self, locator):
        try:
            element = self.driver.find_element(*locator)
            return element
        except Exception as e:
            print(f"Error finding element {locator}: {e}")
            return None

# scroll and highlight element      
    def scroll_highlight_element(self, element):
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.execute_script("arguments[0].style.border='3px solid red';", element)
            sleep(1)
            self.driver.execute_script("arguments[0].style.border=''", element)
        else:
            print("Element not found to highlight.")    

# click on element
    def click_on_element(self, locator):
        element = self.get_element(locator)
        if element:
            self.scroll_highlight_element(element)
            element.click()
        else:
            print(f"Element {locator} not found for clicking.")  

    def is_element_visible(self, locator):
        try:
            return self.driver.find_element(*locator).is_displayed()
        except:
            return False
        
    def is_element_present_wait(self, locator, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False    

    def wait_for_visible_element(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
        
    def wait_for_element(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Wait Element Timeout", attachment_type=AttachmentType.PNG)
            raise Exception(f"Timeout waiting for element: {locator}") from e
        
 