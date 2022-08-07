from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .tasks import payment_message

import braintree

from orders.models import Order


class PaymentProcessView(View):
    payment_process_template = 'payment/process.html'

    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        # Формирование одноразового токена для JS SDK.
        client_token = braintree.ClientToken.generate()
        return render(request, self.payment_process_template, {'order': order, 'client_token': client_token})

    def post(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        # Получение токена для создания транзакции
        nonce = request.POST.get('payment_method_nonce', None)
        # Создание и сохранение транзакции
        result = braintree.Transaction.sale({
            'amount': f'{order.get_total_cost():.2f}',
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            # Отметка заказа как оплаченного 
            order.paid = True
            # Сохранение ID транзакции в заказе
            order.braintree_id = result.transaction.id
            order.save()
            payment_message.delay(order_id)

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')


def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')