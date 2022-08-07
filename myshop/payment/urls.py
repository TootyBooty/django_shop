from django.urls import path

from .views import PaymentProcessView, payment_done, payment_canceled

app_name = 'payment'


urlpatterns = [
    path('process/', PaymentProcessView.as_view(), name='process'),
    path('done/', payment_done, name='done'),
    path('canceled/', payment_canceled, name='canceled'),
]