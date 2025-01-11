import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_number_of_tiles(driver):
    """
    Retrieves the number of property tiles available on the Refine page.

    Args:
        driver (selenium.webdriver): The WebDriver instance controlling the browser.

    Returns:
        int: The number of property tiles on the page.

    Raises:
        Exception: If the script fails to retrieve the number of tiles.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Wait for the ScriptData object to load fully
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return typeof ScriptData !== 'undefined' && ScriptData.pageData && ScriptData.pageData.Items")
            )
            num_tiles = driver.execute_script("return ScriptData.pageData.Items.length;")
            if isinstance(num_tiles, int) and num_tiles > 0:
                return num_tiles
            else:
                raise ValueError(f"Invalid number of tiles retrieved: {num_tiles}")
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} - Error fetching number of tiles: {str(e)}")
            time.sleep(5)  # Wait before retrying
    raise Exception("Failed to retrieve the number of tiles after retries.")