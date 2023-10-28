from rest_framework import generics, status, permissions, renderers
from .serializers import *
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class AdvertisedLoanView(generics.GenericAPIView):
    serializer_class = AdvertisedLoanSerializer


class AdvertisedLoanDetail(generics.GenericAPIView):
    serializer_class = AdvertisedLoanSerializer


class LoanView(generics.GenericAPIView):
    serializer_class = LoanSerializer


class LoanDetail(generics.GenericAPIView):
    serializer_class = LoanSerializer


class LoanRepaymentView(generics.GenericAPIView):
    serializer_class = LoanRepaymentSerializer


class LoanRepaymentDetail(generics.GenericAPIView):
    serializer_class = LoanRepaymentSerializer