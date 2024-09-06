from django.urls import path 
from . import views 

urlpatterns = [
    path("register/", views.register_user, name="register_new_user"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile_view, name="get_update_user_profile"),
    path("users/", views.getUsers, name="get_all_users"),
    path("delete_user/<int:pk>/", views.deleteUser, name="delete_user"),
    path("get_user/<int:pk>/", views.getUserById, name="get_user"),
    path("admin_update_user/<int:pk>/", views.updateUser, name="update_user_by_admin"),
    path("products/", views.get_products, name="get_products"),
    path("product/<int:pk>/", views.get_product, name="get_product_by_id"),
    path("delete_product/<int:pk>/", views.deleteProduct, name="delete_product"),
    path("create/", views.create_product, name="create_product"),
    path("update_product/<int:pk>/", views.updateProduct, name="update_product"),
    path("upload_image/<int:pk>/", views.uploadImage, name="upload_image"),
    path("create_review/<int:pk>/", views.create_review, name="create_product_review"),
    path("add_order_items/", views.add_order_items, name="add_order_items"),
    path("order/<int:pk>/", views.get_order_by_id, name="get_order_by_id"),
    path("update_order_topaid/<int:pk>/", views.update_order_to_paid, name="update_order_to_be_paid"),
    path("update_order_todelivered/<int:pk>/", views.update_order_to_delivered, name="update_order_to_be_delivered"),
    path("my_orders/", views.get_my_orders, name="get_my_orders"),
    path("orders/", views.get_all_orders, name="get_all_orders")
]
