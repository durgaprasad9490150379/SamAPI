from django.urls import path
from . import views

urlpatterns = [
    # path('list/', views.list),
    path('create/', views.create),
    path('delete/<slug:username>', views.delete),
    path('enable_user/<slug:username>', views.enable),
    path('disable_user/<slug:username>', views.disable),
    path('set_expiry/', views.set_expiry),
    path('list/', views.list),
    path('show/<slug:name>', views.show),
    path('move/', views.move),
    path('edit/<slug:username>', views.edit),
    path('set_password/', views.set_password),
]

