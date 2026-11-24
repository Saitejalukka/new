
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'phone_number'
        ]

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop('password2')

        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]
