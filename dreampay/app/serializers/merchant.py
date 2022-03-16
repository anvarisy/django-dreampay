from rest_framework import serializers
import jwt
from app.models import Merchant,MerchantToken, Log, Admin, Client, TransactionLog, WithdrawlLog
from dreampay.settings import SECRET_KEY
import time

class MerchantLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        try:
            c = Merchant.objects.get(phone=phone)
            encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
            Log.objects.create(case={"usecase":"MerchantLoginSerializer","merchant":c.name,"status":"success"})
            MerchantToken.objects.create(merchant_id=c.id, token=encoded_jwt)
        except Exception:
            return {"error":"not found"}
        Log.objects.create(case={"usecase":"MerchantLoginSerializer","merchant":c.name,"status":"success"})
        return {"merchant":c.name,"token":encoded_jwt}

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id','name']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','name']

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id','name']

class GetAllTransaction(serializers.ModelSerializer):
    merchant = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    class Meta:
        model = TransactionLog
        fields = ['id','total','client','merchant','created_at']
    def get_merchant(self, instance):
        try:
            casie = Merchant.objects.get(id=instance.merchant_id)
            return MerchantSerializer(casie).data
        except Exception:
            return{"id":"","name":""}
    def get_client(self, instance):
        try:
            c = Client.objects.get(id=instance.client_id)
            return ClientSerializer(c).data
        except Exception:
            return{"id":"","name":""}

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