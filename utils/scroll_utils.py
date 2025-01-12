import time


def scroll_to_load_all_tiles(driver, delay=2):
    """
    Scroll down the page until all property tiles are loaded.

    Args:
        driver: The WebDriver instance controlling the browser.
        delay: Time in seconds to wait after each scroll to allow content to load.

    Returns:
        None
    """
    previous_height = 0
    while True:
        # Scroll to the bottom of the page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)  # Wait for new content to load

        # Get the current page height after scrolling
        current_height = driver.execute_script(
            "return document.body.scrollHeight;")

        if current_height == previous_height:
            # Stop scrolling if no new content is loaded
            print("All property tiles are loaded.")
            break

        previous_height = current_height
