from django.contrib import admin
from . import models

# Register your models here.
class Projectadmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', )

class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)

class SaquenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')

class ShottAdmin(admin.ModelAdmin):
    list_display = ('name', 'sequence', 'project')

class TasktAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset', 'shot', 'project')

class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'element', 'number', 'task', 'project')

admin.site.register(models.Project, Projectadmin)
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Sequence, SaquenceAdmin)
admin.site.register(models.Shot, ShottAdmin)
admin.site.register(models.Task, TasktAdmin)
admin.site.register(models.Version, VersionAdmin)
