from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


CHOICES1 = [
    ('vw', 'Volkswagen'),
    ('re', 'Renault'),
    ('fo', 'Ford'),
    ('pe', 'Peugeot'),
    ('mb', 'Mercedes-Benz'),
    ('bm', 'BMW'),
    ('op', 'Opel/Vauxhall'),
    ('sk', 'Skoda'),
    ('au', 'Audi'),
    ('to', 'Toyota'),
    ('ci', 'Citroen'),
    ('fi', 'Fiat'),
    ('da', 'Dacia'),
    ('hy', 'Hyundai'),
    ('ki', 'Kia'),
    ('se', 'Seat'),
    ('ni', 'Nissan'),
    ('vo', 'Volvo'),
    ('su', 'Suzuki'),
    ('ma', 'Mazda'),
    ('mi', 'Mini'),
    ('je', 'Jeep'),
    ('lr', 'Land Rover'),
    ('mi', 'Mitsubishi'),
    ('ho', 'Honda'),
]
CHOICES2 = [
    ('og', 'Ogłoszenie'),
    ('sp', 'Sprzedaż'),
    ('ne', 'News'),
]
CHOICES3 = [
    ('su', 'SUV'),
    ('co', 'coupé'),
    ('dc', 'dual cowl'),
    ('fb', 'fastback'),
    ('hb', 'hatchback'),
    ('ka', 'kabriolet'),
    ('ko', 'kombi'),
    ('lb', 'liftback'),
    ('li', 'limuzyna'),
    ('mi', 'mikrovan'),
    ('mv', 'minivan'),
    ('pu', 'pick-up'),
    ('r', 'roadster'),
    ('s', 'sedan'),
    ('t', 'targa'),
    ('v', 'van')
]
CHOICES4 = [
    ('be', 'Benzyna'),
    ('bl', 'Benzyna + LPG'),
    ('bc', 'Benzyna + CNG'),
    ('d', 'Diesel'),
    ('e', 'Elektryczny'),
    ('et', 'Etanol'),
    ('h', 'Hybryda'),
    ('w', 'Wodór'),
]
CHOICES5 = [
    ('fwd', 'Na przednie koła'),
    ('rwd', 'Na tylnie koła'),
    ('awd', 'Na wszystkie koła'),
]
CHOICES6 = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class Post(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    mark = models.CharField(max_length=64, choices=CHOICES1)
    text = models.CharField(max_length=2048)
    date = models.DateField(default=timezone.now)
    datetime = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=64, choices=CHOICES2)
    short_text = models.CharField(max_length=128)
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()


class Cars(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    mark = models.CharField(max_length=64, choices=CHOICES1)
    model = models.CharField(max_length=64)
    generation = models.CharField(max_length=64)
    type_of_car = models.CharField(max_length=32, choices=CHOICES3)
    fuel = models.CharField(max_length=32, choices=CHOICES4)
    engine = models.IntegerField()
    combustion = models.IntegerField()
    drive = models.CharField(max_length=32, choices=CHOICES5)


class Rating(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, related_name='rates', null=True, blank=True, on_delete=models.CASCADE)
    look = models.IntegerField(choices=CHOICES6)
    price = models.IntegerField(choices=CHOICES6)
    reliability = models.IntegerField(choices=CHOICES6)
    practicality = models.IntegerField(choices=CHOICES6)
    family_car = models.IntegerField(choices=CHOICES6)


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.post.name, self.name)