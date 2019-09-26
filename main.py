# Importando a biblioteca 'sys' para receber os pa-
# râmetros via linha de comando
import sys

# Importando biblioteca de datas
from datetime import datetime

# Importando biblioteca para fazer parsing dos 
# argumentos.
import argparse

# Importação da biblioteca de interface com o SO
import os

# Importação de biblioteca de expressões regulares
import re

# Importando biblioteca para utilização de JSON
import json

# Importando subprocesso para injetar comandos no
# terminal do Sistema Operacional
import subprocess

# Regex de nomes de arquivos que devem ser incluídos
including_names = []

# Definição do header do arquivo latex do jeito que 
# costumo usar
header = r'''\documentclass{article}

\usepackage[top=20mm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[brazil]{babel}
\usepackage{xcolor}
\usepackage{float}
\usepackage{graphicx}
\usepackage{color}
\usepackage{multirow}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{longtable}
\usepackage{minted}
\usepackage{url}
\usepackage{tikz}

\usemintedstyle{manni}

\DeclareCaptionType{script}

\newcommand{\leg}[1]{
    \begin{center}
    \textbf{Fonte: } #1.
    \end{center}
    \vspace{0.5cm}
}

\begin{document}

'''

# Definição do rodapé do documento
footer = '\n' + r'''\end{document}'''

# Definição do header de cada bloco de código
code_header = r'''
\begin{minted}[linenos]{'''


# Definição do rodapé de cada bloco de código
code_footer = r'''
\end{minted}
'''

def remove_prints_octave_matlab ( filename: str ):
    # abrindo arquivo a ser analisado
    file = open(filename + '.m', 'r')
    # arquivo temporário para armazenar versão
    # modificada do arquivo original
    file_cache = open(filename + '_tmpcache.m', 'w')
    # string para template de saída
    output = ''
    for line in file:
        # adiciona à string de saída toda linha que 
        # não contém o comando print
        if 'print(' not in line:
            output += line  
    # escreve no arquivo provisório de saída
    file_cache.write(output)

def search ( extension: str, data ):
    """
    Busca no arquivo 'data' passado por parâmetros,
    pelo nome da linguagem que contém a extensão pas-
    sada.
    """

    for entry in data:
        try: 
            if extension in entry['extensions']: return(entry["name"])
        except KeyError: pass
    return None

def find_language_name ( extension: str ) :
    """
    Procura o nome da linguagem a partir da extensão do
    arquivo passado por parâmetro.
    """

    # Abre json com as linguagens e suas extensões
    languages = json.load(open('lang.json', 'r'))['languages']

    # Returna o resultado da busca pela extensão
    return search(extension, languages)


def filter_files ( lista ) :
    """
    Função para filtrar arquivos a partir de uma lista 
    passada por parâmetros. O retorno é uma lista de no-
    mes de arquivos que contém apenas nomes com exten-
    sões contidas na estrutura 'including_names'
    """

    # Vetor de nomes a ser retornado
    final = []

    # Itera sobre os nomes incluídos
    for i in including_names:
        # Compila a expressão regular correspondente
        regex = re.compile(i)
        # Itera sobre os caminhos da lista passada
        for l in lista: 
            # Se o arquivo contém a extensão atual,
            # adiciona ao vetor de nomes a ser retor-
            # nado.
            if regex.match(l):
                final.append(l)   
    return final


def generate_latex_code ( template: str ):
    """
    Gera um arquivo latex com o template passado por parametro
    e salva na pasta saída
    """

    # Abre o arquivo onde será gravado
    file_out = open('saida/saida' + datetime.timestamp(datetime.now()).__str__() + '.tex' , 'w')
    
    # Escreve o arquivo
    file_out.write(template)


