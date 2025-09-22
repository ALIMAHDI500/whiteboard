from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=20, choices=[('Teacher', 'Teacher'), ('Student', 'Student')], default='Student')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize avatar image if it's too large
        # if self.avatar:
        #     img = (self.avatar.path)
        #     if img.height > 300 or img.width > 300:
        #         output_size = (300, 300)
        #         img.thumbnail(output_size)
        #         img.save(self.avatar.path)


class Course(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  course_name = models.CharField(max_length=250)
  user_name = models.CharField()
  course_code = models.CharField()
  image = models.ImageField(default='', upload_to='course_images')


  def __str__(self):
     return f" {self.user} - {self.course_name} - {self.course_code} -{self.user_name} "
  
  def get_absolute_url(self):
     return reverse('detail', kwargs={'course_id': self.id})
  
                
class Enrollment(models.Model):
     student= models.ForeignKey(User,on_delete=models.CASCADE)
     course= models.ForeignKey(Course, on_delete=models.CASCADE) 


     def __str__(self):
       return f" {self.student} - {self.course}  "
  
     def get_absolute_url(self):
         return reverse('detail', kwargs={'course': self.id})
  

class Grade(models.Model):
    enrollment=models.ForeignKey(Enrollment,on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')
    date = models.DateField(auto_now_add=True)
    

    midterm = models.FloatField(default=0)
    quizzes = models.FloatField(default=0)
    assignments = models.FloatField(default=0)
    project = models.FloatField(default=0)
    final_exam = models.FloatField(default=0)


    # def __str__(self):
    #    return f" {self.enrollment} - {self.score}  "
  
    # def get_absolute_url(self):
    #      return reverse('student_list', kwargs={'enrollment': self.id})
  
    def total_score(self):
        return self.midterm + self.quizzes + self.assignments + self.project + self.final_exam
    
    def __str__(self):
        return f"{self.enrollment} - {self.date}"