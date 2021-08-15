from datetime import time, datetime

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, URL, Date
from .forms import ProjectForm
import requests
from bs4 import BeautifulSoup


# Create your views here.


def index(request):
    project_urls = []
    all_projects = Project.objects.all().values_list()
    check_list = all_projects.exists()
    if all_projects:
        first_project_id = all_projects[0][0]
        projects_name = Project.objects.get(id=first_project_id) #choose first item from list
        project_urls = projects_name.related_urls.all()
        projects_names = list(Project.objects.all())

        all_dates = Date.objects.all()
        update_time = all_dates[0]
        print(update_time)
    else:
        projects_names = []
        first_project_id = 0

    return render(request, 'index.html', {'projects_names': projects_names, 'project_urls': project_urls, 'selected_id': first_project_id, 'update_time': update_time})

def load_project(request, id):
    projects_name = Project.objects.get(id=id) #choose selected project from list
    project_urls = projects_name.related_urls.all()
    projects_names = list(Project.objects.all())

    return render(request, 'index.html', {'projects_names': projects_names, 'project_urls': project_urls, 'selected_id': id})

def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        project.delete()
        return redirect(index)

    return render(request, 'delete.html', {'project': project})


def new_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(index)
    return render(request, 'new.html', {'form':form})


def update_project(request, id):
    project = get_object_or_404(Project, pk=id)
    urls = URL.objects.filter(project=id).values_list('urls', flat=True)
    text = '\n'.join(urls)
    form = ProjectForm(request.POST or None, instance=project, initial={'urls': text})
    if form.is_valid():
        form.save()
        return redirect(index)
    return render(request, 'new.html', {'form': form})


def check_url(request):
    all_projects = Project.objects.all()
    if all_projects:

        for project in all_projects:
            project_urls = project.related_urls.all().values_list('id', 'urls') # pobranie powiązanych linków
            reqs = requests.get(project.title)
            soup = BeautifulSoup(reqs.text, 'html.parser') # parsowanie linków na stronie


            # stworzenie listy z linków stronie
            urls_on_site = []
            for link in soup.find_all('a'):
                urls_on_site.append(link.get('href'))

            #sprawdzenie czy urls sa w projekcie

            links_on_site = []
            for single_url in project_urls:
                if single_url[1] in urls_on_site:
                   url_to_update = URL.objects.get(id=single_url[0])
                   url_to_update.links_ok = True
                   url_to_update.save()
                   links_on_site.append(True)
                else:
                    url_to_update = URL.objects.get(id=single_url[0])
                    url_to_update.links_ok = False
                    url_to_update.save()
                    links_on_site.append(False)

            all_links_ok = all(links_on_site)
            project.links_ok = all_links_ok
            project.save()

        try:
            #dac warunek ze jesli jest cos w bazie danych !!!
            all_dates = Date.objects.all()
            print("tu jestem")
            print(all_dates)
            date_time = all_dates[0]
            date_time.time_of_update = datetime.now()
            date_time.save()
        except:
            date_time = Date.objects.create(time_of_update=datetime.now())
            date_time.save()

    return redirect(index)
