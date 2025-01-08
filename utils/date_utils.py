# utils/date_utils.py

from datetime import datetime, timedelta
import random

def get_random_date_range():
    start_date = datetime.now() + timedelta(days=random.randint(1, 30))
    end_date = start_date + timedelta(days=random.randint(1, 7))
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')