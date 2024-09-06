from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Order, ShippingAddress, OrderItems
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer, UserSerializer, RegisterSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import traceback

# Create your views here.

#USER FUNCTIONALITIES
@api_view(['POST'])
def register_user(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'user_id': user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email
            }
            print("Registration Success:", response_data)
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("Error occurred:", str(e))
        traceback.print_exc() 
        return Response({"detail": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def login(request):
    data = request.data
    user = authenticate(request, username=data['email'], password=data['password'])
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response({"error": "Profile does not exist for the current user"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'detail': 'User deleted'}, status=status.HTTP_200_OK)
    except:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        
        data = request.data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.is_staff = data.get('isAdmin', user.is_staff)
        
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#PRODUCT FUNCTIONALITIES
@api_view(["GET"])
def get_products(request) : 
    try : 
        products = Product.objects.all()  
        serializer = ProductSerializer(products , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    except : 
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"]) 
def get_product(request , pk) : 
    try : 
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data  , status=200)
    except Product.DoesNotExist : 
        return Response(status=404)
    except : 
        return Response(status=400)
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response({'detail': 'Product deleted'}, status=status.HTTP_200_OK)
    
    except Product.DoesNotExist : 
        return Response(status=404)
    except : 
        return Response(status=400)
    
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request) : 
    user = request.user 
    data = request.data 
    data["user"] = user.id

    data.setdefault("name", "Default Name")
    data.setdefault("price", 0.0)
    data.setdefault("brand", "Default Brand")
    data.setdefault("countInStock", 0)
    data.setdefault("description", "Default Description")
    data.setdefault("category", "Default Category") 
    try : 
        serializer =  ProductSerializer(data = data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors , status=400)
    except Exception as ex :
        return Response({"details" : f"error happen {str(ex)}"} , status=400) 
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(instance=product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request, pk):
    product = Product.objects.get(id=pk)
    product.image = request.FILES.get('image')
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    data = request.data
    data["product"] = pk
    data["user"] = request.user.id
    
    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        
        product = Product.objects.get(pk=pk)
        product.num_reviews += 1
        product.save() 
        
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)

#ORDER FUNCTIONALITIES
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    
    order_items_data = data.get('order_items')
    if not order_items_data:
        return Response({"error": "No order items provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    total_price = 0
    order_items_list = []

    for item in order_items_data:
        try:
            product = Product.objects.get(id=item['product'])
        except Product.DoesNotExist:
            return Response({"error": f"Product with ID {item['product']} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        item_price = product.price * item['quantity']
        total_price += item_price
        
        order_items_list.append({
            'product': product.id,
            'quantity': item['quantity'],
            'price': product.price
        })

    order_data = {
        'user': user.id,
        'payment_method': data.get('payment_method'),
        'tax_price': data.get('tax_price'),
        'shipping_price': data.get('shipping_price'),
        'total_price': total_price,
    }
    
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()
        
        shipping_address_data = data.get('shipping_address')
        if shipping_address_data:
            ShippingAddress.objects.create(
                order=order,
                **shipping_address_data
            )
        
        for item_data in order_items_list:
            OrderItems.objects.create(
                order=order,
                product=Product.objects.get(id=item_data['product']),
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            product = Product.objects.get(id=item_data['product'])
            product.count_in_stock -= item_data['quantity']
            product.save()
        
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if order.user != request.user and not request.user.is_staff:
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.is_paid = True
        order.paid_at = timezone.now()
        order.save()
        return Response({"message": "Order updated to paid."}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_to_delivered(request, pk):
    try:
        order = Order.objects.get(id=pk)
        order.is_delivered = True
        order.delivered_at = timezone.now()
        order.save()
        return Response({"message": "Order updated to delivered."}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)