from django.db import models

# Create your models here.
class grpmgmt(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    container = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    group_type = models.CharField(max_length=255)
    group_scope = models.CharField(max_length=255)
    mail_id = models.CharField(max_length=255)
    notes = models.TextField()

class grpmembers(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
