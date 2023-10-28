from rest_framework import serializers
from users.models import *


class AdvertisedLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisedLoan
        exclude = []

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return instance


class LoanSerializer(serializers.ModelSerializer):
    advertised_loan = AdvertisedLoanSerializer(True)

    class Meta:
        model = Loan
        exclude = []

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            user=self.context['request'].user,
            advertised_loan=self.context['request'].advertised_loan,
            **validated_data
        )
        return instance


class LoanRepaymentSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)

    class Meta:
        model = LoanRepayment
        exclude = []