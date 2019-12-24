from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list),
    path('create/', views.create),
    path('delete/<slug:computer_name>', views.delete),
    path('show/<slug:computer_name>', views.show),
    path('move/', views.move)
]
