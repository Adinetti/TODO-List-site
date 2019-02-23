from django.urls import path
from . import views

urlpatterns = [    
    path('logout', views.LogoutUser.as_view(), name="logout"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('tag/<slug:tag_slug>', views.Tag.as_view(), name="tag"),
    path('', views.Index.as_view(), name="index"),
]