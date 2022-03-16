from rest_framework import serializers
import jwt
from app.models import Client,ClientToken, Log,TransactionLog, Merchant
from dreampay.settings import SECRET_KEY
import time

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','name']

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id','name']


class ClientLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        try:
            c = Client.objects.get(phone=phone)
            if c.is_active:
                encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
                ClientToken.objects.create(client_id=c.id, token=encoded_jwt)
            else:
                return {"error":"client not activated"}
        except Exception:
            return {"error":"client not found"}
        Log.objects.create(case={"usecase":"ClientLoginSerializer","client":c.name,"status":"success"})
        return {"client":c.name,"token":encoded_jwt}

class ClientRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    name = serializers.CharField(max_length=60, required=True)
    def Register(validated_data):
        phone = validated_data.data['phone']
        name = validated_data.data['name']
        try:
            c = Client.objects.create(phone=phone,name=name)
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(case={"usecase":"ClientRegisterSerializer","client":c.name,"status":"success"})
        return {"detail":"client registered successfully"}

class ClientTransactionSerializer(serializers.Serializer):
    total = serializers.IntegerField( required=True)
    merchant_id = serializers.IntegerField(required=True)
    def Transaction(validated_data, client):
        total = validated_data.data['total']
        merchant_id = validated_data.data['merchant_id']
        try:
            c = Client.objects.get(id=client)
            if c.balance <= total:
                return {"error":"not enough balance"}
            if c.is_active:
                c.balance-=total
                c.save()
                m = Merchant.objects.get(id=merchant_id)
                m.balance+=total
                m.save()
                TransactionLog.objects.create(total=total,merchant_id=merchant_id,client_id=c.id)
            else:
                return {"error":"client not activated"}
        except Exception as e:
            return {"error":str(e)}
        Log.objects.create(case={"usecase":"ClientTransactionSerializer","client":c.name,"merchant":m.name,"total":total,"status":"success"})
        return {"detail":"client transaction successfully"}

class GetAllTransaction(serializers.ModelSerializer):
    merchant = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    class Meta:
        model = TransactionLog
        fields = ['id','total','client','merchant','created_at']
    def get_merchant(self, instance):
        try:
            mrcn = Merchant.objects.get(id=instance.merchant_id)
            return MerchantSerializer(mrcn).data
        except Exception:
            return{"id":"","name":""}
    def get_client(self, instance):
        try:
            c = Client.objects.get(id=instance.client_id)
            return ClientSerializer(c).data
        except Exception:
            return{"id":"","name":""}