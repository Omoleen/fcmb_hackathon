from rest_framework import serializers
from .models import *
from phonenumber_field.serializerfields import PhoneNumberField


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=512, read_only=True)
    refresh = serializers.CharField(max_length=512,  read_only=True)

    class Meta:
        exclude = []


class BeneficiaryContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryContact
        exclude = []

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
        self.Meta.model.objects.create_user(**validated_data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.Meta.model.objects.filter(email=attrs['attrs']).exists():
            raise serializers.ValidationError({
                'email': 'email already exists'
            })
        raise attrs

    def update(self, instance: User, validated_data):
        instance.location_lat = validated_data.get('location_lat', instance.location_lat)
        instance.location_long = validated_data.get('location_long', instance.location_long)
        instance.address = validated_data.get('address', instance.address)
        instance.verify_ID_name = validated_data.get('verify_ID_name', instance.verify_ID_name)
        instance.is_agent = validated_data.get('is_agent', instance.is_agent)
        if validated_data.get('verify_ID').file is not None:
            instance.verify_ID.save(validated_data.get('verify_ID').name, validated_data.get('verify_ID').file, save=False)
        instance.save()
        return instance


class UserAuthSerializer(serializers.ModelSerializer):
    tokens = TokenSerializer(read_only=True)

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
            'first_name': {
                'read_only': True
            },
            'last_name': {
                'read_only': True
            },
            'address': {
                'read_only': True
            },
            'nin': {
                'read_only': True
            },
            'bvn': {
                'read_only': True
            },
            'email': {
                'read_only': True
            },
            'verify_ID': {
                'read_only': True
            },
            'verify_ID_name': {
                'read_only': True
            },
            'is_agent': {
                'read_only': True
            },
        }
        exclude = ['user_permissions', 'groups',
                   'is_admin', 'is_staff', 'is_active',
                   'is_superuser']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.Meta.model.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': 'user does not exist'
            })
        raise attrs

    def create(self, validated_data):
        user = self.Meta.model.objects.get(email=validated_data['email'])
        if user.check_password(validated_data['password']):
            return user
        raise({
            'password': 'is incorrect'
        })


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        exclude = []


class WalletTransferSerializer(serializers.Serializer):
    pass

class WalletDepositSerializer(serializers.Serializer):
    pass

class WalletWithdrawalSerializer(serializers.Serializer):
    pass
