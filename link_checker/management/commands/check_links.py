from django.core.management.base import BaseCommand, CommandError

from datetime import time, datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from link_checker.models import Project, URL, Date
from link_checker.forms import ProjectForm
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_projects = Project.objects.all()
        if all_projects:

            for project in all_projects:
                try:

                    project_urls = project.related_urls.all().values_list('id', 'urls')  #dowlnoad relateds links
                    reqs = requests.get(project.title)
                    soup = BeautifulSoup(reqs.text, 'html.parser') #prasing links on site

                    # create list from links on site
                    urls_on_site = []
                    for link in soup.find_all('a'):
                        urls_on_site.append(link.get('href'))

                    #check urls on site
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