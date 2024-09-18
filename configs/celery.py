import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('configs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'pending-orders-management': {
        'task': 'apps.shopping.tasks.pending_orders_management',
        'schedule': crontab(hour='0', minute='0'),
    },
}
