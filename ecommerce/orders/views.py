from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer

# 1. CartView: Manages retrieving the user's cart (GET) and adding items to it (POST)
# Look up: 'DRF APIView', 'get_or_create', 'IsAuthenticated'
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    # Retrieve (or create) the current logged-in user's cart
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    # Add a product to the cart. If already present, increment the quantity.
    def post(self, request):
        # get_or_create: Returns a tuple (object, created_boolean)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        # get_object_or_404: Returns 404 naturally if the product ID is missing or invalid
        product = get_object_or_404(Product, id=request.data.get('product'))
        
        # Read quantity from request payload, fallback to 1
        quantity = int(request.data.get('quantity', 1))

        # Check if this product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            # If item already exists in cart, increment quantity
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


# 2. CartItemView: Handles removing items from the cart (DELETE)
# Look up: 'Django Model Relationships', 'Django ForeignKey deletion'
class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    # Delete a specific CartItem row by its primary key ID (pk)
    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


# 3. PlaceOrderView: Checks out the cart, placing an order (POST)
# Look up: 'Database Snapshots', 'Transaction Loops'
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    # Converts all CartItems in the cart into a permanent Order
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Calculate order total price
        total = sum(item.product.price * item.quantity for item in cart_items)

        # 2. Create the parent Order record
        order = Order.objects.create(
            user=request.user,
            total=total,
            status='pending'
        )

        # 3. Create snapshot OrderItems.
        # Why snapshots? We store the name and price directly on the OrderItem table
        # instead of referencing the Product model directly. This prevents historical purchases
        # from changing values if the product price or description is updated later.
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=str(item.product.price),
                quantity=item.quantity
            )

        # 4. Empty the user's cart (deletes CartItem records, leaving Cart empty)
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# 4. OrderListView: Displays past checkout orders (GET)
# Look up: 'DRF ListAPIView', 'Django Queryset filtering'
class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    # Limit orders list to the current authenticated user only, sorted newest first
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
