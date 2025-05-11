from .views import CatalogView, DetailView, home, artists
from django.urls import path

app_name = "main"

urlpatterns = [
    path('', home, name='home'),
    path('artists/', artists, name='artists'),
    path('services/', CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', DetailView.as_view(), name='product_detail'),
]
