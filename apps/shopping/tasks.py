from celery import shared_task

from apps.shopping.models import Order
from apps.users.services.sms import SMSService
from apps.users.services.email import EmailService


@shared_task()
def pending_orders_management():
    reminded_orders = Order.objects.filter(reminded=True).values_list('user', flat=True).distinct()

    for order_obj in reminded_orders:
        if order_obj.user.phone_number is not None:
            EmailService.send_reminded_message(order_obj.user.email)
        if order_obj.user.email is not None:
            SMSService.send_reminded_message(order_obj.user.phone_number)

        order_obj.reminded = True
        order_obj.save(update_fields=['reminded'])
