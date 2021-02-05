'''

TESTS OF A SINGLE REPOSITORE

'''


from requests import request
from bs4 import BeautifulSoup
import re
from gitutils import github_scraping

teste = github_scraping.GithubScraping()

pattern = re.compile(r'.html{1}|.css{1}|.json{1}|.md{1}|.js{1}|[.{1}]')
lista = []
projeto = {}

with open('repositores.txt', 'r') as file:
    data = file.readlines()
    for item in data:
        x = item.replace('\n', '')
        lista.append(x)

URL = f'https://github.com/{lista[2]}'
projeto['projeto'] = lista[2]
projeto['diretorios'] = []
projeto['arquivos'] = []


response = request(url=URL, method='GET')
conteudo = response.content

find = BeautifulSoup(conteudo, 'html.parser')
lista_teste = []
urls = find.find_all('a', attrs={'class': 'js-navigation-open link-gray-dark'})

for item in urls:
    if_pattern = teste.find_pattern(item.get('href'))
    if if_pattern:
        projeto['arquivos'].append(teste.get_file_info(item.get('href')))
    else:
        x = item.get('href')
        y = x.split('/')
        dir_dict = {'diretorio': y[-1], 'diretorios': [], 'arquivos': []}
        projeto['diretorios'].append(dir_dict)

print(projeto)
'''
    if not find_pattern:
        #print(item.get('href'))
        req = request(url=f'https://github.com/{item.get("href")}')
        conteudo = req.content
        html_parser = BeautifulSoup(conteudo, 'html.parser')
        urls = html_parser.find_all('a', attrs={'class': 'js-navigation-open link-gray-dark'})

    else:
        #print(item.get('href'))
        pass




print(f'Extensões de codigo e arquivos\n'
      f'{links}\n'
      f'Diretorios\n'
      f'{directory}')
'''

'''links_dir1 = []
links_dir2 = []
dir_links1 = []
dir_links2 = []'''
'''
if directory:
    for item in directory:
        req_dir = request(url=f'https://github.com/{item}', method='GET')
        info_dir = req_dir.content
        dir_soup = BeautifulSoup(info_dir, 'html.parser')
        dir_urls = dir_soup.find('a', attrs={'class': 'js-navigation-open link-gray-dark'})
        for item in dir_urls:
            dir_if_pattern = pattern.search(item.get('href'))
            dir_find_pattern = dir_if_pattern
            if dir_find_pattern:
                #links_dir1.append(item.get('href'))
                print(item.get('href'))
            else:
                #dir_links1.append(item.get('href'))
                print(item.get('href'))
            
            if dir_links1:
                for item in dir_links1:
                    req_dir1 = request(url=f'https://github.com/{item}', method='GET')
                    info_dir1 = req_dir1.content
                    dir1_soup = BeautifulSoup(info_dir1, 'html.parser')
                    dir1_urls = dir1_soup.find('a', attrs={'class': 'js-navigation-open link-gray-dark'})
                    for item in dir1_urls:
                        dir1_if_pattern = pattern.search(item.get('href'))
                        dir1_find_pattern = dir1_if_pattern
                        if dir1_find_pattern:
                            links_dir2.append(item.get('href'))
                        else:
                            dir_links2.append(item.get('href'))
            else:
                pass
            
else:
    pass
'''

'''
if links:
    for item in links:
        req_link = request(url=f'https://github.com/{item}', method='GET')
        info_link = req_link.content
        link_soup = BeautifulSoup(info_link, 'html parser')

else:
    pass
'''