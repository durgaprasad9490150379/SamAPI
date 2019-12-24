from django.db import models

# Create your models here.
class ComputerMgmt(models.Model):
    computer_name = models.CharField(max_length=200,primary_key=True)
    domain_container = models.CharField(max_length=200)
    description = models.CharField(max_length=200)


class ComputerReport(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    dn = models.CharField(max_length=255)
    objectClass = models.CharField(max_length=255)
    cn = models.CharField(max_length=255)
    sn = models.CharField(max_length=255)
    description = models.TextField(default='')
    instanceType = models.CharField(max_length=255)
    whenCreated = models.CharField(max_length=255)
    whenChanged = models.CharField(max_length=255)
    uSNCreated = models.CharField(max_length=255)
    badPwdCount = models.CharField(max_length=255)
    codePage = models.CharField(max_length=255)
    countryCode = models.CharField(max_length=255)
    badPasswordTime = models.CharField(max_length=255)
    lastLogoff = models.CharField(max_length=255)
    lastLogon = models.CharField(max_length=255)
    primaryGroupID = models.CharField(max_length=255)
    accountExpires = models.CharField(max_length=255)
    logonCount = models.CharField(max_length=255)
    sAMAccountName = models.CharField(max_length=255)
    sAMAccountType = models.CharField(max_length=255)
    objectCategory = models.CharField(max_length=255)
    pwdLastSet = models.CharField(max_length=255)
    userAccountControl = models.CharField(max_length=255)
    isCriticalSystemObject = models.CharField(max_length=255)
    uSNChanged = models.CharField(max_length=255)
    distinguishedName = models.CharField(max_length=255)



