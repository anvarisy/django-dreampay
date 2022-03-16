from rest_framework.views import APIView
from app.serializers.merchant import GetAllTransaction
from app.models import TransactionLog, WithdrawlLog

from middleware.authentication import MerchantAuthentication
from app.serializers.merchant import MerchantLoginSerializer, GetAllWithdrawl
from rest_framework.response import Response
from rest_framework import generics, status

class MerchantLoginView(APIView):
    def post(self, request, format=None):
        serializer = MerchantLoginSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.Login()
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllTransactionView(generics.ListAPIView):
    authentication_classes = [MerchantAuthentication]
    serializer_class = GetAllTransaction
    def get_queryset(self, *args, **kwargs):
        merchantId = self.request.auth['id']
        queryset = TransactionLog.objects.filter(merchant_id=merchantId)
        return queryset

class GetAllWithdrawlView(generics.ListAPIView):
    authentication_classes = [MerchantAuthentication]
    serializer_class = GetAllWithdrawl
    def get_queryset(self, *args, **kwargs):
        merchantId = self.request.auth['id']
        queryset = WithdrawlLog.objects.filter(merchant_id=merchantId)
        return queryset