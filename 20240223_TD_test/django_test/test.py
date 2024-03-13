import random

import django
import random
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test.settings'
django.setup()

from django_db.models import Class, Student

for c in Class.objects.all():
    #print(c.name)
    pass

for c in Student.objects.all():
    #print(c.name)
    pass

'''for i in range(10):
    student = Student.objects.create(
        name = f'new_student_{i}',
        age = random.randint(0, 50),
        clas = Class.objects.get(id = i % 2 + 1)
    )

    print(student)

clas = Class.objects.get(id = 1)
students = clas.students.all()
students_order = clas.students.all().order_by('age')
for i in students:
    #打印
    print(i.name, i.age, i.sex)

#排序
for i in students_order:
    print(i.name)'''

#class filter方法
students = Student.objects.filter(clas__id__exact = 1)
for i in students:
    print(i.name)
print('年龄')
#年龄大于10
students = Student.objects.filter(age__gt = 10)
for i in students:
    print(i.name)