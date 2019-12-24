from django.db import models
from rest_framework.urlpatterns import format_suffix_patterns

# Create your models here.

class ad_login_input(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    domain_controller=models.CharField(max_length=20)

    def __str__(self):
        return self.username

