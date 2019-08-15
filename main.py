# Importação da biblioteca de interface com o SO
import os

# Importação de biblioteca de expressões regulares
import re

# Regex de nomes de arquivos que devem ser incluídos
including_names = {
    '.+\.m'
}

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
footer = r'''\end{document}'''

# Definição do header de cada bloco de código
code_header = r'''
\begin{minted}[linenos]{Matlab}
'''
# Definição do rodapé de cada bloco de código
code_footer = r'''
\end{minted}
'''


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
    file_out = open('saida/teste.tex' , 'w')
    
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
        if numero_exercicio:
            # Atualiza a questão atual
            questao_atual = numero_exercicio.group(0)
            # Adiciona seção correspondente ao template
            template += r'''\section*{Exercício ''' + questao_atual + '}\n'
            # Adiciona legenda no bloco atual do template
            template += r'''\captionof{script}{Script para execução do exercício ''' + questao_atual + r'''}\vspace{0.2cm}'''  + '\n'
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
                    template += r'''\section*{Exercício ''' + questao_atual + '}\n'

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
                template += r'''\captionof{script}{Script para execução do exercício ''' + questao_atual + r''' letra ''' + letra_exercicio.group(0) + r'''}\vspace{0.2cm}''' + '\n'

        # Adiciona ao template o cabeçalho de bloco de código
        template += code_header

        # Para cada linha do arquivo contendo o código do arquivo
        # adiciona a mesma ao template,
        for line in file_in:
            template += line

        # Adiciona o rodapé de código no template
        template += code_footer

        # Adiciona a fonte do código como autores
        template += r'''\leg{autores}''' + '\n'

    # Adiciona o rodapé do documento ao template
    template += footer

    # Gera e salva o código latex do template gerado anteriormente
    generate_latex_code(template)


def main():
    execute()   


if __name__ == "__main__":
    main()