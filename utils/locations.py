# utils/locations.py

from faker import Faker

fake = Faker()


def get_random_location():
    """
      Generates a random city name using the Faker library.

    This function is typically used to simulate user input for testing location-based
    search functionality in applications.

    Returns:
        str: A randomly generated city name.

    Example:
        >>> location = get_random_location()
        >>> print(location)
        'San Francisco'

    Notes:
        - The city names are generated based on the locale set in the `Faker` library.
        - Ensure the `Faker` package is installed in your environment before using this function.
    """
    return fake.city()
