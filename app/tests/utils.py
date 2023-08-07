import random
import string


def random_word(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def round_price(price: str) -> str:
    return f'{round(float(price), 2):.2f}'
