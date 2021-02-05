from requests import request
from bs4 import BeautifulSoup
import re
from json import dumps

PATTERN = re.compile(r'.html{1}|.css{1}|.json{1}|.md{1}|.js{1}|[.{1}]')


class GithubScraping:

    def __init__(self, repositores):
        """
        :param repositories: receive a .txt document
        in a string to be readable for built-in function open()
        """
        self.repositores = repositores

    def get_project_paths(self):
        """
        a method that return a list of possible
        repositories in as .txt document.

        :return: a list of of repositories
        """
        list = []
        with open(self.repositores, 'r') as file:
            data = file.readlines()
            for item in data:
                _ = item.replace('\n', '')
                list.append(_)

        return list

    def link_stratctor(self, href):
        '''
        a function that return a list on urls from a project
        :param href: link of project to stract urls
        :return: a list of urls
        '''
        url_list = []
        url = f'https://github.com/{href}'
        response = request(url=url, method='GET')
        content = response.content
        html_parser = BeautifulSoup(content, 'html.parser')
        urls = html_parser.find_all('a', attrs={'class': 'js-navigation-open link-gray-dark'})

        for item in urls:
            url_list.append(item.get('href'))

        return url_list

    def find_pattern(self, href):
        '''
        a function that return a pattern extension
        :param href: link to search patterns
        :return: match or not match
        '''
        if_pattern = PATTERN.search(href)
        find_pattern = if_pattern

        return find_pattern

    def get_file_info(self, file):
        '''
        A function that returns a dictionay info of a github file project
        :param file: link of github project file
        :return: a dictionary file info
        '''
        conversor = 0
        resnpose = request(url=f'https://github.com/{file}', method='GET')
        content = resnpose.content
        html_parser = BeautifulSoup(content, 'html.parser')
        file_info = {}
        file_extension = html_parser.find('strong', attrs={'class': 'final-path'}).text
        file_line = html_parser.find('div', attrs={
            'class': 'text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0'}).text
        if '.png' in file_extension or '.jpg' in file_extension:
            x = file_line.split('\n')
            xy = []
            for item in x:
                xy.append(item.strip().split(' '))
            xy.pop(0)
            xy.pop(0)
            xy.pop()
            if xy[0][1] == 'MB':
                conversor = float(xy[0][0]) * 1000
                file_info['file'] = {'extension': file_extension, 'info': {'linhas': 0, 'kbytes': conversor}}
            elif xy[0][1] == 'Bytes':
                conversor = float(xy[0][0]) * 1000
                file_info['file'] = {'extension': file_extension, 'info': {'linhas': 0, 'kbytes': conversor}}
            else:
                file_info['file'] = {'extension': file_extension, 'info': {'linhas': 0, 'kbytes': float(xy[0][0])}}
        else:
            x = file_line.split('\n')
            x.pop(0)
            x.pop(0)
            x.pop(1)
            x.pop(2)
            y = []
            for _ in range(len(x)):
                y.append(x[_].strip().split(' '))
            file_info['file'] = {'extension': file_extension,
                                 'info': {'linhas': int(y[0][0]), 'kbytes': float(y[1][0])}}

        return file_info

    def write_txt_file(self, arquivo):
        '''
        a function that write a txt file with github project info
        :param arquivo: a list of files to write
        :return: None
        '''
        statistics = self.get_project_statistics(arquivo)
        for itens in arquivo:
            result = itens
            file = open(f'git_info_{result["projeto"].replace("/", "_")}.txt', 'w', encoding='utf-8')
            file.write(f'[{result["projeto"]}]\n')
            if result['diretorios']:
                # varredura do primeiro nivel do projeto diretorios/arquivos (root)
                for item in result['diretorios']:
                    file.write(f'|_[{item["diretorio"]}]\n')
                    if item['diretorios']:
                        # varredura do segundo nível do projeto diretorios/arquivos (first directory layer)
                        for i in item['diretorios']:
                            file.write(f'{"|":<}{"|_":>5}[{i["diretorio"]}]\n')
                            if i['diretorios']:
                                # varredura do terceiro nivel do projeto diretorios/arquivos (second directory layer)
                                for j in i['diretorios']:
                                    file.write(f'{"|":<}{"|":>4}{"|_":>5}[{j["diretorio"]}]\n')
                                    if j['diretorios']:
                                        for k in j['diretorios']:
                                            file.write(f'{"|":<}{"|":>4}{"|":>4}{"|_":>6}[{k["diretorio"]}]\n')
                                            if k['diretorios']:
                                                for l in k['diretorios']:
                                                    file.write(
                                                        f'{"|":<}{"|":>4}{"|":>4}""{"|_":>7}[{l["diretorio"]}]\n')
                                            if k['arquivos']:
                                                for kt in k['arquivos']:
                                                    file.write(
                                                        f'{"|":<}{"|":>4}{"|":>4}{"|":>5}{"|_":>5} {kt["file"]["extension"]} - {kt["file"]["info"]["linhas"]} linhas\n')
                                    if j['arquivos']:
                                        for jt in j['arquivos']:
                                            file.write(
                                                f'{"|":<}{"|":>4}{"|":>4}{"|_":>4} {jt["file"]["extension"]} - {jt["file"]["info"]["linhas"]} linhas\n')
                            if i['arquivos']:
                                for it in i['arquivos']:
                                    file.write(
                                        f'{"|":<}{"|":>4}{"|_":>5} {it["file"]["extension"]} - {it["file"]["info"]["linhas"]} linhas\n')
                    if item['arquivos']:
                        for item1 in item['arquivos']:
                            file.write(
                                f'{"|":<}{"|_":>5} {item1["file"]["extension"]} - {item1["file"]["info"]["linhas"]} linhas\n')

            if result['arquivos']:
                for item in result['arquivos']:
                    file.write(f'|_{item["file"]["extension"]} - {item["file"]["info"]["linhas"]} linhas \n')

            file.write(f'\n{"-" * 6} Estatisticas por Extensão {"-" * 6}\n')
            file.write(f'{"Extensão":<}{"|":^8}{"Linhas":^8}{"|":^8}{"Bytes":^8}\n')
            for item in statistics:
                for k, v in item.items():
                    file.write(
                        f'{k}{v["linhas"]:>15} ({v["total_linhas"]:.0f}%) {v["kbytes"]:>9.0f} ({v["total_bytes"]:.0f}%)\n')

            file.close()
            print('arquivos gerados!!')

    def get_all_info(self, arquivo):
        '''
        a function that return all info about directories and files project
        :param arquivo: list of paths project
        :return: a list of directories and file about project
        '''
        info_lista = []
        object_git = {}
        path = arquivo
        for item in path:
            object_git = {'projeto': item, 'diretorios': [], 'arquivos': []}
            urls = self.link_stratctor(f'{item}')
            for url in urls:
                pattern = self.find_pattern(url)
                if not pattern:
                    y = url.split('/')
                    diretorio = {'diretorio': y[-1], 'diretorios': [], 'arquivos': []}
                    url_dir = self.link_stratctor(url)
                    for i in url_dir:
                        pattern = self.find_pattern(i)
                        if not pattern:
                            j = i.split('/')
                            dir_filho = {'diretorio': j[-1], 'diretorios': [], 'arquivos': []}
                            url_dir2 = self.link_stratctor(i)
                            for k in url_dir2:
                                pattern = self.find_pattern(k)
                                if not pattern:
                                    dir_name_layer2 = k.split('/')
                                    dir_filho_layer2 = {'diretorio': dir_name_layer2[-1], 'diretorios': [],
                                                        'arquivos': []}
                                    url_dir_layer2 = self.link_stratctor(k)
                                    for link_layer2 in url_dir_layer2:
                                        pattern = self.find_pattern(link_layer2)
                                        if not pattern:
                                            dir_name_layer3 = link_layer2.split('/')
                                            dir_filho_layer3 = {'diretorio': dir_name_layer3[-1], 'diretorios': [],
                                                                'arquivos': []}
                                            url_dir_layer3 = self.link_stratctor(link_layer2)
                                            for link_layer3 in url_dir_layer3:
                                                pattern = self.find_pattern(link_layer3)
                                                if not pattern:
                                                    pass
                                                else:
                                                    file = self.get_file_info(link_layer3)
                                                    dir_filho_layer3['arquivos'].append(file)
                                            dir_filho_layer2['diretorios'].append(dir_filho_layer3)
                                        else:
                                            file = self.get_file_info(link_layer2)
                                            dir_filho_layer2['arquivos'].append(file)
                                    dir_filho['diretorios'].append(dir_filho_layer2)
                                else:
                                    file = self.get_file_info(k)
                                    dir_filho['arquivos'].append(file)
                            diretorio['diretorios'].append(dir_filho)
                        else:
                            file = self.get_file_info(i)
                            diretorio['arquivos'].append(file)
                    object_git['diretorios'].append(diretorio)
                else:
                    file = self.get_file_info(url)
                    object_git['arquivos'].append(file)
            info_lista.append(object_git)

        return info_lista

    def write_json_file(self, arquivo):
        '''
        a function to create a json file
        :param arquivo: a list of info to jsonfy
        :return: None
        '''
        for item in arquivo:
            name_json = item['projeto'].replace('/', '-')
            file = open(f'git_info{name_json}.json', 'w')
            dumps(item, indent=4)
            file.close()
            print(f'Arquivo {name_json} Json Criado')

    def get_project_statistics(self, arquivo):
        '''
        a function to get statistics of extension usage from project
        :param arquivo: list of project info
        :return: a list of statistics from project
        '''
        statistic_list = []
        total_kbytes = 0
        total_linhas = 0
        statistics = {'js': {'linhas': 0, 'kbytes': 0},
                      'html': {'linhas': 0, 'kbytes': 0},
                      'css': {'linhas': 0, 'kbytes': 0},
                      'md': {'linhas': 0, 'kbytes': 0},
                      'json': {'linhas': 0, 'kbytes': 0},
                      'outro': {'linhas': 0, 'kbytes': 0}}
        for item in arquivo:
            if item['diretorios']:
                for layer1 in item['diretorios']:
                    if layer1['diretorios']:
                        for layer2 in layer1['diretorios']:
                            if layer2['diretorios']:
                                for layer3 in layer2['diretorios']:
                                    if layer3['diretorios']:
                                        for layer4 in layer3['diretorios']:
                                            if layer4['diretorios']:
                                                for layer5 in layer4['diretorios']:
                                                    if layer5['diretorios']:
                                                        pass
                                                    if layer5['arquivos']:
                                                        pass
                                            if layer4['arquivos']:
                                                for arquivo_layer4 in layer4['arquivos']:
                                                    file = arquivo_layer4['file']['extension'].split('.')
                                                    file_name = file[-1]
                                                    if file_name in statistics.keys():
                                                        statistics[file_name]['linhas'] += \
                                                            arquivo_layer4['file']['info'][
                                                                'linhas']
                                                        statistics[file_name]['kbytes'] += \
                                                        arquivo_layer4['file']['info']['kbytes']
                                                        total_kbytes += arquivo_layer4['file']['info']['kbytes']
                                                        total_linhas += arquivo_layer4['file']['info']['linhas']
                                                    else:
                                                        statistics['outro']['linhas'] += arquivo_layer4['file']['info'][
                                                            'linhas']
                                                        statistics['outro']['kbytes'] += arquivo_layer4['file']['info'][
                                                            'kbytes']
                                                        total_kbytes += arquivo_layer4['file']['info']['kbytes']
                                                        total_linhas += arquivo_layer4['file']['info']['linhas']
                                    if layer3['arquivos']:
                                        for arquivo_layer3 in layer3['arquivos']:
                                            file = arquivo_layer3['file']['extension'].split('.')
                                            file_name = file[-1]
                                            if file_name in statistics.keys():
                                                statistics[file_name]['linhas'] += arquivo_layer3['file']['info'][
                                                    'linhas']
                                                statistics[file_name]['kbytes'] += arquivo_layer3['file']['info'][
                                                    'kbytes']
                                                total_kbytes += arquivo_layer3['file']['info']['kbytes']
                                                total_linhas += arquivo_layer3['file']['info']['linhas']
                                            else:
                                                statistics['outro']['linhas'] += arquivo_layer3['file']['info'][
                                                    'linhas']
                                                statistics['outro']['kbytes'] += arquivo_layer3['file']['info'][
                                                    'kbytes']
                                                total_kbytes += arquivo_layer3['file']['info']['kbytes']
                                                total_linhas += arquivo_layer3['file']['info']['linhas']
                            if layer2['arquivos']:
                                for arquivo_layer2 in layer2['arquivos']:
                                    file = arquivo_layer2['file']['extension'].split('.')
                                    file_name = file[-1]
                                    if file_name in statistics.keys():
                                        statistics[file_name]['linhas'] += arquivo_layer2['file']['info']['linhas']
                                        statistics[file_name]['kbytes'] += arquivo_layer2['file']['info']['kbytes']
                                        total_kbytes += arquivo_layer2['file']['info']['kbytes']
                                        total_linhas += arquivo_layer2['file']['info']['linhas']
                                    else:
                                        statistics['outro']['linhas'] += arquivo_layer2['file']['info']['linhas']
                                        statistics['outro']['kbytes'] += arquivo_layer2['file']['info']['kbytes']
                                        total_kbytes += arquivo_layer2['file']['info']['kbytes']
                                        total_linhas += arquivo_layer2['file']['info']['linhas']
                    if layer1['arquivos']:
                        for arquivo_layer1 in layer1['arquivos']:
                            file = arquivo_layer1['file']['extension'].split('.')
                            file_name = file[-1]
                            if file_name in statistics.keys():
                                statistics[file_name]['linhas'] += arquivo_layer1['file']['info']['linhas']
                                statistics[file_name]['kbytes'] += arquivo_layer1['file']['info']['kbytes']
                                total_kbytes += arquivo_layer1['file']['info']['kbytes']
                                total_linhas += arquivo_layer1['file']['info']['linhas']
                            else:
                                statistics['outro']['linhas'] += arquivo_layer1['file']['info']['linhas']
                                statistics['outro']['kbytes'] += arquivo_layer1['file']['info']['kbytes']
                                total_kbytes += arquivo_layer1['file']['info']['kbytes']
                                total_linhas += arquivo_layer1['file']['info']['linhas']
            if item['arquivos']:
                for arquivo_root in item['arquivos']:
                    file = arquivo_root['file']['extension'].split('.')
                    file_name = file[-1]
                    if file_name in statistics.keys():
                        statistics[file_name]['linhas'] += arquivo_root['file']['info']['linhas']
                        statistics[file_name]['kbytes'] += arquivo_root['file']['info']['kbytes']
                        total_kbytes += arquivo_root['file']['info']['kbytes']
                        total_linhas += arquivo_root['file']['info']['linhas']
                    else:
                        statistics['outro']['linhas'] += arquivo_root['file']['info']['linhas']
                        statistics['outro']['kbytes'] += arquivo_root['file']['info']['kbytes']
                        total_kbytes += arquivo_root['file']['info']['kbytes']
                        total_linhas += arquivo_root['file']['info']['linhas']

        statistic_list.append(statistics)

        for item in statistic_list:
            for k in item.values():
                if k['kbytes'] == 0:
                    k['total_bytes'] = 0
                    k['total_linhas'] = 0
                else:
                    porcentagem_kbytes = (k['kbytes'] / total_kbytes) * 100
                    porcentagem_linhas = (k['linhas'] / total_linhas) * 100
                    k['total_bytes'] = porcentagem_kbytes
                    k['total_linhas'] = porcentagem_linhas

        return statistic_list
