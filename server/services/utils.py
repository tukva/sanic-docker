import random
import string


def generate_session_id():
    return ''.join([random.choices(string.digits + string.ascii_letters)[0] for _ in range(32)])
