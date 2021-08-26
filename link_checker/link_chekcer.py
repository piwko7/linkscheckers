import requests
from bs4 import BeautifulSoup

xxx = 'https://media2.pl/tech/165329-Tanie-zakupy-przez-Internet-serwis-z-rankingami-produktow.html'
project_name = 'https://najlepszy-ranking.pl/'


project_urls = ['http://swiatnaobcasach.pl/jak-wybrac-krem-cc-z-dobrym-skladem/', 'http://ww.google.pl', 'https://szafa.pl/porady/293-ranking-butow-do-biegania-postaw-na-wygode.html']



reqs = requests.get(project_name)
soup = BeautifulSoup(reqs.text, 'html.parser')
urls_on_site = []
for link in soup.find_all('a'):
    urls_on_site.append(str(link.get('href')))

print(urls_on_site)


# for single_url in project_urls:
#     if single_url in urls_on_site:
#         print('To chyba dziala')
#
#
#
# for url in urls_on_site:
#     print(project_name)
#     if project_name in url:
#         print('oto jest pan')
#     else:
#         print('a na imie mu dzban')


# if (any(project_name in url for url in urls_on_site)):
#     print('oto jest pan')
# else:
#     print('a na imie mu dzban')
#
#
# if 'https://najlepszy-ranking.pl' in 'https://najlepszy-ranking.pl':
#     print('zyje')
