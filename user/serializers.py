from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'phone_number', 'verification_code', 'is_verified')
        read_only_fields = ('id', 'verification_code', 'is_verified')


class RegistrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('birth_date',)

    def update(self, instance, validated_data):

        instance.birth_date = validated_data.get('birth_date', instance.birth_date)

        instance.save()

        return instance


