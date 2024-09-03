from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


class Epoch:
    datetime_format_ = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def now(cls, ):
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())  # second

    @classmethod
    def last_month(cls):
        return int((datetime.utcnow().replace(tzinfo=timezone.utc) - relativedelta(months=1)).timestamp())

    @classmethod
    def last_days(cls, days):
        return int((datetime.utcnow().replace(tzinfo=timezone.utc) - relativedelta(days=int(days))).timestamp())

    @classmethod
    def microsecond_now(cls, ):
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() * 1000000)  # microsecond

    @classmethod
    def epoch_to_local_datetime(cls, epoch):
        return datetime.fromtimestamp(epoch)

    @classmethod
    def epoch_to_utc_datetime(cls, epoch, datetime_format=datetime_format_):
        return datetime.utcfromtimestamp(epoch)

    @classmethod
    def epoch_to_string_local_datetime(cls, epoch, datetime_format=datetime_format_):
        return datetime.fromtimestamp(epoch).strftime(datetime_format)

    @classmethod
    def epoch_to_string_utc_datetime(cls, epoch, datetime_format=datetime_format_):
        return datetime.utcfromtimestamp(epoch).strftime(datetime_format)

    @classmethod
    def string_local_datetime_to_epoch(cls, datetime_str, datetime_format=datetime_format_):
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
        return int(datetime_obj.timestamp())  # in milliseconds

    @classmethod
    def string_utc_datetime_to_epoch(cls, datetime_str, datetime_format=datetime_format_):
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
        return int(datetime_obj.replace(tzinfo=timezone.utc).timestamp())  # in milliseconds
