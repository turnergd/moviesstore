from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),   
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('map/', views.map_view, name='cart.map'),
    path('api/map-data/', views.map_data_api, name='cart.map_data'),
    path('set-location/', views.set_location, name='cart.set_location'),
]