from rest_framework import serializers
from profiles.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False) 

    class Meta:
        model = User
        fields = [ 'id', 'role', 'username', 'password', 'phone_number', 'created', 'modified']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['created', 'modified']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_staff = validated_data.get('role').upper() == User.ADMIN

        if 'password' in validated_data:
            user.set_password(validated_data['password'])

        user.save()

        return user
