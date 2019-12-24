from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create),
    path('list/', views.list),
    path('list_members/<slug:name>', views.list_members),
    path('delete/<slug:name>', views.delete),
    path('add_members/', views.add_members),
    path('remove_members/', views.remove_members),
    path('show/<slug:name>', views.show),
]
