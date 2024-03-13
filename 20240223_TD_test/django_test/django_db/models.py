from django.db import models

# Create your models here.

class Class(models.Model):
    name = models.CharField(null=False, max_length=16)

    def __str__(self):
        return self.name
class Student(models.Model):
    name = models.CharField(null=False, max_length=16)
    age = models.IntegerField(null=False)
    sex = models.CharField(choices=(('male', 'Male'), ('famale', 'Famale')), default='male', max_length=8)
    clas = models.ForeignKey(to='Class', related_name='students', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name