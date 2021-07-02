from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
import json
from carblog.forms import CreateUserForm, CreatePostForm, RateCarsForm, AddCarForm, CreateComment
from .models import Post, Cars, Rating
from django.db.models import Avg


def landing_page(request):
    posty = Post.objects.all()
    context = {'posty': posty}
    return render(request, 'index.html', context)


def start_page(request):
    return render(request, 'start.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Stworzono użytkownika dla: ' + user)
                return redirect('/login/')

        context = {'form': form}
        return render(request, 'register.html', context)


def log_in(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                messages.info(request, 'Email or password is incorrect')

        return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('/home/')


def rate(request, car_id):
    if request.user.is_authenticated:
        car = Cars.objects.get(pk=car_id)
        form = RateCarsForm()
        if request.method == 'POST':
            form = RateCarsForm(request.POST)
            if form.is_valid():
                car_prepare = form.save(commit=False)
                car_prepare.user = request.user
                car_prepare.car = Cars.objects.get(pk=car_id)
                car_prepare.save()
                messages.success(request, 'Oddano głos')
                link = '/car_detail/' + car_id
                return redirect(link)

        context = {'form': form, 'car': car}
        return render(request, 'rate.html', context)
    else:
        return redirect('/login/')


def add_car(request):
    if request.user.is_authenticated:
        form = AddCarForm()
        if request.method == 'POST':
            form = AddCarForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Dodano samochód')
                return redirect('/cars/')

        context = {'form': form}
        return render(request, 'add_car.html', context)
    else:
        return redirect('/login/')


def add_post(request):
    if request.user.is_authenticated:
        form = CreatePostForm()
        if request.method == 'POST':
            form = CreatePostForm(request.POST)
            if form.is_valid():
                post_prepare = form.save(commit=False)
                post_prepare.user = request.user
                post_prepare.save()
                messages.success(request, 'Utworzono posta')
                return redirect('/home/')

        context = {'form':form}
        return render(request, 'add_post.html', context)
    else:
        return redirect('/login/')


def cars(request):
    cars2 = Cars.objects.all()
    context = {'cars2': cars2}
    return render(request, 'cars.html', context)


def car_detail(request, car_id):
    car = Cars.objects.get(pk=car_id)
    look = Rating.objects.all().aggregate(lookavg=Avg('look'))
    price = Rating.objects.all().aggregate(priceavg=Avg('price'))
    reliability = Rating.objects.all().aggregate(reliabilityavg=Avg('reliability'))
    practicality = Rating.objects.all().aggregate(practicalityavg=Avg('practicality'))
    family_car = Rating.objects.all().aggregate(family_caravg=Avg('family_car'))
    context = {
        'car': car,
        'look': look['lookavg'],
        'price': price['priceavg'],
        'reliability': reliability['reliabilityavg'],
        'practicality': practicality['practicalityavg'],
        'family_car': family_car['family_caravg']}
    return render(request, 'car_detail.html', context)


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    stuff = get_object_or_404(Post, id=post_id)
    total_likes = stuff.total_likes()
    context = {'post': post, 'total_likes': total_likes}
    return render(request, 'post.html', context)


def my_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user)
        context = {'posts': posts}
        return render(request, 'my_posts.html', context)

    return redirect('/login/')


def edit_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            form = CreatePostForm(instance=post)
            context = {'form': form, 'post': post}
            if request.method == 'POST':
                form = CreatePostForm(request.POST, instance=post)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Edytowano post')
                    return HttpResponse('Edytowano')
            return render(request, 'edit_post.html', context)
        else:
            return redirect('/my_posts/')
    return redirect('/login/')


def delete(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            post.delete()
            messages.success(request, 'Usunięto post')
            return redirect('/my_posts/')
        else:
            return redirect('/my_posts/')
    return redirect('/login/')


def like(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post', args=[str(post_id)]))
    return redirect('/login/')


def comment(request, post_id):
    if request.user.is_authenticated:
        form = CreateComment()
        if request.method == 'POST':
            form = CreateComment(request.POST)
            if form.is_valid():
                post_prepare = form.save(commit=False)
                post_prepare.user = request.user
                post_prepare.post = Post.objects.get(pk=post_id)
                post_prepare.save()
                messages.success(request, 'Utworzono komentarz')
                link = '/post/'+post_id
                return redirect(link)

        context = {'form': form}
        return render(request, 'add_comment.html', context)
    else:
        return redirect('/login/')
