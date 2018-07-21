from django.urls import path
from . import views

urlpatterns = \
    [
        path('landing/', views.Landing.as_view(), name="Landing"),
        path('home/', views.home, name="home"),
        path('home/<int:class_id>/', views.home_in_context, name="homecontext"),
        path('resources/<int:class_id>/', views.parallel_home, name="parallel"),
        path('UserInfo/', views.def_user, name="user"),
        path('post/newpost/<int:class_id>/', views.PostCreateView.as_view(), name="create_post"),
        path('post/delete/<int:post_id>/', views.delete_post, name="delete"),
        path('resource/delete/<slug:slug>', views.delete_resource, name="delete_resource"),
        path('class/new/', views.ClassCreateView.as_view(), name="new_class"),
        path('class/users/<int:class_id>/', views.class_list, name="filesList"),
        path('files/newfile/<int:class_id>/<int:ass_id>/', views.ResourceCreateView.as_view(), name="new_file"),
        path('class/class_enrolled/', views.class_list, name="class_list"),
        path('class/enrollclass/', views.ClassEnrollView.as_view(), name="enroll"),
        path('allclasses/', views.all_classes, name="all_classes"),
        path('classes/middle/', views.middle, name='middle'),
        path('class/delete/<int:class_id>', views.delete_class, name='delete_class'),
        path('about/<int:class_id>/', views.class_details, name='pr'),
        path('home/<int:class_id>/body/<int:view_id>/', views.home_body, name='body'),
        path('assignment/handin/<int:assignment_id>/', views.AssignmentHandIn.as_view(), name='hand_in'),
        path('assignment/CreateAssignment/<int:class_id>/', views.AssignmentCreateView.as_view(), name='new_assignment')
    ]


