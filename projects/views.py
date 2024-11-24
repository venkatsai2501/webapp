from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from .models import Project,Tag,Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm
from .forms import SignUpForm
from .models import Profile
from django.contrib.auth import login
from django.db.models.functions import ExtractYear
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save the role to the Profile model
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, role=role)
            login(request, user)
            return redirect('home')  # Redirect to a dashboard or homepage after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def landing_page(request):
    return render(request, 'landing.html')

def home(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'landing.html')

def contact(request):
    return render(request, 'landing.html')

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_view(request):
    return redirect('view_my_projects')  # Redirect to 'My Projects' by default

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .models import Tag, User  # Assuming Tag and User are imported


@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Associate project with logged-in user
            project.save()

            # Handle faculty members
            faculty_ids = request.POST.getlist('faculty_members')
            faculty_members = Profile.objects.filter(id__in=faculty_ids, role='faculty')
            project.faculty_members.set([faculty.user for faculty in faculty_members if faculty.user])

            # Handle team members
            team_member_ids = request.POST.getlist('team_members')
            team_members = Profile.objects.filter(id__in=team_member_ids, role='student')
            project.team_members.set([member.user for member in team_members if member.user])  # Avoid None users

            # Handle tags (add selected tags)
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                project.tags.add(tag)

            # Handle new tags (if any)
            new_tag_names = request.POST.getlist('new_tags')
            for tag_name in new_tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            return redirect('view_my_projects')  # Redirect to a success page
        else:
            # If the form is invalid, render the form with errors
            faculty_users = Profile.objects.filter(role='faculty')
            team_users = Profile.objects.filter(role='student')
            return render(request, 'create_project.html', {
                'form': form,
                'faculty_users': faculty_users,
                'team_users': team_users,
            })
    else:
        # Handle GET request
        form = ProjectForm()
        faculty_users = Profile.objects.filter(role='faculty')
        team_users = Profile.objects.filter(role='student')
        return render(request, 'create_project.html', {
            'form': form,
            'faculty_users': faculty_users,
            'team_users': team_users,
        })

    
@login_required
def view_my_projects_view(request):
    if request.user.profile.role == 'faculty':
        # If the logged-in user is a faculty member, fetch projects where the user is in faculty_members
        user_projects = Project.objects.filter(faculty_members=request.user)
    else:
        # If the logged-in user is a student, fetch their own projects
        user_projects = Project.objects.filter(user=request.user)

    return render(request, 'my_projects.html', {'projects': user_projects})


def view_all_projects_view(request):
    projects = Project.objects.all()

    # Handle tag filtering
    tag_id = request.GET.get('tag_id')
    if tag_id:
        projects = projects.filter(tags__id=tag_id)

    # Handle search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Handle department filtering
    department = request.GET.get('department', '')
    if department:
        projects = projects.filter(department=department)

    # Handle year filtering
    year = request.GET.get('year', '')
    if year.isdigit():
        projects = projects.filter(created_at__year=year)

    # Sorting functionality
    sort_by = request.GET.get('sort', 'title')
    projects = projects.order_by(sort_by)

    # Dropdown options for Department and Year
    departments = Project.objects.values_list('department', flat=True).distinct()
    years = (
        Project.objects.annotate(year=ExtractYear('created_at'))
        .values_list('year', flat=True)
        .distinct()
    )

    # Get all tags for dropdown
    tags = Tag.objects.all()

    context = {
        'projects': projects,
        'tags': tags,
        'departments': departments,
        'years': years,
        'search_query': search_query,
        'department': department,
        'year': year,
        'tag_id': tag_id,
        'sort_by': sort_by,
    }

    return render(request, 'all_projects.html', context)

@login_required
def my_projects(request):
    projects = Project.objects.filter(user=request.user)  # Assuming projects are associated with a user
    return render(request, 'my_projects.html', {'projects': projects})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)  # Ensure the user owns the project
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('view_my_projects')  # Redirect to the my_projects page after deletion
    
    return render(request, 'delete_project_confirm.html', {'project': project})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)  # Ensure the user owns the project

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('view_my_projects')  # Redirect to 'my_projects' page after editing
    else:
        form = ProjectForm(instance=project)  # Pre-fill the form with the current project data

    return render(request, 'edit_project.html', {'form': form, 'project': project})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    reviews = project.reviews.all()  # Get all reviews for this project

    # Count views for both authenticated and anonymous users
    viewed_projects = request.session.get('viewed_projects', [])

    if pk not in viewed_projects:
        project.views += 1
        project.save()
        viewed_projects.append(pk)
        request.session['viewed_projects'] = viewed_projects

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if user has already rated this project
            if not Review.objects.filter(project=project, user=request.user).exists():
                review = form.save(commit=False)
                review.project = project
                review.user = request.user
                review.save()
                return redirect('project_detail', pk=project.pk)
    else:
        form = ReviewForm()

    # Check if the user has already rated this project
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(project=project, user=request.user)
        except Review.DoesNotExist:
            user_review = None

    return render(request, 'project_detail.html', {
        'project': project,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })
