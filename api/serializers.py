from rest_framework import serializers
from .models import CustomUser, UserProfile, Booking, Payment
from django.contrib.auth import authenticate





class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError('Email is required')
        if not password:
            raise serializers.ValidationError('Password is required')

        data['email'] = email
        data['password'] = password
        return data
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'profile_picture', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_picture': {'required': False}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            name=validated_data['name'],
            profile_picture=validated_data.get('profile_picture', None),
            is_staff = validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

       


class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Booking
        fields = ('booking_id', 'user', 'connector_type', 'poi_name', 'poi_url')

    

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('bookingId', 'cardNumber', 'cardHolder', 'expiryDate', 'cvc')
    
