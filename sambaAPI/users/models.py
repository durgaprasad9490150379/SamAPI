from django.db import models

# Create your models here.
class UsersModel(models.Model):
    username = models.CharField(max_length=255,primary_key=True)
    password = models.CharField(max_length=255)
    userou = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    mail_address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)



class UserReport(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    dn = models.CharField(max_length=255)
    objectClass = models.CharField(max_length=255)
    cn = models.CharField(max_length=255)
    sn = models.CharField(max_length=255)
    description = models.TextField(default='')
    givenName = models.CharField(max_length=255)
    instanceType = models.CharField(max_length=255)
    whenCreated = models.CharField(max_length=255)
    whenChanged = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)
    uSNCreated = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
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
    userPrincipalName = models.CharField(max_length=255)
    objectCategory = models.CharField(max_length=255)
    pwdLastSet = models.CharField(max_length=255)
    userAccountControl = models.CharField(max_length=255)
    uSNChanged = models.CharField(max_length=255)
    memberOf = models.CharField(max_length=255)
    memberOf = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    telephoneNumber = models.CharField(max_length=255)
    distinguishedName = models.CharField(max_length=255)



