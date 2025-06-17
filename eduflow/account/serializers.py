from rest_framework import serializers
from .models import CustomUser


class regserialiser(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','password']

    def create(self,validated_data):
        user=CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.role=2
        user.save()
        return user


class logserialiser(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','email','role','is_blocked']

    def update(self, instance, validated_data):
        if 'is_blocked' in validated_data:  
            instance.is_blocked = validated_data['is_blocked']
            instance.save()
        return instance

