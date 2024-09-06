from rest_framework import serializers 
from .models import Product, Review, Order, ShippingAddress, OrderItems
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class ReviewSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Review
        fields = "__all__"
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Product
        fields = "__all__"
        
    def get_reviews(self , obj) : 
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data
    reviews = serializers.SerializerMethodField(read_only = True)


class ShippingAddressSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShippingAddress 
            fields = "__all__"

class OrderItemsSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = OrderItems
        fields = ["product", "quantity", "price"]

class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=False)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "isAdmin", "password", "token"]

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_isAdmin(self, obj):
        return obj.is_staff

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()

        return instance
 
class OrderSerializer(serializers.ModelSerializer): 
    user_data = serializers.SerializerMethodField(read_only = True)
    
    def get_user_data(self, obj) :  
        user = obj.user 
        if user : 
            serializer = UserSerializer(user)
            return serializer.data 
        
        else : 
            return {}
         
    order_items = serializers.SerializerMethodField(read_only = True)
    
    def get_order_items(self, obj): 
        order_items = obj.order_items.all()
        serializer  = OrderItemsSerializer(order_items, many = True)
        return serializer.data
    
    shipping_address = serializers.SerializerMethodField(read_only = True)
    
    def get_shipping_address(self, obj): 
        if hasattr(obj,"shipping_address" ):
            address = obj.shipping_address 
        else : 
            return {}
 
        serializer = ShippingAddressSerializer(address)
        return serializer.data
        
    class Meta : 
        model = Order 
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

