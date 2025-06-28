import random
import string # to generate random strings
from datetime import datetime

# Generate Random Name
def generate_random_name(prefix="user"):
    return f"{prefix}_{random.randint(1000, 9999)}"

# Generate Today's Date

def get_today_date(format="%Y%m%d"):  # You can change format to "%d-%b-%Y" etc.
    return datetime.now().strftime(format)

# combines random name + today's date:
def generate_random_name_with_date(prefix="user"):
    today = datetime.now().strftime("%Y%m%d")  # e.g., 20250628
    rand = random.randint(1000, 9999)
    return f"{prefix}_{today}_{rand}"