def execute ():
    """
    Função que faz o carregamento dos arquivos e gera o template
    para gerar no final, o arquivo latex básico.
    """

    # Array que será carregado com os caminhos para os arquivos 
    # que irão ser carregados.
    files_to_use = []

    # Itera sobre uma pasta, buscando nome das subpastas e nome
    # dos arquivos para que os mesmos sejam filtrados pela fun-
    # ção 'filter_files()'.
    for  (dirpath, dirnames, filenames) in os.walk('exercicios'):
        # Caso haja arquivos, verifica se os mesmos compreendem
        # arquivos com as extensões desejadas, e se sim, adicio-
        # nam os mesmos (com o caminho completo) ao array de ar-
        # quivos.
        if len(filenames) > 0:
            for file in filter_files(filenames):
                files_to_use.append(dirpath.__str__() + '/' + file)

    # Inicia o template com o header do documento
    template = header
    
    # Abre o arquivo com os dados do cabeçalho
    file = open('assets/inicio.tex', 'r')

    # Adiciona cada uma das linhas do cabeçalho no
    # template
    for line in file:
        template += line

    template += '\n'

    files_to_use.sort()

    # Variável que irá armazenar a questão atual para que
    # possamos gerar uma seção com seu número no latex:
    # - questao_atual = 1 irá gerar um látex com a seção
    #   \section{Exercício 1} 
    questao_atual = 0

    # Itera sobre os arquivos do array de arquivos filtrados
    for file_path in files_to_use:

        # Abre o arquivo corresposnde com função de leitura
        file_in = open(file_path, 'r')

        # Tenta uma busca pelo número da questão/exercício 
        # no nome do arquivo, exemplo:
        # - arquivo 'pasta_1/pasta_2/ex1/ex1.m' tem número 
        #   de exercício = 1
        numero_exercicio = re.search(r'(?<=\/[a-zA-Z]{2})([0-9]+)(?=\.m)', file_path)

        # Se a busca obtiver sucesso atualiza a variavel de
        # controle 'questao_atual' e agrega ao template o có-
        # digo para gerar a seção correspondente e a legenda
        # no latex.
        # 
        # Se a busca não obtiver sucesso, uma segunda busca 
        # irá ser testada. Essa tentativa representa os exer-
        # cícios com tópicos/letras:
        # - Nº1 letra a, nº2 letra b etc.

        # variavel para armazenar a questao atual
        questao_atual = 0

        if numero_exercicio:
            # Atualiza a questão atual
            questao_atual = numero_exercicio.group(0)
            # Adiciona seção correspondente ao template
            template += '\n' + r'''\section*{Exercício ''' + questao_atual + '}\n'
            # Adiciona legenda no bloco atual do template
            template += '\n' + r'''\captionof{script}{Script para execução do exercício ''' + questao_atual + r'''}\vspace{0.2cm}'''  + '\n'
           
        else:
            # Tenta encontrar o número do exercício com o se-
            # guinte padrão:
            # - arquivo 'pasta_1/pasta_2/ex1/ex1_a.m' tem número 
            #   de exercício = 1
            numero_exercicio = re.search(r'(?<=\/[a-zA-Z]{2})([0-9]{1})(?=\_[a-z]\.m)', file_path)

            # Se a busca for bem sucedida:
            if numero_exercicio:
                # Compara se o número encontrado é diferente da 
                # questão atual
                if numero_exercicio.group(0) != questao_atual:
                    # Atualiza a questão atual com o novo número
                    questao_atual = numero_exercicio.group(0)
                    # Gera uma seção nova com o nome da questão atual
                    template += '\n\n' + r'''\section*{Exercício ''' + questao_atual + '}\n'

                # Tenta uma busca pela letra/tópico do exercício:
                # - arquivo 'pasta_1/pasta_2/ex1/ex1_a.m' tem letra 
                #   de exercício = a
                letra_exercicio = re.search(r'(?<=\/[a-zA-Z]{2}[0-9]{1}\_)([a-z]+)(?=\.m)', file_path)

                # Caso a busca seja bem sucedida
                if letra_exercicio:
                    # Gera uma subseção para o tópico/letra encontra-
                    # dos na busca
                    template += r'''\subsection*{Letra ''' + letra_exercicio.group(0) + '}\n'

                # Adiciona a legenda do código no bloco atual do template
                template += '\n' + r'''\captionof{script}{Script para execução do exercício ''' + questao_atual + r''' letra ''' + letra_exercicio.group(0) + r'''}\vspace{0.2cm}''' + '\n'

        # Busca a extensão do arquivo.
        extensao = re.search(r'(\.[^.]+)$', file_path)

        # Caso a busca seja bem sucedida.
        if extensao:
            # Adiciona ao template o cabeçalho de bloco de código e a lin-
            # guagem buscada a partir da extensão do arquivo.
            template += code_header + find_language_name(extensao.group(0)) + '}\n'

        # Para cada linha do arquivo contendo o código do arquivo
        # adiciona a mesma ao template,
        for line in file_in:
            template += line

        # Adiciona o rodapé de código no template
        template += code_footer

        # Adiciona subseção para saída do script
        template += '\n' + r'''\subsection*{Saída do exercício ''' + questao_atual + '}\n'
        # Adiciona abertura de verbatim para saída do comando
        template += '\n' + r'''\begin{small}''' + '\n' + r'''\begin{verbatim}''' + '\n'

        if extensao.group(0) == '.m':
            try:
                # removendo print() do arquivo .m (dispara uma exceção no python)
                script_execution_output = remove_prints_octave_matlab('exercicios/ex' + questao_atual + '/ex' + questao_atual)
                # adiciona saída do programa gerada a partir da execução do script no terminal
                # do sistema operacional
                template += str(subprocess.check_output([ 'octave', 'exercicios/ex' + questao_atual + '/ex' + questao_atual + '_tmpcache.m' ], universal_newlines=True)) 
                # remove arquivo de cache
                subprocess.check_output([ 'rm', 'exercicios/ex' + questao_atual + '/ex' + questao_atual + '_tmpcache.m' ])
            except:
                print('[ warning ] : Problema na execução do script exercicios/ex' + questao_atual + '/ex' + questao_atual + '.m')
        
        # Adiciona fechamento de verbatim para saída do comando
        template += r'''\end{verbatim}''' + '\n' + r'''\end{small}''' + '\n'
        # Adiciona a fonte do código como autores
        template += '\n' + r'''\leg{autores}''' + '\n'

    # Adiciona o rodapé do documento ao template
    template += footer

    # Gera e salva o código latex do template gerado anteriormente
    generate_latex_code(template)

def main():
    """
    Cria um parser de argumentos para receber as extensões de ar-
    quivos a ser processadas, e chama a função para gerar o latex.
    """

    # Cria o parser de argumentos
    parser = argparse.ArgumentParser(description='Gerador de relatórios')

    # Adiciona um tipo de argumento para receber as extensões.
    parser.add_argument('-e', help='extensões aceitáveis', nargs='+', action='append')

    if parser.parse_args().e:
        # Filtra as extensões.
        extensions = list(map(lambda x: '.' + x if '.' not in x else x, parser.parse_args().e[0]))

        # Adiciona o regex aos nomes inclusos para cada extensão
        # obtida via parâmetro.
        for i in extensions:
            including_names.append('.+\\' + i + '$')

        execute()   

if __name__ == "__main__":
    main()