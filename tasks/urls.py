from django.urls import path
from . import views

urlpatterns = [    
    path('logout', views.LogoutUser.as_view(), name="logout"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('tag/<slug:tag_slug>', views.TagIndex.as_view(), name="tag"),
    path('done_task', views.DoneTask.as_view(), name="doneTask"),
    path('create_task', views.CreateTask.as_view(), name="createTask"),
    path('create_tag', views.CreateTag.as_view(), name="createTag"),
    path('add_to_task/<slug:task_slug>', views.CreateTask.as_view(), name="addToTask"),
    path('edit_task/<slug:task_slug>', views.EditTask.as_view(), name="addToTask"),
    path('task/<slug:task_slug>', views.TaskDetail.as_view(), name="task"),
    path('', views.Index.as_view(), name="index"),
]