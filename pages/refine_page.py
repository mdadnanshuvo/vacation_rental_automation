# pages/search_results_page.py

from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class RefinePage(BasePage):
    def validate_properties(self, properties_checked, max_properties_to_check):
        visited_properties = set()
        properties_validated = 0

        while properties_checked + properties_validated < max_properties_to_check:
            tiles = self.driver.find_elements(By.XPATH, "//div[@class='title']/a[contains(@class, 'font-bold')]")

            if not tiles:
                self._scroll_to_load_more()
                continue

            for tile in tiles:
                prop_id = tile.get_attribute("data-id")
                if prop_id in visited_properties:
                    continue

                visited_properties.add(prop_id)
                self._validate_property_tile(tile)

                properties_validated += 1
                if properties_checked + properties_validated >= max_properties_to_check:
                    break

            self._scroll_to_load_more()

        return properties_validated

    def _scroll_to_load_more(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def _validate_property_tile(self, tile):
        tile.click()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        from .check_availability import PropertyPage
        PropertyPage(self.driver).validate_property_availability()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])