from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Like)