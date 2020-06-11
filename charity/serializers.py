from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Institution, Donation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    imie = serializers.CharField(source='first_name')
    nazwisko = serializers.CharField(source='last_name')
    hasło = serializers.CharField(source='password')

    # username = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("url", "imie", "nazwisko", "email", "username", "hasło")
        extra_kwargs = {
            'hasło': {'write_ony': True},
            'username': {'read_only': True}
        }
        # write_only_fields = ('password',)
        # read_only_fields = ('username',)

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
        instance.first_name = validated_data.get('name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.last_name)
        instance.username = validated_data.get('email', instance.username)
        return instance


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
