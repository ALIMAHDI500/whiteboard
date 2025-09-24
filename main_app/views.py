from django.shortcuts import get_object_or_404, render


from django.shortcuts import render, redirect
from .models import User, Profile,Course,Grade,Enrollment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import  DeleteView

from .forms import RegisterForm ,NewcourseForm,Add_Enrollment_Student,GradeForm
from django.db import IntegrityError, models 
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# @login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html')

class ProfileCreate(CreateView):
  model = Profile
  fields = [ 'phone', 'bio', 'avatar','role']
 
  def form_valid(self, form):
       form
       form.instance.user=self.request.user
       return super().form_valid(form)
  
class update_profile(UpdateView):
    model = Profile
    fields = ['phone', 'bio', 'avatar']
    template_name = 'users/update_profile.html'  
    success_url = reverse_lazy('profile')
    
    def get_object(self):
       
        return get_object_or_404(Profile, user=self.request.user)
    
    def form_valid(self, form):
      
        user = self.request.user
        user.first_name = self.request.POST.get('first_name', user.first_name)
        user.last_name = self.request.POST.get('last_name', user.last_name)
        user.email = self.request.POST.get('email', user.email)
        user.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
  
def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')

def course_index(request):
  courses = Course.objects.filter(user=request.user)

  return render(request, 'course/index.html',{'courses':courses,} )


def student_course(request):
  user_id = request.user.id 

  user=request.user
  courses = Course.objects.filter(
     enrollment__student__id=user_id,
     enrollment__student__profile__role='Student'  
  ).distinct()
  
  enrollments = Enrollment.objects.filter(
        student=user,
        student__profile__role='Student'
    ).select_related('course')

  if not enrollments.exists():
       
        return render(request, 'main_app/student_course.html', {
            'message': 'No courses enrolled yet'
        })  

  context = {'courses': courses,'enrollments':enrollments}
  return render(request, 'main_app/student_course.html', context )



class CourseCreate(CreateView):
  model=Course
  fields=['course_name','course_code']
  def form_valid(self, form):
       form
       form.instance.user=self.request.user
       return super().form_valid(form)

class course_delete(DeleteView):
    model=Course
    success_url='/courses/'

class CourseUpdate(UpdateView):
    model = Course
    fields=['course_name','course_code']
    template_name = 'main_app/course_form.html'  
    success_url = reverse_lazy('index')
       
def add_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = Add_Enrollment_Student(request.POST)
        if form.is_valid():
          
            user = form.cleaned_data['user']
            if not Enrollment.objects.filter(student=user, course=course).exists():
                enrollment = form.save(commit=False)
                enrollment.course = course
                enrollment.save()
            return redirect('detail', course_id=course_id)
    else:
        form = Add_Enrollment_Student()
    
    return render(request, 'main_app/student_form.html', {
        'form': form,
        'course': course,
    })


class delete_student_enrollment (DeleteView):
 model=Enrollment
 success_url = reverse_lazy('index')  
   
     
def student_list(request,course_id):
 course = get_object_or_404(Course, id=course_id)
 students = User.objects.filter(enrollment__course=course).distinct()   
 enrollments = Enrollment.objects.filter(course=course).select_related('student')

 for enrollment in enrollments:
    try:
           Grade.objects.get(enrollment=enrollment)
           enrollment.has_grade = True
    except Grade.DoesNotExist:
           enrollment.has_grade = False
    
 if request.method == 'POST':     
   return redirect('detail', course_id=course_id)
 
    
 return render(request, 'main_app/student_list.html', {
       
        'course': course,
        'students':students,
        'enrollments': enrollments,
        
    })


def add_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id) 

    try:
      grade = Grade.objects.get(enrollment=enrollment)
    except Grade.DoesNotExist:
      grade = None
     
    if request.method == 'POST':
     
        form = GradeForm(request.POST)
        if form.is_valid():
            grade.status='complated'
            new_grade = form.save(commit=False)
            new_grade.enrollment = enrollment
            
            new_grade.save()
            
          
    else:
        form = GradeForm()  
       
    return render(request, 'main_app/grade_detail.html', {
        'form': form,
        'enrollment': enrollment,
        'grade':grade  
    })

def update_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    grade, created = Grade.objects.get_or_create(
        enrollment=enrollment,
        defaults={'status': 'pending'}
    )
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            grade.status='complated'
            form.save()
          
            return redirect('grade_detail', enrollment_id=enrollment.id)
    else:
        form = GradeForm(instance=grade)
    
    return render(request, 'main_app/update_grade.html', {
        'form': form, 
        'enrollment': enrollment,
        'grade': grade
    })


def course_detail(request, course_id):
  
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course)
    students = User.objects.filter(enrollment__course=course).distinct()
    
    return render(request, 'course/detail.html', {
        'course': course,
        'enrollments': enrollments,
        'students': students,
    })



def grade_detail(request,enrollment_id):
    

  enrollment = get_object_or_404(Enrollment, id=enrollment_id)
  
  grade = Grade.objects.filter(enrollment=enrollment).first()

  context = {'enrollment': enrollment,'grade':grade}
  
  return render(request, 'main_app/grade_detail.html',context,)


def signup(request):
    if request.method == 'POST':
     
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
           
            role = form.cleaned_data.get('role', 'Student')
            Profile.objects.create(
                user=user, 
                role=role,
                bio='',
                phone=''
            )
            
           
            login(request, user)
            return redirect('home') 
        else:
            error_message = 'Invalid signup - Please try again'
    else:
        form = RegisterForm 
        error_message = ''
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)