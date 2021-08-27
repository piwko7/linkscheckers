from datetime import time, datetime, timedelta

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
        test = first_project_id - len(all_projects) + 3
        projects_name = Project.objects.get(id=first_project_id) #choose first item from list
        project_urls = projects_name.related_urls.all()
        projects_names = list(Project.objects.all())
        selected_project = 1

        try:
            all_dates = Date.objects.all()
            update_time = all_dates[0]
        except:
            update_time = None
    else:
        projects_names = []
        first_project_id = 0
        update_time = None
        selected_project = None

    return render(request, 'index.html', {'projects_names': projects_names, 'project_urls': project_urls, 'selected_id': first_project_id, 'selected_project': selected_project, 'update_time': update_time})

def load_project(request, id):
    projects_name = Project.objects.get(id=id) #choose selected project from list
    project_urls = projects_name.related_urls.all()
    projects_names = list(Project.objects.all())

    # find selected id from HTML
    all_projects = list(Project.objects.all().values_list('id', flat=True))
    selected_project = all_projects.index(id) + 1

    try:
        all_dates = Date.objects.all()
        update_time = all_dates[0]
    except:
        update_time = None

    return render(request, 'index.html', {'projects_names': projects_names, 'project_urls': project_urls, 'selected_id': id, 'selected_project': selected_project, 'update_time': update_time})

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
            try:
                project_urls = project.related_urls.all().values_list('id', 'urls')  #dowlnoad relateds links

                links_on_site = [] #check urls on site
                for single_url in project_urls:
                    reqs = requests.get(single_url[1])
                    time.sleep(3)
                    soup = BeautifulSoup(reqs.text, 'html.parser') #prasing links on site

                    # create list from links on site
                    urls_on_site = []
                    for link in soup.find_all('a'):
                        urls_on_site.append(str(link.get('href')))

                # for single_url in project_urls:
                    if (any(project.title in url for url in urls_on_site)):

                        url_to_update = URL.objects.get(id=single_url[0])
                        url_to_update.links_ok = True
                        url_to_update.save()
                        links_on_site.append(True)
                    else:
                        url_to_update = URL.objects.get(id=single_url[0])
                        url_to_update.links_ok = False
                        url_to_update.save()
                        links_on_site.append(False)

                #save True/False for main Project
                all_links_ok = all(links_on_site)
                project.links_ok = all_links_ok
                project.save()
            except:
                # except if project name is wrong
                pass
            try:
                all_dates = Date.objects.all()
                date_time = all_dates[0]
                date_time.time_of_update = datetime.now() + timedelta(hours=2)
                date_time.save()
            except:
                date_time = Date.objects.create(time_of_update=datetime.now()+ timedelta(hours=2))
                date_time.save()

    return redirect(index)

