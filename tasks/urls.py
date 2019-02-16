from django.urls import path
from . import views

urlpatterns = [
    path('', views.wellcome, name="wellcome"),
    path('logout', views.logout_user, name="logout"),
    path('login', views.login_user, name="login"),
    path('<str:username>', views.index, name="index") 
]