from gitutils.github_scraping import GithubScraping

project = GithubScraping('repositores.txt')
path = project.get_project_paths()

for item in path:
    print('Buscando informações do projeto')
    repositores_info = project.get_all_info(path)
    print('done!')
    print('Buscando estatisticas do projeto')
    arquivo = project.get_project_statistics(repositores_info)
    print('done!')
    print('Gerando Arquivos')
    txt = project.write_txt_file(repositores_info)
