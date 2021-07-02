"""ProjektKoncowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from carblog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.landing_page, name='home'),
    path('', views.start_page, name='start'),
    path('cars/', views.cars, name='cars'),
    path('car_detail/<car_id>', views.car_detail, name='car_detail'),

    path('rate/<car_id>', views.rate, name='rate'),
    path('add_car/', views.add_car, name='add_car'),
    path('add_post/', views.add_post, name='add_post'),

    path('my_posts/', views.my_posts, name='my_posts'),
    path('edit/<post_id>', views.edit_post, name='edit'),
    path('delete/<post_id>', views.delete, name='delete'),

    path('like/<post_id>/', views.like, name='like_post'),
    path('comment/<post_id>/', views.comment, name='add_comment'),

    path('post/<post_id>', views.post, name='post'),

    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
]
