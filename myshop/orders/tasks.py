from myshop.celery import app

from django.conf import settings
from django.core.mail import send_mail


from .models import Order


@app.task
def order_created(order_id):
    """   Задача отправки email уведомлений при успешном оформлении заказа   """
    order = Order.objects.get(pk=order_id)
    subject = f'Order number {order_id}'
    message = f'Dear {order.first_name}\n\nYou have successfully placed an order.\
        Your order id is {order.id}.'
    mail_sent = send_mail(subject,
    message,
    settings.EMAIL_HOST_USER,
    [order.email])
    return mail_sent

