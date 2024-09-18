# TODO: add this functionality to background tasks
class EmailService:
    @classmethod
    def send_code(cls, code: str, email: str) -> None:
        print(f'code ({code}) sent to email ({email})')

    @classmethod
    def send_transaction_factor(cls, email: str) -> None:
        print(f'transaction sent to email ({email})')

    @classmethod
    def send_reminded_message(cls, email: str) -> None:
        print(f'reminded sent to email ({email})')
