from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('accounts/profile/', profile_view, name='profile'),  # Add profile page URL
    path('create-project/', create_project_view, name='create_project'),
    path('my-projects/', view_my_projects_view, name='view_my_projects'),
    path('all-projects/', view_all_projects_view, name='view_all_projects'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('delete-project/<int:project_id>/', delete_project, name='delete_project'),
    path('edit-project/<int:project_id>/', edit_project, name='edit_project'),
    path('project/<int:pk>/', project_detail, name='project_detail'),
]
