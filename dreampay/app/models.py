from django.db import models
from django.db.models import JSONField
import datetime
import pytz
from django.utils import timezone
myDate = datetime.datetime.now(pytz.utc)
# Create your models here.
class Admin(models.Model):
    email = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    # password = models.CharField(max_length=240, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
class AdminToken(models.Model):
    token = models.CharField(max_length=360, blank=True, null=True)
    admin = models.ForeignKey(Admin, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default = True)

class Merchant(models.Model):
    email = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    balance = models.IntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    admin = models.ForeignKey(Admin,blank=True,null=True,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateField(blank=True, null=True)

class MerchantToken(models.Model):
    token = models.CharField(max_length=360, blank=True, null=True)
    merchant = models.ForeignKey(Merchant, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default = True)

class Cashier(models.Model):
    email = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    # password = models.CharField(max_length=240, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    balance = models.IntegerField(default=0)
    admin = models.ForeignKey(Admin,blank=True,null=True,related_name='admin_on_cashier', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateField(blank=True, null=True)

class CashierToken(models.Model):
    token = models.CharField(max_length=360, blank=True, null=True)
    cashier = models.ForeignKey(Cashier, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default = True)

class Client(models.Model):
    email = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    # password = models.CharField(max_length=240, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateField(blank=True, null=True)

class ClientToken(models.Model):
    token = models.CharField(max_length=360, blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default = True)

class Log (models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.DO_NOTHING)
    cashier = models.ForeignKey(Cashier, blank=True, null=True, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Admin, blank=True, null=True, on_delete=models.DO_NOTHING)
    merchant = models.ForeignKey(Merchant, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    case = JSONField()
    def __str__(self) -> str:
        return self.case

class TopupLog(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Admin, blank=True, null=True, on_delete=models.DO_NOTHING)
    cashier = models.ForeignKey(Cashier, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.IntegerField(default=0)

class WithdrawlLog(models.Model):
    merchant = models.ForeignKey(Merchant, blank=True, null=True, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Admin, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.IntegerField(default=0)

class TransactionLog(models.Model):
    merchant = models.ForeignKey(Merchant, blank=True, null=True, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.IntegerField(default=0)