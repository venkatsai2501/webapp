from django import forms
from django.forms import modelformset_factory
from .models import Project,Tag,Review,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title', 'team_members', 'faculty_members', 'department', 
            'university', 'description', 'video', 'document','image','github_link','tags'
        ]
        faculty_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='faculty'),
        widget=forms.CheckboxSelectMultiple,
        required=False)

        team_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='student'),
        widget=forms.CheckboxSelectMultiple,
        required=False)
       
        tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),  # 1-5 star rating
        }
        