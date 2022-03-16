from rest_framework.views import APIView
from app.serializers.admin import AdminFerivyClient, AdminLoginSerializer,AdminCreateMerchant,AdminCreateCashier,\
    AdminTopupBalance,GetAllCashier,GetAllTopup,GetAllClient,VerifyTopup,CreateWithdrawl,GetAllWithdrawl,GetAllTransaction
from middleware.authentication import AdminAuthentication
from rest_framework.response import Response
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from app.models import Cashier,TopupLog, Client, WithdrawlLog, TransactionLog
# Create your views here.
class VerifyClientView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = AdminFerivyClient(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.Verify(adminId)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(APIView):
    def post(self, request, format=None):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.Login()
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateMerchantView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = AdminCreateMerchant(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.create(adminId)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCashierView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = AdminCreateCashier(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.create(adminId)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopupClientView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = AdminTopupBalance(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.TopUp(adminId)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCashierView(generics.ListAPIView):
    authentication_classes = [AdminAuthentication]
    queryset = Cashier.objects.all()
    serializer_class = GetAllCashier

class GetAllTopupView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_id', 'cashier_id']
    authentication_classes = [AdminAuthentication]
    queryset = TopupLog.objects.all()
    serializer_class = GetAllTopup

class GetAllClientView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phone']
    authentication_classes = [AdminAuthentication]
    queryset = Client.objects.all()
    serializer_class = GetAllClient

class UpdateTopuplogView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = VerifyTopup(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.UpdateAll(adminId)
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateWithdrawlView(APIView):
    authentication_classes = [AdminAuthentication]
    def post(self, request, format=None):
        serializer = CreateWithdrawl(data=request.data)
        if serializer.is_valid():
            adminId = request.auth['id']
            res = serializer.Withdrawl(adminId)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllWithdrawlView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['merchant_id']
    authentication_classes = [AdminAuthentication]
    queryset = WithdrawlLog.objects.all()
    serializer_class = GetAllWithdrawl

class GetAllTransactionView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_id','merchant_id']
    authentication_classes = [AdminAuthentication]
    queryset = TransactionLog.objects.all()
    serializer_class = GetAllTransaction