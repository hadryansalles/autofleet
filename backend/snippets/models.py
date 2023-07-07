from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django_admin_geomap import GeoItem

from django.contrib.auth.models import User, Permission

import math

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']


class Ping(models.Model):
    ping = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        '''lexer = get_lexer_by_name(self.language)
        ping = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=ping,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)'''
        super().save(*args, **kwargs)

class Manager(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ("name", "username")

    def save(self, *args, **kwargs):
        if not User.objects.filter(username=self.username).exists():
            user = User.objects.create_user(username=self.username,password=self.password,is_staff=True)
            #user.is_staff = True   

            #definindo as permissoes de um manager
            add_driver_permission = Permission.objects.get(codename='add_driver')
            change_driver_permission = Permission.objects.get(codename='change_driver')
            view_driver_permission = Permission.objects.get(codename='view_driver')
            delete_driver_permission = Permission.objects.get(codename='delete_driver')
            user.user_permissions.add(add_driver_permission)
            user.user_permissions.add(change_driver_permission)
            user.user_permissions.add(view_driver_permission)
            user.user_permissions.add(delete_driver_permission)

            add_manager_permission = Permission.objects.get(codename='add_manager')
            view_manager_permission = Permission.objects.get(codename='view_manager')
            #user.user_permissions.add(add_manager_permission) acho que talvez seria melhor somente os superusers adicionar novos managers
            user.user_permissions.add(view_manager_permission)        

            add_trip_permission = Permission.objects.get(codename='add_trip')
            change_trip_permission = Permission.objects.get(codename='change_trip')
            view_trip_permission = Permission.objects.get(codename='view_trip')
            delete_trip_permission = Permission.objects.get(codename='delete_trip')
            user.user_permissions.add(add_trip_permission)
            user.user_permissions.add(change_trip_permission)
            user.user_permissions.add(view_trip_permission)
            user.user_permissions.add(delete_trip_permission)
            
            view_trip_history_permission = Permission.objects.get(codename='view_triphistory')
            user.user_permissions.add(view_trip_history_permission)

            #user.user_permissions.add(view_driver_permission)

            view_trip_drowsiness_permission = Permission.objects.get(codename='view_tripdrowsiness')
            user.user_permissions.add(view_trip_drowsiness_permission)

            view_trip_hands_off_permission = Permission.objects.get(codename='view_triphandsoff')
            user.user_permissions.add(view_trip_hands_off_permission)

            add_device_permission = Permission.objects.get(codename='add_device')
            change_device_permission = Permission.objects.get(codename='change_device')
            view_device_permission = Permission.objects.get(codename='view_device')
            delete_device_permission = Permission.objects.get(codename='delete_device')
            user.user_permissions.add(add_device_permission)
            user.user_permissions.add(change_device_permission)
            user.user_permissions.add(view_device_permission)
            user.user_permissions.add(delete_device_permission)

            user.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if User.objects.filter(username=self.username).exists():
            user = User.objects.get(username=self.username)
            user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    trips_count = models.IntegerField()

    class Meta:
        ordering = ("name", "manager")

    def save(self, *args, **kwargs):
        if not User.objects.filter(username=self.username).exists():
            user = User.objects.create_user(username=self.username,password=self.password,is_staff=True)
            #definindo as permissoes de um driver
            change_trip_permission = Permission.objects.get(codename='change_trip')
            view_trip_permission = Permission.objects.get(codename='view_trip')
            user.user_permissions.add(change_trip_permission)
            user.user_permissions.add(view_trip_permission)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if User.objects.filter(username=self.username).exists():
            user = User.objects.get(username=self.username)
            user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Device(models.Model):
    device_number = models.IntegerField(null=True, blank=True, unique=True)
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.device_number}"

class Trip(models.Model):
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    real_start = models.DateTimeField(null=True, blank=True)
    real_end = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)   # seta null para motorista excluido...
    device_id = models.ForeignKey(Device,on_delete=models.SET_NULL,null=True, blank=True)
    is_started = models.BooleanField(default=False)  # indica se a viagem foi iniciada
    is_ended = models.BooleanField(default=False)

    class Meta:
        ordering = ("id", "driver")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.real_start}, {self.real_end}, {self.driver.name}"

class TripHistory(models.Model, GeoItem):
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING)
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    acc_x = models.FloatField()
    acc_y = models.FloatField()
    acc_z = models.FloatField()
    acc = models.FloatField(null=True)
    hands_state = models.IntegerField(null=True)    # null=True só para nao afetar as trips existentes no momento da adição do campo hands_state
    drowsy_state = models.IntegerField(null=True)   # null=True só para nao afetar as trips existentes no momento da adição do campo drowsy_state
    date = models.DateTimeField(blank=True, null=True)
    
    @property
    def geomap_icon(self):
        if self.drowsy_state == 2:
            return "https://maps.google.com/mapfiles/ms/micons/red.png"
        elif self.speed > 90:
            return "https://maps.google.com/mapfiles/ms/micons/purple.png"
        elif self.speed > 50 or (self.acc != None and self.acc > 4.0):
            return "https://maps.google.com/mapfiles/ms/micons/blue.png"
        else:
            return "https://maps.google.com/mapfiles/ms/micons/green.png"

    @property
    def geomap_longitude(self):
        return '' if (self.longitude is None or self.longitude == 0) else str(self.longitude)

    @property
    def geomap_latitude(self):
        return '' if (self.latitude is None or self.latitude == 0) else str(self.latitude)

    def save(self, *args, **kwargs):
        self.acc_x = (self.acc_x / 16384) * 9.8
        self.acc_y = (self.acc_y / 16384) * 9.8
        self.acc_z = (self.acc_z / 16384) * 9.8
        self.acc = abs(math.sqrt(self.acc_x**2 + self.acc_y**2 + self.acc_z**2) - 9.8)
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.trip.id}"

class TripDrowsiness(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    duration = models.FloatField()
    drowsy_ratio = models.FloatField()

    class Meta:
        ordering = ("id", "trip")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.trip.id}, {self.date},{self.drowsy_ratio}"


class TripHandsOff(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    duration = models.FloatField()
    hands_off = models.IntegerField()

    class Meta:
        ordering = ("id", "trip")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.trip.id}, {self.date},{self.hands_off}"
