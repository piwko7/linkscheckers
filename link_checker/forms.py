from django import forms
from django.core.exceptions import ValidationError
from .models import Project, URL
from django.db import transaction

class ProjectForm(forms.ModelForm):

    urls = forms.CharField(widget=forms.Textarea, max_length=10000)
    class Meta:
        model = Project
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed_urls = set()
        # self.instance
    def clean_urls(self):
        data = self.cleaned_data['urls']
        self.parsed_urls =  set(data.split())
        if not self.parsed_urls:
            raise ValidationError("Musi byc chociaż 1 link")
        return data

    def save(self, commit=False):
        # obiekt typu Project
        with transaction.atomic():
            if self.instance.id:
                self._create()
            else:
                self._update()

    def _create(self):
        self.instance.save()
        old_urls = set(URL.objects.filter(project=self.instance).values_list('urls', flat=True))
        urls_to_delete = old_urls - self.parsed_urls
        urls_to_insert = self.parsed_urls - old_urls


        for url in urls_to_delete:
            URL.objects.filter(urls=url).delete()

        for url in urls_to_insert:
            URL.objects.create(urls=url, project=self.instance)

    def _update(self):
        # tutaj tworzymy nowy obiekt
        self.instance.save()
        for url in self.parsed_urls:
            URL.objects.create(urls=url, project=self.instance)