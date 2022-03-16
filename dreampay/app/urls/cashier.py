from django.urls import  path

from app.views.cashier import CashierLoginView,TopupClientView,GetAllClientView,GetAllTopupView

urlpatterns = [
    path('login/',CashierLoginView.as_view()),
    path('topup/',TopupClientView.as_view()),
    path('all-client/',GetAllClientView.as_view()),
    path('all-topup/',GetAllTopupView.as_view()),
]