from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('dashboard/', views.home, name="home"),
    path('logout/', views.logout_user, name="logout_user"),
    path('register/', views.register_page, name="register_page"),

    path('submit_a_day/<str:pk>/', views.add_steps, name="add_steps"),
]
