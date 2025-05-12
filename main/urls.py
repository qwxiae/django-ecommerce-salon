from .views import CatalogView, ProcedureDetailView, home, artists
from django.urls import path

app_name = "main"

urlpatterns = [
    path('', home, name='home'),
    path('artists/', artists, name='artists'),
    path('services/', CatalogView.as_view(), name='catalog'),
    path('procedure/<slug:slug>/', ProcedureDetailView.as_view(), name='procedure_detail'),
]
