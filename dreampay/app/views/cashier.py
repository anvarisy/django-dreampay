from rest_framework.views import APIView

from middleware.authentication import CashierAuthentication
from rest_framework.response import Response
from rest_framework import generics, status
from app.serializers.cashier import CashierLoginSerializer,CashierTopupBalance, GetAllClient, GetAllTopup
from django_filters.rest_framework import DjangoFilterBackend
from app.models import Client,TopupLog

class CashierLoginView(APIView):
    def post(self, request, format=None):
        serializer = CashierLoginSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.Login()
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopupClientView(APIView):
    authentication_classes = [CashierAuthentication]
    def post(self, request, format=None):
        serializer = CashierTopupBalance(data=request.data)
        if serializer.is_valid():
            cashierId = request.auth['id']
            res = serializer.TopUp(cashierId)
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllClientView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'phone']
    authentication_classes = [CashierAuthentication]
    queryset = Client.objects.filter(is_active=True)
    serializer_class = GetAllClient

class GetAllTopupView(generics.ListAPIView):
    authentication_classes = [CashierAuthentication]
    serializer_class = GetAllTopup
    def get_queryset(self, *args, **kwargs):
        cashierId = self.request.auth['id']
        queryset = TopupLog.objects.filter(cashier_id=cashierId)
        return queryset