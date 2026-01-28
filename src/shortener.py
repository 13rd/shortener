import string
from secrets import choice

ALPHABET: str = string.ascii_letters + string.digits

def generate_random_slug(length: int = 6) -> str:
    slug = ""
    for _ in range(length):
        slug += choice(ALPHABET)
    return slug