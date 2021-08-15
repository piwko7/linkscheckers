from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=2000)
    links_ok = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.title


class URL(models.Model):
    urls = models.CharField(max_length=2000)
    links_ok = models.BooleanField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='related_urls')

    def __str__(self):
        return "{} {}".format(self.project.title, self.urls)

class Date(models.Model):
    time_of_update = models.DateTimeField()




