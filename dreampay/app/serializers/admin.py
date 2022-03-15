from app.models import Client, Log, Admin, Cashier
from rest_framework import serializers

from dreampay.app.models import Merchant

class AdminFerivyClient(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    def Verify(admin, validated_data):
        try:
            c = Client.objects.get(phone=validated_data['phone'])
            c.is_active = True
            Log.objects.create(client_id=c, admin_id=admin, case={"usecase":"AdminFerivyClient","status":"success"})
            c.save()
        except Exception:
            return {"detail":" client not found"}
        return {"detail":" client actived successfully"}

class AdminCreateMerchant(serializers.Serializer):
    class Meta:
        model = Merchant
        fields = '__all__'
    def create(admin, validated_data):
        validated_data['admin_id']=admin
        m = Merchant.objects.create(**validated_data)
        Log.objects.create(merchant_id=m, admin_id=admin, case={"usecase":"AdminCreateMerchant","status":"success"})
        return m

class AdminCreateCashier(serializers.Serializer):
    class Meta:
        model = Cashier
        fields = '__all__'
    def create(admin, validated_data):
        validated_data['admin_id']=admin
        c = Merchant.objects.create(**validated_data)
        Log.objects.create(cashier_id=c, admin_id=admin, case={"usecase":"AdminCreateCashier","status":"success"})
        return c

class AdminTopupBalance(serializers.Serializer):
    phone = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    def TopUp(admin, validated_data):
        phone=validated_data['phone']
        total=validated_data['total']
        try:
            c = Client.objects.get(phone=phone)
            # a = Admin.objects.get(id=admin)
            balance = c.balance
            c.balance = balance + int(total)
            Log.objects.create(client_id=c, admin_id=admin, case={"usecase":"AdminTopupBalance","total":total,"status":"success"})
            c.save()
            return {"balance":balance + int(total)}
        except Exception:
            return {"detail":"client not found"}