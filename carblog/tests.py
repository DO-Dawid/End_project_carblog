from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Cars, Comment, Rating
import json
import re
from django.contrib import auth
from django.http import request

# Create your tests here.


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('alamakota')
        self.user.save()

    def test_user_create_POST(self):
        response = self.client.post(reverse('register'), {'first_name': 'slawek', 'username': 'cooklee@wp.pl',
                                                          'password1': 'alamakota','password2': 'alamakota',
                                                          'last_name': 'bo'})
        user = User.objects.get(username='cooklee@wp.pl')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, 'slawek')
        self.assertEqual(user.last_name, 'bo')

    def test_post_create_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_post'), {'name': 'Testowy1', 'mark': 'mb',
                                                          'short_text': 'testowy krótki tekst',
                                                          'text': 'testowy text', 'post_type':'og'})
        # # posts = Post.objects.create(name= 'Testowy1', mark= 'mb',
        # #                             short_text= 'testowy krótki tekst',
        #                             text= 'testowy text')
        # posts.save()
        post = Post.objects.get(name='Testowy1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.name, 'Testowy1')
        self.assertEqual(post.text, 'testowy text')
        self.assertEqual(post.mark, 'mb')

    def test_edit_post_POST(self):
        self.client.force_login(self.user)
        post = Post.objects.create(name='testowy2', mark='mb', text='testowytext',
                                         post_type='og', short_text='testowy', user=self.user)
        id = post.id
        response = self.client.post(reverse('edit', args=(id,)), {'name': 'testowy3', 'mark': 'mb',
                                                               'text': 'testowytexttestowy',
                                                               'post_type': 'og', 'short_text': 'testowy2'})
        edited_post = Post.objects.get(name='testowy3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(edited_post.name, 'testowy3')
        self.assertEqual(edited_post.text, 'testowytexttestowy')

        self.assertEqual(edited_post.post_type, 'og')
        self.assertEqual(edited_post.short_text, 'testowy2')

    def test_delete_post(self):
        self.client.force_login(self.user)
        post = Post.objects.create(name='testowy2', mark='mb', text='testowytext', date='2021-3-3',
                                   datetime='2012-09-04 06:00', post_type='og', short_text='testowy')
        id = post.id
        response = self.client.get(reverse('delete', args=(id,)))
        self.assertEqual(response.status_code, 302)
        try:
            Post.objects.get(pk=id)
            assert False
        except:
            assert True

    def test_car_create_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_car'), {'mark': 'mb', 'model': 'c klasa',
                                                         'generation': 'W205', 'type_of_car': 'su',
                                                         'engine': 3000, 'combustion': 10,
                                                         'fuel': 'd', 'drive': 'rwd'})
        # cars = Cars.objects.create(mark='mb', model='c klasa', generation= 'W205', type_of_car= 'su',
        #                             fuel= 'd', engine=3000, combustion=10, drive= 'rwd')
        # cars.save()
        car = Cars.objects.get(mark='mb')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(car.mark, 'mb')
        self.assertEqual(car.model, 'c klasa')
        self.assertEqual(car.generation, 'W205')
        self.assertEqual(car.type_of_car, 'su')
        self.assertEqual(car.fuel, 'd')
        self.assertEqual(car.drive, 'rwd')

    def test_login_POST(self):
        user = User.objects.create(username='testowy@wp.pl')
        user.set_password('alamakota')
        user.save()
        response = self.client.post(reverse('login'), {'email': 'testuser', 'password': 'alamakota'})
        self.assertEqual(response.status_code, 302)

    def test_log_out(self):
        self.client.force_login(self.user)
        self.client.login(username='testuser', password='alamakota')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_comment_POST(self):
        self.client.force_login(self.user)
        posts = Post.objects.create(name='Testowy1', mark='mb',
                                    short_text='testowy krótki tekst',
                                    text='testowy text')
        posts.save()
        id = posts.id
        response = self.client.post(reverse('add_comment', args=(id,)), {'text': 'testowy text'})
        comment = Comment.objects.get(text='testowy text')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(comment.text, 'testowy text')


    def test_rate_POST(self):
        self.client.force_login(self.user)
        self.car = Cars.objects.create(mark='mb', model='c klasa',
                                       generation='W205', type_of_car='su',
                                       engine=3000, combustion=10,
                                       fuel='d', drive='rwd')
        self.car.save()
        id = self.car.id
        response = self.client.post(reverse('rate', args=(id,)), {'look': 4, 'price': 3, 'reliability': 4,
                                                                'practicality': 3, 'family_car': 4})
        rate = Rating.objects.get(look=4)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(rate.look, 4)
        self.assertEqual(rate.price, 3)
        self.assertEqual(rate.reliability, 4)
        self.assertEqual(rate.practicality, 3)
        self.assertEqual(rate.family_car, 4)
"""
Like Deletepost Editpost


class TestDifferentRequestMethods(TestCase):

    def test_my_get_request(self):
        response = self.client.get(reverse('remove_myclass', args=(myobject.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to remove') # THIS PART WORKS

    def test_my_post_request(self):
        post_response = self.client.post(reverse('remove_myclass', args=(myobject.id,)), follow=True)
        self.assertRedirects(post_response, reverse('myclass_removed'), status_code=302)
"""