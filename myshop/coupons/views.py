from django.shortcuts import render, redirect
from django.utils import timezone, decorators
from django.views.decorators.http import require_POST
from django.views import View

from .models import Coupon
from .forms import CouponApplyForm


@decorators.method_decorator(require_POST, name='dispatch')
class CouponApplyView(View):
    form_class = CouponApplyForm

    def post(self, request, *args, **kwargs):
        now = timezone.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                request.session['coupon_id'] = coupon.id
            except Coupon.DoesNotExist:
                request.session['coupon_id'] = None
            return redirect('cart:cart_detail')

