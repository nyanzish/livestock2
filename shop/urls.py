from django.urls import path
from . import views
from livestock import settings
from django.conf.urls.static import static


app_name= "shop"

urlpatterns=[
	path('', views.HomeView.as_view(), name='home'),
	path('cart/', views.OrderSummaryView.as_view(), name='cart'),
	path('pay/', views.pay, name='pay'),
	path('checkout/', views.checkout, name='checkout'),
	path('cart/checkout/', views.checkout, name='checkout'),
	path('farmer/', views.post_product, name='post_product'),
	path('farmer_register/', views.reg_farmer, name='reg_farmer'),
	path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
	path('product/<slug>/', views.product, name='product'),
	path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
	path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
	path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
	path('mymarket/', views.MarketView.as_view(), name='mymarket'),
	path('product_upload/', views.product_upload, name='product_upload')




]
#path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)