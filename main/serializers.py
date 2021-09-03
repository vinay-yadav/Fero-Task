from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserDocuments

User = get_user_model()


def create_document(user, doc_type, document):
    UserDocuments.objects.create(
        user=user,
        doc_type=doc_type,
        document=document
    )


class UserRegisterSerializer(serializers.ModelSerializer):
    pan = serializers.FileField(required=False, allow_null=True, write_only=True)
    aadhar = serializers.FileField(required=False, allow_null=True, write_only=True)
    others = serializers.FileField(required=False, allow_null=True, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            'pan',
            'aadhar',
            'others'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        password = data.get('password', None)
        password2 = data.pop('password2', None)

        if password2 != password:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )

        user_obj.set_password(validated_data.get('password'))
        user_obj.save()

        if validated_data.get('pan', None):
            create_document(user_obj, 'pan', validated_data.get('pan'))

        if validated_data.get('aadhar', None):
            create_document(user_obj, 'aadhar', validated_data.get('aadhar'))

        if validated_data.get('others', None):
            create_document(user_obj, 'others', validated_data.get('others'))

        return user_obj
