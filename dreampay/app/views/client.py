from app.serializers.client import ClientLoginSerializer, ClientRegisterSerializer, ClientTransactionSerializer, GetAllTransaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from middleware.authentication import ClientAuthentication
from app.models import TransactionLog
class ClientLoginView(APIView):
    def post(self, request, format=None):
        serializer = ClientLoginSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.Login()
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientRegisterView(APIView):
    def post(self, request, format=None):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.Register()
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientTransactionView(APIView):
    authentication_classes = [ClientAuthentication]
    def post(self, request, format=None):
        serializer = ClientTransactionSerializer(data=request.data)
        if serializer.is_valid():
            clientId = request.auth['id']
            res = serializer.Transaction(clientId)
            if "error" in str(res):
                return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllTransactionView(generics.ListAPIView):
    authentication_classes = [ClientAuthentication]
    
    serializer_class = GetAllTransaction
    def get_queryset(self, *args, **kwargs):
        clientId = self.request.auth['id']
        print(clientId)
        queryset = TransactionLog.objects.filter(client_id=clientId)
        return queryset