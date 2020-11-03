from django.contrib.auth.models import Permission, User
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name




# class Project_access(models.Model):
#     project_name = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
#     #project_owner_id = models.IntegerField(max_length=2, default=1)
#     project_owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='project_owner', default=1)
#     project_owner_email = models.EmailField(blank=True, unique=False)
#     requester = models.ForeignKey(User, on_delete=models.CASCADE,related_name='requester', default=1)
#     requester_email = models.EmailField(blank=True, unique=False)
#     notes = models.CharField(max_length=100, default='Need access to the project to make change and execute jobs')
#     role = models.CharField(max_length=10, choices=ROLE_TYPE, default='Master')
#     status = models.CharField(max_length=50, default='Pending')
#     access = models.BooleanField(default=False)











# class Album(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     artist = models.CharField(max_length=250)
#     album_title = models.CharField(max_length=500)
#     genre = models.CharField(max_length=100)
#     album_logo = models.FileField()
#     is_favorite = models.BooleanField(default=False)

#     def __str__(self):
#         return self.album_title + ' - ' + self.artist


# class Song(models.Model):
#     album = models.ForeignKey(Album, on_delete=models.CASCADE)
#     song_title = models.CharField(max_length=250)
#     audio_file = models.FileField(default='')
#     is_favorite = models.BooleanField(default=False)

#     def __str__(self):
#         return self.song_title


