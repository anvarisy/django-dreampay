
from rest_framework import serializers
import jwt
from app.models import Admin,AdminToken,Merchant,MerchantToken,Cashier,\
    CashierToken,Client,ClientToken, Log
from dreampay.settings import SECRET_KEY
import time



class MerchantLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    # password = serializers.CharField(max_length=40, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        # password = validated_data.data['password']
        try:
            c = Merchant.objects.get(phone=phone)
            # decPass = jwt.decode(c.password, SECRET_KEY, algorithm="HS256")
            # if decPass != password:
            #     return {"merchant":"password not match"}
            encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
            Log.objects.create(case={"usecase":"MerchantLoginSerializer","merchant":c.name,"status":"success"})
            MerchantToken.objects.create(client=c, token=encoded_jwt)
        except Exception:
            return {"merchant":"not found"}
        return {"merchant":c.name,"token":encoded_jwt}

class CashierLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    # password = serializers.CharField(max_length=40, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        # password = validated_data.data['password']
        try:
            c = Cashier.objects.get(phone=phone)
            # decPass = jwt.decode(c.password, SECRET_KEY, algorithm="HS256")
            # if decPass != password:
            #     return {"merchant":"password not match"}
            encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
            Log.objects.create(case={"usecase":"CashierLoginSerializer","cashier":c.name,"status":"success"})
            CashierToken.objects.create(cashier_id=c.id, token=encoded_jwt)
        except Exception:
            return {"cashier":"not found"}
        return {"cashier":c.name,"token":encoded_jwt}

class ClientLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    # password = serializers.CharField(max_length=40, required=True)
    def Login(validated_data):
        phone = validated_data.data['phone']
        # password = validated_data.data['password']
        try:
            c = Client.objects.get(phone=phone)
            # decPass = jwt.decode(c.password, SECRET_KEY, algorithm="HS256")
            # if decPass != password:
            #     return {"client":"password not match"}
            encoded_jwt = jwt.encode({"id": c.id,"phone":c.phone,"time":time.time()}, SECRET_KEY, algorithm="HS256")
            Log.objects.create(case={"usecase":"ClientLoginSerializer","client":c.name,"status":"success"})
            ClientToken.objects.create(client_id=c.id, token=encoded_jwt)
        except Exception:
            return {"client":"not found"}
        return {"client":c.name,"token":encoded_jwt}