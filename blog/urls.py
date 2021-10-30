from django.urls import path

from . import views

urlpatterns = [
    path('b/ee477c1859d67eb03f9e04eb63c89f19', views.index, name='index'),
    path('c/new', views.crypto_index, name='crypto_index'),
    path('c/new/single_crypto', views.crypto_get_single, name='crypto_get_single'),
    path('cu/new/', views.currency, name='currency'),
    path('s/new/', views.stocks, name='stocks'),
]