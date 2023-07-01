from Accounts.models import User, Branch, Customer
from .models import MenuItem, Order, TransactionTable, Table
from billingApp1.serializers import RegisterSerializer, BranchSerializer, CustomerSerializer, MenuSerializer, TransitionSerializer, OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class JWTokenCreator(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['branch'] = user.branch.name

        # response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'token':token
        # }
        return token


class TokenCreator(TokenObtainPairView):
    serializer_class = JWTokenCreator
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


# Just for testing
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def Dasboard(request):
    if request.method == 'GET':
        data = f"{request.user}, this is a get request"
        return Response({'data':data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f"I've received {text}"
        return Response({'data':data}, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)



# Adding Branch

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def addBranch(request):
    if request.method == 'POST':
        branch = BranchSerializer(data=request.data)
        if branch.is_valid():
            branch.save()
        else:
            return Response(branch.error_messages, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'GET':
        branch = Branch.objects.all()
        serBranch = BranchSerializer(branch, many = True)
        return Response(serBranch.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)



#Adding User

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def addCustomer(request):
    if request.method == 'POST':
        customer = CustomerSerializer(data=request.data)
        if customer.is_valid():
            customer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(customer.data, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        customer = Customer.objects.all()
        serCutomer = CustomerSerializer(customer, many = True)
        return Response(serCutomer.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)



#Adding Menus (Items)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def addMenuItem(request):
    if request.method == 'POST':
        menu = MenuSerializer(data=request.data)
        if menu.is_valid():
            menu.save()
            return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        menu = MenuItem.objects.all()
        serMenu = MenuSerializer(menu, many = True)
        return Response(serMenu.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)




#Taking Orders
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def takeOrder(request):
    if request.method == 'POST':
        try:
            tableNumber = Table.objects.get(tableNumber = request.data.get('tableNumber'))
            menus = request.data.get('items')

            # creating order out of it.
            order = Order.objects.create(tabelNumber = tableNumber)
            # Iterate over each menu items and get that menu via it's id and multiple quantity and price.

            for items in menus:
                menu_id = items.get('menu_id')
                quantity = items.get('quantity')
                menuItem = MenuItem.objects.get(id = menu_id)
                print(type(items['quantity']), items['quantity'])
                subTotal = int(items['quantity']) * int(menuItem.price)


                TransactionTable.objects.create(
                    order = order,
                    item = menuItem,
                    quantity = quantity,
                    subTotal = subTotal
                )
            order.order_completed()
            return Response({'message': 'Order Placed successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error":e})
        
    elif request.method == 'GET':
        try:
            data = TransactionTable.objects.all()
            serData = TransitionSerializer(data, many=True)
            return Response(serData.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_204_NO_CONTENT)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)



#Getting and Updating specific order via Order ID

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def handle_order(request, id):
    if request.method == 'GET':
        try:
            transaction = TransactionTable.objects.filter(order = id)
            serTransaction = TransitionSerializer(transaction, many = True)
            order = Order.objects.get(id = id)
            serOrder = OrderSerializer(order, many = False)
            return Response({'Transaction':serTransaction.data, 'Order': serOrder.data })
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_204_NO_CONTENT)
        
    elif request.method == 'PATCH':
        try:
            order_obj = Order.objects.get(id = id)
            order = OrderSerializer(order_obj, data=request.data, partial = True)
            if order.is_valid():
                order.save()
                return Response({}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({}, status=status.HTTP_304_NOT_MODIFIED)
        except Exception as e:
            return Response({"Error":e})
    return Response(status=status.HTTP_400_BAD_REQUEST)


