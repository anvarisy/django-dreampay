from django.urls import  path

from app.views.merchant import MerchantLoginView,GetAllTransactionView,GetAllWithdrawlView
urlpatterns = [
path('login/',MerchantLoginView.as_view()),
path('all-transaction/',GetAllTransactionView.as_view()),
path('all-withdrawl/',GetAllWithdrawlView.as_view()),
]