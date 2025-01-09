from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present in the DOM."""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def wait_for_element_visible(self, by, value, timeout=10):
        """Wait for an element to be visible."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))

    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable."""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))

    def wait_for_elements(self, by, value, timeout=10):
        """Wait for multiple elements to be present in the DOM."""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, value)))

    def wait_for_elements_visible(self, by, value, timeout=10):
        """Wait for multiple elements to be visible."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located((by, value)))

    def click_element(self, by, value, timeout=10):
        """Wait for an element to be clickable and then click it."""
        element = self.wait_for_element_clickable(by, value, timeout)
        element.click()

    def enter_text(self, by, value, text, timeout=10):
        """Wait for an element to be visible and enter text."""
        element = self.wait_for_element_visible(by, value, timeout)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, by, value, timeout=10):
        """Wait for an element to be visible and get its text."""
        element = self.wait_for_element_visible(by, value, timeout)
        return element.text

    def get_element_attribute(self, by, value, attribute, timeout=10):
        """Wait for an element to be visible and get an attribute value."""
        element = self.wait_for_element_visible(by, value, timeout)
        return element.get_attribute(attribute)
