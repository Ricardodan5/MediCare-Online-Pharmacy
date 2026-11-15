from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="customers/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("prescriptions/", views.prescriptions, name="prescriptions"),
    path("prescriptions/list/", views.prescription_list, name="prescription_list"),
    path(
        "prescriptions/<int:prescription_id>/review/",
        views.review_prescription,
        name="review_prescription",
    ),
    path("prescriptions/<int:pk>/file/", views.view_prescription_file, name="view_prescription_file"),
    path("orders/place/", views.place_order, name="place_order"),
    path("orders/", views.my_orders, name="my_orders"),
    path("orders/<int:order_id>/", views.track_order, name="track_order"),
    path("orders/<int:order_id>/update/", views.update_order_status, name="update_order_status"),
    path("availability/", include("availability.urls")),
]
