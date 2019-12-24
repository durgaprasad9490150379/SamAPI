from django.db import models

# Create your models here.
class OrgUnit(models.Model):
	name = models.CharField(max_length=255,primary_key=True)
	description = models.TextField()
	domain_name = models.TextField()

class OrgUnitReport(models.Model):
	ou_name = models.CharField(max_length=255,primary_key=True)
	description = models.TextField()
	domain_name = models.CharField(max_length=255)
	distinguished_name = models.CharField(max_length=255)
	when_changed = models.CharField(max_length=255)
	when_Created = models.CharField(max_length=255)
	object_guid = models.TextField()
	zip_code = models.CharField(max_length=100)
	street_Address = models.TextField()
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	managed_by = models.TextField()
