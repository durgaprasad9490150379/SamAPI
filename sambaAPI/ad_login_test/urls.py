from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.create),
    # path('list/', views.list),
    # path('delete/<slug:name>', views.delete),
    # path('rename/<slug:old_name>', views.rename),
    # path('edit/<slug:name>', views.edit)
]

