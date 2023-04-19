
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer, BookingSerializer, PaymentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .models import  CustomUser, UserProfile, Booking, Payment
from rest_framework import viewsets
from datetime import datetime, timedelta


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data from the serializer
        validated_data = serializer.validated_data

        # Add the is_staff field to the validated data
        is_staff = request.data.get('is_staff', False)
        validated_data['is_staff'] = is_staff

        # Save the user object with the added is_staff field
        self.perform_create(serializer)
        if is_staff:
            user_profile = UserProfile(user_id=serializer.data.get("id"),carmodel=request.data.get('carmodel', ''), license=request.data.get('license', ''), plugtype=request.data.get('plugtype', ''))
            user_profile.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            refresh.set_exp(lifetime=timedelta(minutes=300))
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return None


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        # Set the user for the booking as the currently authenticated user
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'status': 'success', 'message': 'Payment successful.'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


