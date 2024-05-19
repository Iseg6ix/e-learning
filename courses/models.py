from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

# Custom User model to handle different roles and additional details
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=225, null=False)
    last_name = models.CharField(max_length=225, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    date_of_birth = models.DateField(null=False)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    intended = models.TextField() 

    def __str__(self):
        return self.user.username
    
class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=False, default='Display_pics/name_of_pics.jpg')

    def __str__(self):
        return self.user.username

# Course model
class Course(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='Display_pics/', null=False, default='Display_pics/name_of_pics.jpg')
    created_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='courses_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Module model for breaking down courses into modules
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    resources = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=False)
    order = models.IntegerField()

    def __str__(self):
        return self.title


#for the module videos 
class Videos(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    videos = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov'])], null=False)
    order = models.IntegerField()

    def __str__(self):
        return self.title 
    
# Lesson model within modules
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return self.title   

# Enrollment model to track which users are enrolled in which courses
class Enrollment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'

# Quiz model
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# Question model within quizzes
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return self.text

# Choice model for multiple choice questions
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# QuizResult model to store the results of quizzes taken by users
class QuizResult(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} scored {self.score} in {self.quiz.title}'

# Model to track likes on courses
class CourseLike(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='liked_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.course.title}'

# Model to handle the wishlist functionality
class Wishlist(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} added {self.course.title} to wishlist'
