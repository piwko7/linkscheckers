import requests
from bs4 import BeautifulSoup


def check_link(project_name, project_urls):
    reqs = requests.get(project_name)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls_on_site = []
    for link in soup.find_all('a'):
        urls_on_site.append(link.get('href'))

    print(urls_on_site)


    for single_url in project_urls:
        if single_url in urls_on_site:
            print('To chyba dziala')

check_link('https://www.devilpage.pl/', ['http://www.mufsc.pl', 'http://ww.google.pl'])