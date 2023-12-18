import string
import random

def generate_ext(length=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(length))

def generate_unique_ext(instance, length=10):
    """ Create unique ext_id of alphanumeric characters """
    ext_id = generate_ext(length)
    while not instance.check_unique(ext_id):
        ext_id = generate_ext(length)
    return ext_id