from django.urls import path

from . import views

urlpatterns = [
    path('b/ee477c1859d67eb03f9e04eb63c89f19', views.index, name='index'),
    path('c/new', views.crypto_index, name='crypto_index'),
    path('c/new/single_crypto', views.crypto_get_single, name='crypto_get_single'),
    path('c/new/all_crypto', views.get_all_crypto_name, name='all_crypto'),
    path('cu/new/', views.currency, name='currency'),
    path('cu/new/single_exchange', views.currency_get_single, name='currency_get_single'),
    path('cu/new/all_exchanges', views.get_all_currency_name, name='all_exchanges'),
    path('s/new/', views.stocks, name='stocks'),
]