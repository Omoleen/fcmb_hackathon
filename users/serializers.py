import hashlib
import secrets

import requests
from django.urls import reverse
from rest_framework import serializers
from .models import *
from phonenumber_field.serializerfields import PhoneNumberField
from django.conf import settings


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=512, read_only=True)
    refresh = serializers.CharField(max_length=512,  read_only=True)

    class Meta:
        exclude = []


class BeneficiaryContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryContact
        exclude = ['user']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            user=self.context['request'].user,
            **validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(read_only=True)
    phone_number = PhoneNumberField()
    beneficiaries = BeneficiaryContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            'wallet': {
                'read_only': True
            },
            'otp': {
                'read_only': True
            },
            'credit_score': {
                'read_only': True
            },
            'date_joined': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'password': {
                'write_only': True
            },
        }
        exclude = ['user_permissions', 'groups',
                   'is_admin', 'is_staff', 'is_active',
                   'is_superuser']

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.Meta.model.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({
                'phone_number': 'already exists'
            })
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    beneficiaries = BeneficiaryContactSerializer(many=True, read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            'wallet': {
                'read_only': True
            },
            'otp': {
                'read_only': True
            },
            'credit_score': {
                'read_only': True
            },
            'date_joined': {
                'read_only': True
            },
            'last_login': {
                'read_only': True
            },
            'phone_number': {
                'read_only': True
            },
        }
        exclude = ['user_permissions', 'groups',
                   'is_admin', 'is_staff', 'is_active',
                   'is_superuser', 'password']

    def update(self, instance: User, validated_data):
        instance.location_lat = validated_data.get('location_lat', instance.location_lat)
        instance.location_long = validated_data.get('location_long', instance.location_long)
        instance.address = validated_data.get('address', instance.address)
        instance.verify_ID_name = validated_data.get('verify_ID_name', instance.verify_ID_name)
        instance.is_agent = validated_data.get('is_agent', instance.is_agent)
        if validated_data.get('verify_ID') is not None:
            instance.verify_ID.save(validated_data.get('verify_ID').name, validated_data.get('verify_ID').file, save=False)
        instance.save()
        return instance


class UserAuthSerializer(serializers.Serializer):
    profile = UserSerializer(read_only=True)
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True)

    class Meta:
        exclude = []
        # model = User
        # extra_kwargs = {
        #     'wallet': {
        #         'read_only': True
        #     },
        #     'otp': {
        #         'read_only': True
        #     },
        #     'credit_score': {
        #         'read_only': True
        #     },
        #     'date_joined': {
        #         'read_only': True
        #     },
        #     'last_login': {
        #         'read_only': True
        #     },
        #     'password': {
        #         'write_only': True
        #     },
        #     'first_name': {
        #         'read_only': True
        #     },
        #     'last_name': {
        #         'read_only': True
        #     },
        #     'address': {
        #         'read_only': True
        #     },
        #     'nin': {
        #         'read_only': True
        #     },
        #     'bvn': {
        #         'read_only': True
        #     },
        #     'email': {
        #         'read_only': True
        #     },
        #     'verify_ID': {
        #         'read_only': True
        #     },
        #     'verify_ID_name': {
        #         'read_only': True
        #     },
        #     'is_agent': {
        #         'read_only': True
        #     },
        # }
        # exclude = ['user_permissions', 'groups',
        #            'is_admin', 'is_staff', 'is_active',
        #            'is_superuser']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        try:
            user = User.objects.get(phone_number=attrs['phone_number'])
            print(user.check_password(attrs['password']))
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({
                    'password': 'is incorrect'
                })
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'phone_number': 'user does not exist'
            })
        return attrs

    def create(self, validated_data):
        return self.user


    def to_representation(self, instance):
        return {
            'profile': UserSerializer(instance).data
        }


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        exclude = []


def generate_ref():
    # Generate a random string
    random_string = secrets.token_hex(16)
    # Convert the string to bytes
    message = random_string.encode('utf-8')
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the message
    md5_hash.update(message)
    # Get the hexadecimal representation of the hash
    return md5_hash.hexdigest()


class WalletDepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)
    status = serializers.CharField(read_only=True, default='success')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['amount'] < 0:
            raise serializers.ValidationError({
                'amount': 'is lower than 0'
            })
        return attrs

    def create(self, validated_data):
        # payload = {
        #     'amount': validated_data['validated_data'],
        #     'reference': f'{generate_ref()}',
        #     'notification_url': settings.BASE_URL + reverse('users:korapay_webhooks'),
        #     'currency': 'NGN',
        #     'customer': {
        #         "email": self.context['request'].user.email,
        #     },
        #     'merchant_bears_cost': False
        # }
        # headers = {
        #     'Authorization': f'Bearer {settings.KORAPAY_SECRET_KEY}'
        # }
        # url = settings.KORAPAY_CHARGE_API
        # response = requests.post(url=url, json=payload, headers=headers)
        # print(response.json())
        # rep = {}
        # if response.ok:
        #     if response.json()['status'] is True:
        #         rep['checkout_url'] = response.json()['data']['checkout_url']
        #         return rep
        self.context['request'].user.wallet += validated_data['amount']
        self.context['request'].user.save()
        TransactionHistory.objects.create(
            user=self.context['request'].user,
            title=TransactionHistoryChoices.DEPOSIT
        )
        return self.context['request'].user


class WalletTransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=10, write_only=True)
    phone_number = PhoneNumberField(write_only=True)

    def validate(self, attrs):
        attrs = super(WalletTransferSerializer, self).validate(attrs)
        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            if attrs['amount'] < 0:
                raise serializers.ValidationError({
                    'amount': 'is lesser than 0'
                })
            if self.context['request'].user.wallet < attrs['amount']:
                raise serializers.ValidationError({
                    'amount': ' is greater than your account balance'
                })
        else:
            raise serializers.ValidationError({
                'phone_number': 'phone_number does not exist'
            })
        return attrs

    def create(self, validated_data):
        receiving_user = User.objects.get(phone_number=validated_data['phone_number'])
        receiving_user.wallet += validated_data['amount']
        receiving_user.save()
        TransactionHistory.objects.create(
            user=receiving_user,
            agent=self.context['request'].user,
            title=TransactionHistoryChoices.DEPOSIT
        )
        TransactionHistory.objects.create(
            user=self.context['request'].user,
            title=TransactionHistoryChoices.TRANSFER
        )
        self.context['request'].user.wallet -= validated_data['amount']
        self.context['request'].user.save()
        return self.context['request'].user


class WalletWithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)
    status = serializers.CharField(read_only=True, default='success')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['amount'] < 0:
            raise serializers.ValidationError({
                'amount': 'is lower than 0'
            })
        return attrs

    def create(self, validated_data):
        self.context['request'].user.wallet -= validated_data['amount']
        self.context['request'].user.save()
        TransactionHistory.objects.create(
            user=self.context['request'].user,
            title=TransactionHistoryChoices.WITHDRAWAL
        )
        return self.context['request'].user
