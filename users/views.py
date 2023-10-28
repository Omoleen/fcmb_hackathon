from rest_framework import generics, status, permissions, renderers
from .serializers import *
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class UserRegister(generics.GenericAPIView):
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    # renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'{list(serializer.errors.keys())[0]} - {list(serializer.errors.values())[0][0]}'
            }, status=status.HTTP_400_BAD_REQUEST)


class Profile(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        return Response({
            'data': self.serializer_class(request.user).data
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'{list(serializer.errors.keys())[0]} - {list(serializer.errors.values())[0][0]}'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.GenericAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User logged in',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({
                'message': f'{list(serializer.errors.keys())[0]} - {list(serializer.errors.values())[0][0]}'
            }, status=status.HTTP_400_BAD_REQUEST)


class BeneficiariesView(generics.GenericAPIView):
    serializer_class = BeneficiaryContactSerializer

    def get_queryset(self):
        return self.request.user.beneficiaries.all()

    def get(self, request, **kwargs):
        return Response({
            'data': self.serializer_class(self.get_queryset(), many=True).data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'beneficiary registered',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'{list(serializer.errors.keys())[0]} - {list(serializer.errors.values())[0][0]}'
            }, status=status.HTTP_400_BAD_REQUEST)


class BeneficiariesDetail(generics.GenericAPIView):
    serializer_class = BeneficiaryContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.user.beneficiaries.all()

    def get(self, request, **kwargs):
        return Response({
            'data': self.serializer_class(self.get_object()).data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionHistoryView(generics.GenericAPIView):
    serializer_class = TransactionHistorySerializer

    def get_queryset(self):
        return self.request.user.transaction_histories.all()

    def get(self, request, **kwargs):
        return Response({
            'data': self.serializer_class(self.get_queryset(), many=True).data
        }, status=status.HTTP_200_OK)


class TransactionHistoryDetail(generics.GenericAPIView):
    serializer_class = TransactionHistorySerializer

    def get_queryset(self):
        return self.request.user.transaction_histories.all()

    def get(self, request, **kwargs):
        return Response({
            'data': self.serializer_class(self.get_object()).data
        }, status=status.HTTP_200_OK)


# class WalletTransfer(generics.GenericAPIView):
    # se