# TODO: add this functionality to background tasks
class SMSService:
    @classmethod
    def send_code(cls, code: str, phone_number: int) -> None:
        print(f'code ({code}) sent to phone_number ({phone_number})')

    @classmethod
    def send_transaction_factor(cls, phone_number: int) -> None:
        print(f'transaction sent to phone_number ({phone_number})')

    @classmethod
    def send_reminded_message(cls, phone_number: str) -> None:
        print(f'reminded sent to phone_number ({phone_number})')
