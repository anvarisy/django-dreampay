from app.models import Client, Log, Cashier,Merchant, Admin, AdminToken, TopupLog, WithdrawlLog, TransactionLog
from rest_framework import serializers
from rest_framework import serializers
import jwt
from dreampay.settings import SECRET_KEY
import time

class AdminLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        try:
            c = Admin.objects.get(phone=phone)
            encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
            AdminToken.objects.create(admin_id=c.id, token=encoded_jwt)
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(case={"usecase":"AdminLoginSerializer","admin":c.name,"status":"success"})
        return {"admin":c.name,"token":encoded_jwt}

class AdminFerivyClient(serializers.Serializer):
    client_id = serializers.CharField(max_length=15, required=True)
    def Verify(admin, validated_data):
        try:
            c = Client.objects.get(id=validated_data['client_id'])
            c.is_active = True
            c.save()
        except Exception:
            return {"error":" client not found"}
        Log.objects.create(client_id=c, admin_id=admin, case={"usecase":"AdminFerivyClient","status":"success"})
        return {"detail":" client actived successfully"}

class AdminCreateMerchant(serializers.Serializer):
    # email = serializers.CharField(max_length=120, required=True)
    name = serializers.CharField(max_length=120, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    def create(validated_data, admin):
        try:
            email = validated_data['email'].value
            name = validated_data['name'].value
            phone = validated_data['phone'].value
            m = Merchant.objects.create(email=email,name=name,phone=phone,admin_id=admin)
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(merchant_id=m.id, admin_id=admin, case={"usecase":"AdminCreateMerchant","status":"success"})
        return {"detail":"Cashier created successfully"}
        

class AdminCreateCashier(serializers.Serializer):
    # email = serializers.CharField(max_length=120, required=True)
    name = serializers.CharField(max_length=120, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    def create(validated_data, admin):
        try:
            email = validated_data['email'].value
            name = validated_data['name'].value
            phone = validated_data['phone'].value
            c = Cashier.objects.create(email=email,name=name,phone=phone,admin_id=admin)
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(cashier_id=c.id, admin_id=admin, case={"usecase":"AdminCreateCashier","status":"success"})
        return {"detail":"Cashier created successfully"}

class AdminTopupBalance(serializers.Serializer):
    client_id = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    def TopUp(validated_data, admin):
        client_id=validated_data['client_id'].value
        total=validated_data['total'].value
        try:
            c = Client.objects.get(id=client_id)
            if c.is_active:
                balance = c.balance
                c.balance = balance + int(total)
                c.save()
                TopupLog.objects.create(client_id=c.id, admin_id=admin,total=total)
            else:
                return {"error":"client not activated"}
        except Exception:
            return {"error":"client not found"}
        Log.objects.create(client_id=c.id, admin_id=admin, case={"usecase":"AdminTopupBalance","total":total,"status":"success"})
        return {"balance":balance + int(total)}

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id','name']

class CashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashier
        fields = ['id','name']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','name']

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id','name']

class GetAllCashier(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    class Meta:
        model = Cashier
        fields = ['id','name','phone','balance','admin']
    def get_admin(self, cashier_instance):
        adm = Admin.objects.get(id=cashier_instance.admin_id)
        return AdminSerializer(adm).data

class GetAllMerchant(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields ='__all__'
   
class GetAllTopup(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    cashier = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    class Meta:
        model = TopupLog
        fields = ['id','total','client','admin','cashier','created_at']
    def get_admin(self, instance):
        try:
            adm = Admin.objects.get(id=instance.admin_id)
            return AdminSerializer(adm).data
        except Exception:
            return{"id":"","name":""}
    def get_cashier(self, instance):
        try:
            casie = Cashier.objects.get(id=instance.cashier_id)
            return CashierSerializer(casie).data
        except Exception:
            return{"id":"","name":""}
    def get_client(self, instance):
        try:
            c = Client.objects.get(id=instance.client_id)
            return ClientSerializer(c).data
        except Exception:
            return{"id":"","name":""}

class VerifyTopup(serializers.Serializer):
    topup_id = serializers.ListField(child=serializers.IntegerField())
    def UpdateAll(validated_data,admin):
        list = validated_data['topup_id'].value
        try:
            for item in list:
                t = TopupLog.objects.get(id=item)
                t.admin_id=admin
                t.save()
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(admin_id=admin, case={"usecase":"VerifyTopup","id":list,"status":"success"})
        return{"detail":"All id updated successfully"}

class GetAllClient(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class CreateWithdrawl(serializers.Serializer):
    merchant_id = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    def Withdrawl(validated_data, admin):
        merchant = validated_data['merchant_id'].value
        total = validated_data['total'].value
        try:
            m = Merchant.objects.get(id=merchant)
            balance = m.balance
            if balance < total:
                return {"error":"not enough balance for withdrawl"}
            m.balance = balance-int(total)
            m.save()
            WithdrawlLog.objects.create(admin_id=admin,merchant_id=merchant,total=total)
        except Exception as e:
            return{"error":str(e)}
        Log.objects.create(merchant_id=merchant, admin_id=admin, case={"usecase":"CreateWithdrawl","total":total,"status":"success"})
        return {"balance":balance - int(total)}

class GetAllWithdrawl(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    merchant = serializers.SerializerMethodField()
    class Meta:
        model = WithdrawlLog
        fields = ['id','total','merchant','admin','created_at']
    def get_admin(self, instance):
        try:
            adm = Admin.objects.get(id=instance.admin_id)
            return AdminSerializer(adm).data
        except Exception:
            return{"id":"","name":""}
    def get_merchant(self, instance):
        try:
            mrchnt = Merchant.objects.get(id=instance.merchant_id)
            return AdminSerializer(mrchnt).data
        except Exception:
            return{"id":"","name":""}

class GetAllTransaction(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    merchant = serializers.SerializerMethodField()
    class Meta:
        model = WithdrawlLog
        fields = ['id','total','merchant','client','created_at']
    def get_client(self, instance):
        try:
            c = Client.objects.get(id=instance.client_id)
            return ClientSerializer(c).data
        except Exception:
            return{"id":"","name":""}
    def get_merchant(self, instance):
        try:
            mrchnt = Merchant.objects.get(id=instance.merchant_id)
            return AdminSerializer(mrchnt).data
        except Exception:
            return{"id":"","name":""}

