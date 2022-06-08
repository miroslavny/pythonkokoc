import requests
from bs4 import BeautifulSoup
import re

main_url = 'https://ak-sound.ru'

request = requests.get(main_url)


match = re.search(r"Google Tag Manager -->(.*?'(GTM-[0-9a-zA-Z]+)'.*?)<!-- End Google Tag Manager", request.text,
                  re.DOTALL)
if match is not None:
    print(match.group(1))
    gtm = match.group(2)
    print(gtm)
else:
    print('ничего не найдено')



uniq_urls = set()
soup = BeautifulSoup(request.text, "html.parser")
for link in soup.findAll('a'):
    url = link.get('href')
    if url:
        url = url.split('#')[0]
    if url:
        if main_url in url:
            url = url.replace(main_url, '')
        if url.startswith('http://') or url.startswith('https://') or url.startswith('mailto:') or url.startswith('tel:') or 'javascript' in url:
            continue
        uniq_urls.add(url)

print(f'найдено {len(uniq_urls)} уникальных ссылок')


uniq_urls_short = []
for url in uniq_urls:
    print(url)
    uniq_urls_short.append(url)


uniq_urls_full = [main_url + url for url in uniq_urls_short]
print(*uniq_urls_full)

gtms = set()
for x in uniq_urls_full:
    request1 = requests.get(x)
    match1 = re.search(r"Google Tag Manager -->(.*?'(GTM-[0-9a-zA-Z]+)'.*?)<!-- End Google Tag Manager", request.text,
                       re.DOTALL)
    if match1 is not None:
        gtms.add(match.group(2))
    else:
        print('GTM не на всех страницах')
        break

if len(gtms) == 1:
    print("GTM на всех страницах")
elif len(gtms) > 1:
    print ("На страницах разные GTM")
