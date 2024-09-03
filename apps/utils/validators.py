from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = '^[a-zA-Z][a-zA-Z0-9_\.]+$'
    message = ('Enter a valid username starting with a-z. '
               'This value may contain only letters, numbers and underscore characters.'),
    code = 'invalid_username'


class PhoneNumberValidator(RegexValidator):
    regex = '^98(9[0-6,9]\d{8}|[1-9]\d{9})$'
    message = 'Phone number must be a VALID 12 digits like 98xxxxxxxxxx'
    code = 'invalid_phone_number'


validate_phone_number = PhoneNumberValidator()
validate_username = UsernameValidator()
