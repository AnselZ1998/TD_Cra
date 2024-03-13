from django.contrib import admin

# Register your models here.
from . import models

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name',)

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',)

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',)

class ShotAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'sequence', )

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'shot', 'asset')

class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'element', 'project', 'task', 'number')


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Sequence, SequenceAdmin)
admin.site.register(models.Shot, ShotAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Version, VersionAdmin)