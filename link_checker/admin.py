from django.contrib import admin

from .models import Project, URL, Date
# Register your models here.

admin.site.register(Project)
admin.site.register(URL)
admin.site.register(Date)
