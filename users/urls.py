from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *


urlpatterns = [
    path('register/', UserRegister.as_view()),
    path('profile/', Profile.as_view()),
    path('login/', UserLogin.as_view()),
    path('beneficiary/', BeneficiariesView.as_view()),
    path('beneficiary/<int:id>/', BeneficiariesDetail.as_view()),
    path('transaction/', TransactionHistoryView.as_view()),
    path('transaction/<int:id>/', TransactionHistoryDetail.as_view()),
    path('transfer/', WalletTransfer.as_view()),
    path('withdraw/', WalletWithdrawal.as_view()),
    path('deposit/', WalletDeposit.as_view()),
    # path('webhooks/', KorapayWebHooksReceiver.as_view(), name='korapay_webhooks')
]
