import os
from .base_page import BasePage
from .hybrid_page import HybridPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, InvalidSessionIdException
import time
from urllib.parse import urlparse
from utils.excel_utils import append_to_excel_file, ensure_data_folder_exists, create_excel_file, EXCEL_FILE_PATH
from utils.num_of_tiles import get_number_of_tiles  # Import the utility function


class RefinePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Ensure the data folder and Excel file exist
        ensure_data_folder_exists()
        if not os.path.exists(EXCEL_FILE_PATH):
            create_excel_file()

    def check_property_tiles(self):
        """
        Checks the availability of all property tiles on the Refine page and logs the results.
        """
        try:
            print("Fetching the total number of property tiles...")
            time.sleep(5)  # Allow time for the page to stabilize
            
            # Fetch the total number of tiles using the utility function
            try:
                total_tiles = get_number_of_tiles(self.driver)
                print(f"Total property tiles found: {total_tiles}")
            except Exception as e:
                print(f"Error fetching property tile count: {str(e)}")
                total_tiles = 3  # Fallback to default
            
            num_checked = 0
            while num_checked < total_tiles:
                print(f"Waiting for property tiles to load... Checking tile {num_checked + 1} of {total_tiles}.")
                time.sleep(5)  # Allow tiles to load

                # Fetch all currently visible tiles
                property_tiles = self.wait_for_elements(
                    By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'title')]//a", timeout=60
                )

                # Iterate over visible tiles and test until total_tiles is reached
                for tile in property_tiles:
                    if num_checked >= total_tiles:
                        break  # Stop if we’ve already checked all tiles
                    
                    try:
                        href = tile.get_attribute("href")
                        title = tile.text
                        if not href or not title:
                            print("Invalid tile data; skipping...")
                            continue

                        print(f"Opening property: {title} ({href})")
                        time.sleep(5)  # Delay before opening the new tab
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])

                        print("Waiting for the Hybrid page to load...")
                        time.sleep(5)  # Delay to allow the Hybrid page to stabilize
                        self.wait_for_element(By.XPATH, "//div[@id='js-date-available'] | //div[@id='js-date-unavailable']", timeout=60)

                        hybrid_page = HybridPage(self.driver, source_page="refine")
                        availability = hybrid_page.check_property_availability()
                        availability_status = 'Available' if availability else 'Unavailable'
                        print(f"Property availability for {title}: {availability_status}")

                        # Log results in Excel
                        data = [
                            urlparse(href).netloc,  # Domain
                            href,  # URL
                            "Hybrid",  # Page
                            "Property available in date range",  # Test Case
                            availability,  # Passed
                            f"The property '{title}' is {availability_status} in the specified date range."  # Comments
                        ]

                        append_to_excel_file(data)

                        print("Closing property window and returning to Refine page...")
                        time.sleep(5)  # Delay for smooth transition back
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                        num_checked += 1
                    except NoSuchWindowException as e:
                        print(f"Window closed unexpectedly: {str(e)}")
                        if len(self.driver.window_handles) > 0:
                            self.driver.switch_to.window(self.driver.window_handles[0])
                    except Exception as e:
                        print(f"Error checking property tile: {str(e)}")
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])

            print("Finished checking all property tiles. Cleaning up...")
        except Exception as e:
            print(f"Error during property tile check: {str(e)}")
        finally:
            self.cleanup_and_quit()

    def wait_for_elements(self, by, value, timeout=60):
        """
        Waits for the presence and visibility of multiple elements on the page.

        Args:
            by (selenium.webdriver.common.by.By): The type of locator (e.g., By.XPATH).
            value (str): The locator value (e.g., the XPath string).
            timeout (int): The timeout in seconds to wait for the elements.

        Returns:
            list: A list of located WebElements.

        Raises:
            Exception: If the elements cannot be located within the timeout period.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((by, value))
            )
            return elements
        except Exception as e:
            print(f"Error waiting for elements: {str(e)}")
            raise

    def cleanup_and_quit(self):
        """
        Cleans up by closing all browser windows and quitting the WebDriver session.
        """
        try:
            print("Closing all browser windows...")
            while len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()
            print("All browser windows closed.")
        except InvalidSessionIdException as e:
            print(f"Invalid session id: {str(e)}")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        finally:
            print("Ending the WebDriver session...")
            try:
                self.driver.quit()
            except InvalidSessionIdException as e:
                print(f"Invalid session id: {str(e)}")
            except Exception as e:
                print(f"Error quitting WebDriver: {str(e)}")
            print("WebDriver session ended.")
