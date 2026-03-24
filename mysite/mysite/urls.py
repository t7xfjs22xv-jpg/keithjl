from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('blog/', views.blog_view, name='blog_view'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('about/', views.about_author, name='about_author'),
]