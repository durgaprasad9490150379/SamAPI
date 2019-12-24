from django.db import models

# Create your models here.
class Domain(models.Model):
	#domain_id = models.AutoField(primary_key=True)
	domain_name = models.CharField(max_length=200,primary_key=True)
	domain_controller = models.TextField(null=False)
	username = models.CharField(max_length=200, null=False)
	password = models.CharField(max_length=200, null=False)
	default_name = models.CharField(max_length=200)
	status = models.CharField(max_length=200, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
