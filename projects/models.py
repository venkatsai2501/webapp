from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
    )
    
    title = models.CharField(max_length=200)
    team_members =  models.ManyToManyField(User, related_name='team_members', blank=True)
    faculty_members = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Add status field
    department = models.CharField(max_length=100)
    university = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    # Add multiple ImageFields to the Project model
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)  # Add this line
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # To associate project with the user
    github_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)  # New field for counting views


    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0

class Review(models.Model):
    project = models.ForeignKey(Project, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']  # Ensure a user can review a project only once

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.rating} stars)"