from django.urls import path
from . import views
from django.urls import path
from .views import profile
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import path



urlpatterns = [
   
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.course_index, name='index'),
    path('student_course/', views.student_course, name='student_course'),

    path('student_course/<int:enrollment_id>/grade_detail/', views.grade_detail, name='grade_detail'),
    path('courses/<int:course_id>/',views.course_detail, name='detail'),
    path('course/create',views.CourseCreate.as_view(), name='course_create'),
    # path('course/<int:pk>/update/', views.CourseUpdate.as_view(), name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete.as_view(), name='course_delete'),
    path('courses/<int:course_id>/add_student/', views.add_student, name='add_student'),

   path('courses/<int:enrollment_id>/add_grade/', views.add_grade, name='add_grade'),
   path('update_grade/<int:enrollment_id>/', views.update_grade, name='update_grade'),
    path('courses/<int:course_id>/student_list/',views.student_list, name='student_list'),

    # path('courses/<int:course_id>/student_list/<int:enrollment_id>/add_grade/',views.add_grade, name='add_grade'),


    
   
    path('accounts/signup',views.signup,name='signup'),
    path('accounts/profile/', profile, name='profile'),
    path('profile/<int:pk>/update/', views.update_profile.as_view(), name='update_profile'),

   
 

]  
     