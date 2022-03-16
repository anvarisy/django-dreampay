from django.urls import  path
from app.views.admin import VerifyClientView,AdminLoginView, CreateMerchantView, CreateCashierView,TopupClientView,\
    GetAllCashierView,GetAllTopupView,GetAllClientView,UpdateTopuplogView,CreateWithdrawlView,GetAllWithdrawlView,\
        GetAllTransactionView

urlpatterns = [
    path('verify/',VerifyClientView.as_view()),
    path('login/',AdminLoginView.as_view()),
    path('create-merchant/',CreateMerchantView.as_view()),
    path('create-cashier/',CreateCashierView.as_view()),
    path('topup/',TopupClientView.as_view()),
    path('cashier/',GetAllCashierView.as_view()),
    path('all-topup/',GetAllTopupView.as_view()),
    path('all-client/',GetAllClientView.as_view()),
    path('update-topup/',UpdateTopuplogView.as_view()),
    path('withdrawl/',CreateWithdrawlView.as_view()),
    path('all-withdrawl/',GetAllWithdrawlView.as_view()),
    path('all-transaction/',GetAllTransactionView.as_view()),
]