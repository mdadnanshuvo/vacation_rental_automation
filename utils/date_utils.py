# utils/date_utils.py

from datetime import datetime, timedelta
import random


def get_random_date_range():
    """
    Generates a random date range consisting of a start date and an end date.

    The start date is randomly chosen within the next 1 to 30 days from the current date.
    The end date is randomly chosen as 1 to 7 days after the start date.

    Returns:
        tuple: A tuple containing two strings:
            - start_date (str): The randomly generated start date in 'YYYY-MM-DD' format.
            - end_date (str): The randomly generated end date in 'YYYY-MM-DD' format.

    Example:
        >>> start_date, end_date = get_random_date_range()
        >>> print(start_date, end_date)
        '2025-02-10', '2025-02-15'

    Notes:
        - This function is typically used for selecting check-in and check-out dates for testing purposes.
    """
    start_date = datetime.now() + timedelta(days=random.randint(1, 30))
    end_date = start_date + timedelta(days=random.randint(1, 7))
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
