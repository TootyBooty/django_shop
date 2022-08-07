from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import reverse
from django.views import View

import pdfkit
import os

from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


class OrderCreateView(View):
    order_create_template = 'orders/order/create.html'
    form_class = OrderCreateForm

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = self.form_class()
        return render(request, self.order_create_template, {'cart': cart, 'form': form})


    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'])

            # Очищаем корзину
            cart.clear()
            # Запуск асинхронной задачи
            order_created.delay(order.id)
            # Сохранение заказа в сессии
            request.session['order_id'] = order.id
            # Перенаправление на страницу оплаты
            return redirect(reverse('payment:process'))

    
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    pdf_file_path = os.path.join(settings.ORDERS_PDF_ROOT, f'order_{order_id}.pdf')
    pdfkit.from_string(html, pdf_file_path, css=settings.STATIC_ROOT + 'css/pdf.css', options={'encoding': 'UTF-8'})
 
    try:
        response = FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
        os.remove(pdf_file_path)
    except FileNotFoundError:
        raise Http404()
    except: pass 

    return response