from django.contrib import admin

# Register your models here.
from .models import Class, Student

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name','students')

    def students(self, obj):
        return ','.join ([s.name for s in obj.students.all()])


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'clas')

admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)