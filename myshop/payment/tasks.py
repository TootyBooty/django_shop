from myshop.celery import app

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from orders.models import Order

import os
from io import BytesIO
import pdfkit

@app.task
def payment_message(order_id):
    order = Order.objects.get(pk=order_id)
    # Создание электронного сообщения.
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.' 
    email = EmailMessage(subject,
                            message, 
                            settings.EMAIL_HOST_USER, 
                            [order.email]) 
    # Формирование PDF.
    html = render_to_string('orders/order/pdf.html', {'order': order})
    pdf_file_path = os.path.join(settings.ORDERS_PDF_ROOT, f'send_order_{order_id}.pdf')
    out = BytesIO()
    pdfkit.from_string(html, pdf_file_path, css=settings.STATIC_ROOT + 'css/pdf.css', options={'encoding': 'UTF-8'})

    with open(pdf_file_path, 'rb') as f:
        out.write(f.read())
        
    # # Прикрепляем PDF к электронному сообщению.
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    # Отправка сообщения.
    email.send()
    os.remove(pdf_file_path) 