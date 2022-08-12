from django.urls import path
from .views import ProductListView, product_detail

app_name = 'shop'


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    # path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
]