import random

from utils.epoch import Epoch


class OTPService:
    @classmethod
    def generate(cls):
        token = list(str(Epoch.microsecond_now())[-6:])
        random.shuffle(token)
        return ''.join(token)
