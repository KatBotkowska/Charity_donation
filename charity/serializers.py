from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Institution, Donation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    imie = serializers.CharField(source='first_name')
    nazwisko = serializers.CharField(source='last_name')
    haslo = serializers.CharField(source='password', style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ("url", "imie", "nazwisko", "email", "username", "haslo")
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }

    def validate_password(self, value, user=None):
        errors = {}
        try:
            password_validation.validate_password(value, user=self.instance)
        except ValidationError as exc:
            errors['password'] = list(exc.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def to_representation(self, obj):
        # to hide hashed password in 'get' data
        rep = super(UserSerializer, self).to_representation(obj)
        rep.pop('haslo', None)
        return rep

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.last_name)
        instance.username = validated_data.get('email', instance.username)
        if 'password' in validated_data and validate_password(validated_data['password'], instance):
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class DonationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
