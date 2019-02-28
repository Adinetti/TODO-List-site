from django.urls import path
from . import views

urlpatterns = [    
    path('logout', views.LogoutUser.as_view(), name="logout"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('tag/<slug:tag_slug>', views.Tag.as_view(), name="tag"),
    path('create_task', views.CreateTask.as_view(), name="createTask"),
    path('add_to_task/<slug:task_slug>', views.CreateTask.as_view(), name="addToTask"),
    path('task/<slug:task_slug>', views.TaskDetail.as_view(), name="task"),
    path('', views.Index.as_view(), name="index"),
]