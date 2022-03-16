from django.contrib import admin
from app.models import Admin,AdminToken,Merchant,MerchantToken,Client,ClientToken,Cashier,CashierToken,Log,TopupLog,WithdrawlLog,TransactionLog
# Register your models here.
admin.site.register([Admin,AdminToken,Merchant,MerchantToken,Client,ClientToken,Cashier,CashierToken,Log,TopupLog,WithdrawlLog,TransactionLog])
