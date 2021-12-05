from django.db import models
from django.contrib.auth.models import User, Group

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name = 'Associated user', on_delete = models.CASCADE, primary_key = True)
    address = models.TextField('Address', blank = True)
    phone = models.CharField('Phone number', max_length = 32, blank = True)
    alt_email = models.EmailField('Alternate email address', blank = True)
    
    class Meta:
        ordering = ["user"]
    
    def __str__(self):
        return f'Profile for \'{self.user.username}\''

class Course(models.Model):
    name = models.CharField('Course name', max_length = 256, primary_key = True, default = 'No course name')
    desc = models.CharField('Course description', max_length = 256, default = 'No course description')
    users = models.ManyToManyField(User, verbose_name = 'Assigned instructors and TAs', blank = True)
    
    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return f'{self.name} ({self.desc})'

class Section(models.Model):
    name = models.CharField('Section name', max_length = 256, primary_key = True, default = 'No section name')
    course = models.ForeignKey(Course, verbose_name = 'Associated course', on_delete = models.CASCADE, default = None)
    users = models.ManyToManyField(User, verbose_name = 'Assigned TAs', blank = True)
    
    class Meta:
        ordering = ["course", "name"]
    
    def __str__(self):
        return f'{self.course.name} ({self.course.desc}) - {self.name}'
