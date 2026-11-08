from django.urls import path, include

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path(        "register/",

        views.register,
        name="register"
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="customers/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

   path(
    "prescriptions/", views.prescriptions, name="prescriptions"
),

path('prescriptions/list/', views.prescription_list, name='prescription_list'),

path('prescriptions/<int:prescription_id>/review/', views.review_prescription, name='review_prescription'),
path('inventory/', include('inventory.urls')),

path('availability/', include('availability.urls')),
]
    path(
        "prescriptions/",
        views.prescriptions,
        name="prescriptions"
    ),

    path(
        "prescriptions/<int:pk>/file/",
        views.view_prescription_file,
        name="view_prescription_file"
    ),
]
