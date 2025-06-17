from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import regserialiser,logserialiser
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .models import CustomUser

# user registraion

class register(APIView):
    def post(self,request):
        k=request.data
        ser=regserialiser(data=k)
        if ser.is_valid():
            ser.save()
            return Response({"message":"User created"},status=status.HTTP_201_CREATED)
        return Response(ser.errors)

# user login

class logg(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        print("im login view=============")
        k=request.data
        ser=logserialiser(data=k)
        if not ser.is_valid():
            return Response(ser.errors)
        user=authenticate(
            email=ser.validated_data['email'],
            password=ser.validated_data['password']
        )
        
        if user is None:
            return Response("user not exist")
        if user.is_blocked:                                              
            return Response("Your account has been blocked by the admin.")       
        refresh = RefreshToken.for_user(user)
        USER=CustomUser.objects.get(email=user)
        print("user==",USER.is_admin)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'role':user.role,
            'admin':user.is_admin,
        }, status=200)
    



