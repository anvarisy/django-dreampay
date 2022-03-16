from django.urls import  path

from app.views.client import ClientLoginView,ClientRegisterView,ClientTransactionView,GetAllTransactionView

urlpatterns = [
    path('login/',ClientLoginView.as_view()),
    path('register/',ClientRegisterView.as_view()),
    path('transaction/',ClientTransactionView.as_view()),
    path('all-transaction/',GetAllTransactionView.as_view()),
]