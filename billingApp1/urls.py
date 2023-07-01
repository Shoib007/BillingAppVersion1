from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import TokenCreator, RegisterView, Dasboard, addBranch, addCustomer, addMenuItem, takeOrder, handle_order
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Dasboard, name="user_info"),
    path('token/', TokenCreator.as_view(), name='token_creator'),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('register/',RegisterView.as_view(), name="register_user"),
    path('branch/', addBranch, name='addBranch'),
    path('customer/', addCustomer, name="addCustomer"),
    path('menu', addMenuItem, name="addMenuItem"),
    path('order/',takeOrder, name='take_Order' ),
    path('order/<int:id>/', handle_order, name="order_Details"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)