from rest_framework import serializers

from users.models import CustomUser, Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
        read_only_fields = [
            "user",
            "payment_date",
            "session_id",
            "payment_amount",
            "link",
        ]


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
