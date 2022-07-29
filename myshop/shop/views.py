from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View

from cart.forms import CartAddProductForm
from .models import Category, Product


class ProductListView(View):
    template_name = 'shop/product/list.html'

    def get(self, request, category_slug=None, *args, **kwargs):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, self.template_name, context=context)
    

# class ProductDetailView(View):
#     template_name = 'shop/product/detail.html'
#     form_class = CartAddProductForm

#     def post(self, request, id, slug, *args, **kwargs):
#         product = get_object_or_404(Product, pk=id, slug=slug, available=True)
#         cart_product_form = self.form_class()
#         context = {
#             'product': product,
#             'cart_product_form': cart_product_form
#         }
#         return render(request, self.template_name, context=context)

#     def get(self, request, id, slug, *args, **kwargs):
#         product = get_object_or_404(Product, pk=id, slug=slug, available=True)
#         cart_product_form = self.form_class()
#         context = {
#             'product': product,
#             'cart_product_form': cart_product_form
#         }
#         return render(request, self.template_name, context=context)
        

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True) 
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,'cart_product_form': cart_product_form})