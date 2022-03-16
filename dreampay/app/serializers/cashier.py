from rest_framework import serializers
import jwt
from app.models import Cashier,CashierToken,Client,Log,TopupLog, Admin
from dreampay.settings import SECRET_KEY
import time


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
            CashierToken.objects.create(cashier_id=c.id, token=encoded_jwt)
        except Exception:
            return {"error":"not found"}
        Log.objects.create(case={"usecase":"CashierLoginSerializer","cashier":c.name,"status":"success"})
        return {"cashier":c.name,"token":encoded_jwt}

class CashierTopupBalance(serializers.Serializer):
    client_id = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    def TopUp(validated_data, cashier):
        client_id=validated_data['client_id'].value
        total=validated_data['total'].value
        try:
            c = Client.objects.get(id=client_id)
            if c.is_active:
                balance = c.balance
                c.balance = balance + int(total)
                c.save()
                TopupLog.objects.create(client_id=c.id, cashier_id=cashier,total=total)
            else:
                return {"error":"client not activated"}
        except Exception:
            return {"error":"client not found"}
        Log.objects.create(client_id=c.id, cashier_id=cashier, case={"usecase":"CashierTopupBalance","total":total,"status":"success"})
        return {"balance":balance + int(total)}

class GetAllClient(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

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