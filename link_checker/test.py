def check_url(request):
    all_projects = Project.objects.all()
    if all_projects:

        for project in all_projects:
            project_urls = project.related_urls.all().values_list('urls', flat=True) # pobranie powiązanych linków
            reqs = requests.get(project.title)
            soup = BeautifulSoup(reqs.text, 'html.parser') # parsowanie linków na stronie

            # stworzenie listy z linków stronie
            urls_on_site = []
            for link in soup.find_all('a'):
                urls_on_site.append(link.get('href'))

            #sprawdzenie czy urls sa w projekcie

            links_on_site = []
            for single_url in project_urls:
                print(single_url)
                print(urls_on_site)
                if single_url in urls_on_site:
                   url_to_update = URL.objects.get(urls=single_url)
                   url_to_update.links_ok = True
                   url_to_update.save()
                   links_on_site.append(True)
                else:
                    url_to_update = URL.objects.get(urls=single_url)
                    url_to_update.links_ok = False
                    url_to_update.save()
                    links_on_site.append(False)

            all_links_ok = all(links_on_site)
            project.links_ok = all_links_ok
            project.save()

    return redirect(index)