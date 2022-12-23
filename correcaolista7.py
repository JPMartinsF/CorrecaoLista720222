# Computacao 1 - 2022-2
# Correcao automatica da lista de exercicios 1


import sys
import importlib
import lista7gabarito
import os


# O import abaixo deve ser feito somente para listas em que os alunos
# precisam usar a funcao input.
#from funcoesParaListaComInteracao import chamarFuncaoComStd,\
#                                         criarArquivosGabarito,\
#                                         escreverArquivoSaidaCompleto,\
#                                         testarEntradasInteracao


###########################################################
# Colocar o numero da lista abaixo:
nLista = 6
###########################################################

###########################################################
# Se a lista for dividida em duas partes, indique a parte
# na variavel abaixo, por exemplo 'p1' ou 'p2', se nao,
# a variavel parte deve ser uma string vazia:
parte = ''
###########################################################

###########################################################
# Colocar o numero de questoes abaixo:
nQuestoes = 4
questoesComLetra ={4:['a', 'b']}
###########################################################

###########################################################
# A variavel testar deve ser True se desejamos testar as
# entradas que serao utilizadas com o gabarito:
testar = False
###########################################################

###########################################################
# A variavel testarCorrigir deve ser True se desejamos 
# testar a funcao de corrigir:
testarCorrigir = False
###########################################################

###########################################################
# A variavel funcoesComInteracao deve ser uma lista vazia 
# se a lista de exercicios nao tiver iteracao, ou uma lista
# com o numero das questoes que contem interacao
funcoesComInteracao = []
###########################################################

###########################################################
# Criando o arquivo com os nomes dos alunos:
if nLista == 1:
    from criarListaNomes import criarArqNomes
    # Ordem dos argumentos: arq Entrada, arq saida,
    # O arquivo de entrada eh o arquivo que vem da
    # pauta, com DRE e numero e o arquivo de saida
    # eh o arquivo com somente nomes dos alunos
    # (sem numeros)
    criarArqNomes('alunos.txt','nomesAlunos.txt')
###########################################################


###########################################################
# Funcoes usadas em todas as listas

def criarStrings(numLista,parte=''):
    '''Utiliza o conteudo de nomesAlunos para gerar uma lista de
    strings com os nomes dos arquivos no padrao que os alunos
    devem mandar.'''
    
    alunos = open('nomesAlunos.txt','r')

    aluno = alunos.readline()
    arquivos = []
    
    while aluno != '':

        aluno = aluno.lower()
        aluno.replace('á','a')
        aluno.replace('ã','a')
        aluno.replace('é','e')
        aluno.replace('í','i')
        aluno.replace('ó','o')
        aluno.replace('õ','o')
        aluno.replace('ú','u')


        espaco = []
        n=0
        while n < len(aluno):
            letra = aluno[n]
            if letra == ' ':
                espaco.append(n)
            n = n+1
            
        arquivo = 'lista'+str(numLista)+parte+\
                  aluno[:espaco[0]]+aluno[espaco[-1]+1:-1]
        arquivos.append(arquivo)
        
        aluno = alunos.readline()

    alunos.close()
    arquivos.sort()
    return arquivos

def encontrarArquivosMesmoAluno(nomesListasAlunos,nomeDesejado):
    '''Recebe uma lista de nomes de arquivos e um nome desejado
    e retorna uma lista com os nomes dos arquivos que contem
    o nomeDesejado, retirando o .py e um possivel numero
    entre parenteses, que pode ter sido incluido pelo pelo
    classroom. Considera que os nomes podem estar em
    minusculas ou maiusculas em padroes diferentes.'''
    
    nomesArquivos = []
    # Retiramos o .py do arquivo, pois listaNnomeDesejado
    # eh a parte do nome do arquivo que pode aparecer em
    # outros arquivos.
    if '.py' in nomeDesejado:
        p = nomeDesejado.index('.py')
        nomeDesejado = nomeDesejado[:p]
    # Pela mesma logica usada para retirar o .py, retiramos
    # a numeracao colocada pelo classroom
    if ' ' in nomeDesejado:
        p = nomeDesejado.index(' ')
        nomeDesejado = nomeDesejado[:p]

    # Passa por todos os nomes de arquivos da lista
    for nomeArquivo in nomesListasAlunos:
        # Utiliza o lower para o caso em que o aluno
        # fez o upload primeiro em letras maiusculas
        # e em seguida corrigiu.
        if nomeDesejado.lower() in nomeArquivo.lower():
            # Se a string listaNnomeDesejado for 
            # encontrada em alguma string da lista com
            # os nomes dos arquivos, essa string da
            # lista eh incluida na lista que serah
            # retornada.
            nomesArquivos.append(nomeArquivo)
    
    return nomesArquivos

def apagarArquivosVersoesAntigas(nomesListasAlunos):
    '''Essa funcao modifica os arquivos de uma pasta,
    apagando arquivos quando necessario. O objetivo
    eh identificar se a pasta contem mais de um arquivo
    do mesmo aluno e manter somente o arquivo mais
    recente. Recebe a lista de strings com nomes do
    arquivos, verifica se ha mais de um arquivo de um
    mesmo aluno, encontra o mais recente e apaga os
    demais. Retira os nomes apagados da lista. Retorna
    a lista com os nomes dos arquivos que nao foram
    apagados.'''
    
    i = 0
    # Cria uma copia para garantir que vamos passar por todos
    # os nomes, e nomesListasAlunos serah modificada
    nomesListasAlunosCopia = nomesListasAlunos[:]
    while i < len(nomesListasAlunosCopia):
        nomeAtual = nomesListasAlunosCopia[i]
        # Para cada nome, verificamos se ha outros arquivos do mesmo aluno
        # A funcao retorna uma lista com todos os nomes de arquivos que comecam
        # com listaNnomeAtual.
        arquivosMesmoAluno = encontrarArquivosMesmoAluno(nomesListasAlunos,nomeAtual)

        # Ha mais de um arquivo de um aluno se arquivosMesmoAluno possuir
        # mais de uma string.
        if len(arquivosMesmoAluno) > 1:
            # O primeiro nome eh considerado, a principio, como o
            # nome do arquivo mais recente
            nomeMaisRecente = arquivosMesmoAluno[0]
            # os.path.getmtime retorna o tempo da ultima modificacao
            # do arquivo. O arquivo com maior tempo eh o mais recente,
            # pois foi modificado depois. 
            tempMaisRecente = os.path.getmtime(nomeMaisRecente)
            for nome in arquivosMesmoAluno[1:]:
                temp = os.path.getmtime(nome)
                # Se tempMaisRecente < temp, entao encontramos um
                # arquivo mais recente.
                if tempMaisRecente < temp:
                    # O arquivo mais antigo eh apagado, retirado
                    # da lista e as variaveis sao sobrescritas
                    os.remove(nomeMaisRecente)
                    nomesListasAlunos.remove(nomeMaisRecente)
                    tempMaisRecente = temp
                    nomeMaisRecente = nome
                else:
                    # Se o arquivo nao for mais recente que
                    # aquele definido como mais recente, entao
                    # o arquivo mais antigo eh apagado, retirado
                    # da lista e as variaveis sao sobrescritas
                    os.remove(nome)
                    nomesListasAlunos.remove(nome)            
        i = i+1
      
    return nomesListasAlunos
                

def corrigirNomesArquivos():
    '''Funcao para corrgir possiveis erros nos nomes dos arquivos dos alunos
    como a utilizacao de letras maiusculas, de alguns caracteres especiais,
    de parenteses com um numero (por causa do google classroom)...'''
    
    arquivos = os.listdir('.')
    listasAlunos = [nome for nome in arquivos if (nome[:5].lower() == 'lista') and\
                                                 ('.py' in nome) and\
                                                 ('gabarito' not in nome)]

    listasAlunos = apagarArquivosVersoesAntigas(listasAlunos)
    
    # Corrigir o nome
    for listaAluno in listasAlunos:
        nomeNovo = ''
        if listaAluno != listaAluno.lower():
            os.rename(listaAluno,listaAluno.lower())
            nomeNovo = listaAluno.lower()
        if ' (' in listaAluno.lower():
            p = listaAluno.find(' (')
            nomeNovo = listaAluno.lower()[:p]+'.py'
            os.rename(listaAluno.lower(),nomeNovo)
        if ('í' in listaAluno.lower()) or ('á' in listaAluno.lower()) or\
           ('é' in listaAluno.lower()) or ('ê' in listaAluno.lower()) or\
           ('ã' in listaAluno.lower()) or\
           ('ç' in listaAluno.lower()):
            if nomeNovo == '':
                nomeNovo = listaAluno.lower()
            nomeAntigo = nomeNovo
            nomeNovo = nomeNovo.replace('á','a')
            nomeNovo = nomeNovo.replace('ã','a')
            nomeNovo = nomeNovo.replace('é','e')
            nomeNovo = nomeNovo.replace('ê','e')
            nomeNovo = nomeNovo.replace('í','i')
            nomeNovo = nomeNovo.replace('ç','c')
            os.rename(nomeAntigo,nomeNovo)
        if 'lista0' in listaAluno.lower():
            if nomeNovo == '':
                nomeNovo = listaAluno.lower()
            nomeAntigo = nomeNovo
            nomeNovo = nomeNovo[:len('lista')]+nomeNovo[len('lista')+1:]
            os.rename(nomeAntigo,nomeNovo)
            

def gerarEntradas(questao, nomeLista=''):
    '''Definicao das entradas de cada questao atraves de tuplas de
    tuplas. Cada tupla interna deve ter como o numero de elementos igual
    ao numero de argumentos.'''

    if questao == 1:
        return (
            (('Ladrão de Raios', 'Mar de Monstros'), ('Rick Riordan', 'Rick Riordan'), (344, 359), (2004, 2006),), \

            (('Harry Potter', 'Os Pilares da Terra', 'O Sobrinho do Mago', 'Eu, Robô', 'Sinais e Sistemas Lineares'),\
            ('J K Rowling', 'Ken Follett', 'C. S. Lewis', 'Issac Azimov', 'B. P Lathi'),\
            (223, 548, 234, 326, 853), (1997, 2006, 1955, 1950, 2006),), \

            (('Eu, Robô',), ('Isaac Azimov',), (326,), (1950,),), \

            (('Os Pilares da Terra', 'O Sobrinho do Mago', 'Sinais e Sistemas Lineares'),\
            ('Ken Follett', 'C. S. Lewis', 'B. P Lathi'),\
            (548, 234, 853), (2006, 1955, 2006),), \

            (('Os Pilares da Terra', 'O Sobrinho do Mago', 'Eu, Robô', 'Sinais e Sistemas Lineares'),\
            ('Ken Follett', 'C. S. Lewis', 'Issac Azimov', 'B. P Lathi'),\
            (548, 234, 326, 853), (2006, 1955, 1950, 2006),), \
            )

    elif questao == 2:
        return (

            ((71.0, 23.4, -33.4), (115.6, 103.1, 40.0), ('S1', 'S2', 'S2'), 'S1'),\

            ((14.6, 32.9, 61.2, 89.9, -10.0), (-125.5, -100.2, 82.1, 2.5, 169.9), ('S1', 'S2', 'S1', 'S2', "S3"), 'S1'),\

            ((-44.6, 30.1, -41.2, 48.9, 50.0), (15.3, -179.9, 179.9, 22.9, 9.9), ('S1', 'S2', 'S3', 'S4', "S3"), 'S5'),\
            
            ((46.6, 3.2, 6.1, -89.9, 89.9), (-15.5, 10.3, 8.4, 46.5, 19.3), ('S1', 'S2', 'S1', 'S2', "S2"), 'S2'),\
            
            ((11.5, 45.4), (110.2, -113.1), ('S1', 'S2'), 'S1')
            
            )
    elif questao == 3:
        return (

            ("Testando a funcao", "func", "quest"), \

            ("Testando a funcao", "Test", "Us"), \

            ("Ttttt", "ttt", "u"), \

            ("Gasolina esta cara", "cara", "barata"), \

            ("Gasolina esta cara", "Etanol", "GNV"), \

            ("Os Knicks nao sao bons", "nao", ""), \

            )

    elif questao == 4:
        return (
            #Questao 4a

            ((0,1,2,3),), \

            ((7,7,7),), \

            ((10,10,9,8,9,10),), \

            ((100,10,20,30),), \

            ((10,10,7.5,8,9,40,250),), \

            #Questao 4b

            (((0,1,2,3),(4,4,1,3),(10,3,8,9),(8,8,2,1)),), \

            (((0,1),(1,0),(1,1),(1,0)),), \

            (((10,10,13,15),),), \

            (((1,1,1), (3,1,5), (5,5,3)),), \

            (((5,3,7,90),(10,2,3,5),(100,5,9,12),(9,9,2,8)),), \

            )

    elif questao == 5:
        pass
    elif questao == 6:
        pass
    elif questao == 7:
        pass
    elif questao == 8:
        pass        
    elif questao == 9:
        pass
    elif questao == 10:
        pass

def testarEntradas(nQuestoes,questoesComLetra = {},questoesComInteracao=[]):
    '''Testa as entradas definidas em gerarEntradas utilizando o gabarito.'''
    
    for questao in range(1,nQuestoes+1):
        testes = gerarEntradas(questao)
        if questao not in questoesComInteracao:
            if questao not in questoesComLetra:
                print('---Questao %i---'%questao)
                funcao = getattr(lista7gabarito, 'questao%i'%questao)
                for teste in testes:
                    gabarito = funcao(*teste)
                    print(gabarito)
                print('---------------')
            else:
                inicio = 0
                fim = len(testes)//len(questoesComLetra[questao])
                for letra in questoesComLetra[questao]:
                    testesLetra = testes[inicio:fim]
                    print('---Questao %i%s--'%(questao,letra))
                    funcao = getattr(lista7gabarito, 'questao%i%s'%(questao,letra))
                    for teste in testesLetra:
                        gabarito = funcao(*teste)
                        print(gabarito)
                    print('---------------')
                    inicio = fim
                    fim = fim + len(testes)//len(questoesComLetra[questao])
        else:
            funcao = getattr(lista7gabarito, 'questao%i'%questao)
            for teste in testes:
                print('---------------')
                print('---Questao %i,%s---'%(questao,teste))
                testarEntradasInteracao(teste,funcao)
                print('---------------')
            
                

def definirListaFuncoes(listaExAluno, nQuestoes,questoesLetras = {}):
    '''Funcao que define uma lista de funcoes de acordo com o conteudo
    do arquivo do aluno. Para que uma funcao seja encontrada, ela deve
    possui como ultimo caractere do nome o numero da questao.'''
    
    listaAtributos = dir(listaExAluno)

    listaAtributosCopia = listaAtributos[:]

    questoes = [0]*nQuestoes

    for num in range(1,nQuestoes+1):
        if num not in questoesLetras:
            listaAtributosCopia = listaAtributos[:]
            for atributo in listaAtributosCopia:
                if atributo[-1] == str(num):
                    questoes[num-1] = getattr(listaExAluno, atributo)
                    listaAtributos.remove(atributo)
                    break
                elif '__' in atributo:
                    listaAtributos.remove(atributo)
        else:
            questoes[num-1] = [0]*len(questoesLetras[num])
            posLetra = 0
            for letra in questoesLetras[num]:
                listaAtributosCopia = listaAtributos[:]
                for atributo in listaAtributosCopia:
                    if atributo[-2:] == str(num)+letra:
                        questoes[num-1][posLetra] = getattr(listaExAluno, atributo)
                        posLetra = posLetra+1
                        listaAtributos.remove(atributo)
                        break
                    elif atributo[-2:] == str(num)+letra.upper():
                        questoes[num-1][posLetra] = getattr(listaExAluno, atributo)
                        posLetra = posLetra+1
                        listaAtributos.remove(atributo)
                        break
                    elif '__' in atributo:
                        listaAtributos.remove(atributo)
                
    return questoes
    
def retirarCaracteresEspeciais(string):
    '''Funcao usada para retirar os caracteres especiais de strings.
    Útil principalmente para as listas em que o print eh importante'''
    string = string.replace(' ','').lower()
    string = string.replace('\n','')
    string = string.replace(':','')
    string = string.replace(';','')
    string = string.replace(',','')
    string = string.replace('!','')
    string = string.replace('ç','c')
    string = string.replace('á','a')
    string = string.replace('à','a')
    string = string.replace('ã','a')
    string = string.replace('ê','e')
    string = string.replace('é','eh')
    string = string.replace('ú','u')
    
    return string


def corrigirLista(nomeLista,nQuestoes,questoesComLetra={},gabaritosComInteracao = []):
    '''Funcao que realiza a correcao automatica do arquivo cujo nome eh nomeLista.
    Recebe a quantidade de questoes para criar uma lista de notas com o tamanho
    certo. O dicionario questoesComLetra indica se ha mais de uma letra na questao
    e eh utilizado para dividir a correcao daquela questao em partes.
    gabaritosComInterecao eh uma lista de valores retornados em questoes com
    interacao ao usuario.'''
        
    try:
        lista = importlib.import_module(nomeLista)
    except ModuleNotFoundError:
        notas = [-1]*nQuestoes
        errosQuestoes = [-1]*nQuestoes
    except:
        notas = [-2]*nQuestoes
        errosQuestoes = [-2]*nQuestoes
    else:

        notas = [0]*nQuestoes
        errosQuestoes = [0]*nQuestoes

        # A funcao definirListaFuncoes retorna uma lista de
        # funcoes. O elemento da posicao [0] de questoes eh
        # aquele que deve ser utilizado para a chamada da
        # funcao da questao 1; o elemento da posicao [1] eh
        # aquele que deve ser utilizado para a chamada da
        # funcao da questao 2; e assim por diante...
        questoes = definirListaFuncoes(lista,nQuestoes,questoesComLetra)
        
        questao = 1
        
        try:
            casos = []
            erros = []

            # gerarEntradas retorna uma tupla com as
            # entradas que serao usadas para o teste
            testes = gerarEntradas(questao)
            
            for teste in testes:

                gabarito = lista7gabarito.questao1(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta or abs(gabarito-resposta) < 0.00001:
                    casos.append(10)
                else:
                    erros.append([teste,resposta,gabarito])
                    
            notas[questao-1] = round(sum(casos)/len(testes),2)
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
        except:
            print('------------------------------------------')
            print('Questao 1')
            if type(questoes[questao-1]) == list:
                if 0 in questoes[questao-1]:
                    print('Funcao nao encontrada!')
            elif questoes[questao-1] == 0:
                print('Funcao nao encontrada!')
            else:
                print(sys.exc_info()[0])
            print(nomeLista)
            print(teste)
            print('------------------------------------------')
            notas[questao-1] = round(sum(casos)/len(testes),2)
            erros.append((sys.exc_info()[0],teste))
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            
        try:
            casos = []
            erros = []

            # gerarEntradas retorna uma tupla com as
            # entradas que serao usadas para o teste
            testes = gerarEntradas(questao)
            
            for teste in testes:

                gabarito = lista7gabarito.questao2(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta or abs(gabarito-resposta) < 0.00001:
                    casos.append(10)
                else:
                    erros.append([teste,resposta,gabarito])
                    
            notas[questao-1] = round(sum(casos)/len(testes),2)
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
        except:
            print('------------------------------------------')
            print('Questao 2')
            if type(questoes[questao-1]) == list:
                if 0 in questoes[questao-1]:
                    print('Funcao nao encontrada!')
            elif questoes[questao-1] == 0:
                print('Funcao nao encontrada!')
            else:
                print(sys.exc_info()[0])
            print(nomeLista)
            print(teste)
            print('------------------------------------------')
            notas[questao-1] = round(sum(casos)/len(testes),2)
            erros.append((sys.exc_info()[0],teste))
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            
        try:
            casos = []
            erros = []

            # gerarEntradas retorna uma tupla com as
            # entradas que serao usadas para o teste
            testes = gerarEntradas(questao)
            
            for teste in testes:

                gabarito = lista7gabarito.questao3(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta or abs(gabarito-resposta) < 0.00001:
                    casos.append(10)
                else:
                    erros.append([teste,resposta,gabarito])
                    
            notas[questao-1] = round(sum(casos)/len(testes),2)
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
        except:
            print('------------------------------------------')
            print('Questao 3')
            if type(questoes[questao-1]) == list:
                if 0 in questoes[questao-1]:
                    print('Funcao nao encontrada!')
            elif questoes[questao-1] == 0:
                print('Funcao nao encontrada!')
            else:
                print(sys.exc_info()[0])
            print(nomeLista)
            print(teste)
            print('------------------------------------------')
            notas[questao-1] = round(sum(casos)/len(testes),2)
            erros.append((sys.exc_info()[0],teste))
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            
        try:
            casos = []
            erros = []
            
            testes = gerarEntradas(questao)

            # Mesmo numero de testes para cada letra.
            fimLetra = len(testes)//len(questoesComLetra[questao])            
                
            # Correcao: questao 4a   
            for teste in testes[:fimLetra]:
                gabarito = lista7gabarito.questao4a(*teste)
                resposta = questoes[questao-1][0](*teste)
                print("Gabarito/Resposta: ", gabarito, resposta)
                if  gabarito == resposta:
                    casos.append(10)
                else:
                    erros.append([teste, resposta, gabarito])
            nota4a = round(sum(casos)/len(testes[:fimLetra]),2)
            casos = []

            # Correcao: questao 4b
            for teste in testes[fimLetra:]:
                gabarito = lista7gabarito.questao4b(*teste)
                resposta = questoes[questao-1][1](*teste)
                                
                if  gabarito == resposta:
                    casos.append(10)
                else:
                    erros.append([teste, resposta, gabarito])
            nota4b = round(sum(casos)/len(testes[fimLetra:]),2)
            notas[questao-1] = round((0.4*nota4a+0.6*nota4b),2)
            
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            
        except:
            print('------------------------------------------')
            print('Questao 4')
            print(questoes)
            if type(questoes[questao-1]) == list:
                if 0 in questoes[questao-1]:
                    print('Funcao nao encontrada!')
            elif questoes[questao-1] == 0:
                print('Funcao nao encontrada!')
            else:
                print(sys.exc_info()[0])
            print(nomeLista)
            print(teste)
            print('------------------------------------------')
            notas[questao-1] = round(sum(casos)/len(testes),2)
            erros.append((sys.exc_info()[0],teste))
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1

    return notas,errosQuestoes


def notasManuais(notas,arquivo):
    '''Ajustes das notas se a correcao automatica estiver
    muito rigorosa ou se o aluno tiver usado alguma funcao
    ou metodo que nao eh permitido.'''
    
    n = notas[:]

    '''
    Exemplo: se você nao concordar com a nota de um aluno
    em um determinada questao, mude manualmente por aqui,
    atraves de uma condicional. A condição deve ser que
    a variavel 'arquivo' seja igual a string com o nome
    do arquivo .py do com codigo do aluno. Por exemplo:
    
    if arquivo == 'lista1gustavopires':
        n[7-1] = 9.0 # Preferencialmente, coloque um comentario
                     # breve para que voce lembre o motivo.
                     # Nesse exemplo, estou modificando a nota da questao 7
                     # o -1 eh soh para corrigir o indice da lista.                     
    elif arquivo == 'lista1ericrafaelpereira':
        n[2-1] = 7.0 # Nesse exemplo, estou modificando a nota da questao 2
                     # o -1 eh soh para corrigir o indice da lista.

    '''
        
    return n

def criarGabaritosDeFuncoesComInteracao(questoes,numLista):
    '''Funcao utilizada somente em listas que possuem
    interacao com o usuario (input). questoes deve ser do
    tipo lista e deve conter os numeros das funcoes
    com interacao'''
    
    respostas = []
    for questao in questoes:
        testes = gerarEntradas(questao)
        funcao = getattr(lista7gabarito, 'questao%i'%questao)
        path = './SaidaInteracao/q%ilista%igabarito'%(questao,numLista)
        respostas.append(criarArquivosGabarito(testes,path,funcao))
    return respostas

def calcularMedia(listaNotas,pesos):
    '''Calculo da media do aluno'''
    
    if sum(pesos) == len(pesos):
        # Media simples
        nota = round(sum(listaNotas)/(len(listaNotas)),2)
    else:
        # Media ponderada
        somatorio = 0
        denominador = 0
        for i in range(len(listaNotas)):
            somatorio += listaNotas[i]*pesos[i]
            denominador += pesos[i]

        nota = round(somatorio/denominador,2)
        
    return nota

###########################################################
# Criando uma lista de strings onde cada string eh o nome
# do arquivo de um aluno, segundo a padronizacao pedida.
arquivos = criarStrings(nLista,parte)
###########################################################

# Para testar uma lista especifica, coloque o nome
# do arquivo do Python abaixo, como nos exemplos:
# arquivos = ['lista1brunaduarte']
# arquivos = ['lista1gustavopires','lista1tiagooliveira']
# arquivos = ['lista1jhonatanleandro','lista1felippesilva']

arqNotas = open('notas.txt','w')
arqErros = open('erros.txt','w')
corrigirNomesArquivos()

###########################################################
# Criando os arquivos de gabarito:
if funcoesComInteracao != []:
    gabaritosInteracao = criarGabaritosDeFuncoesComInteracao(funcoesComInteracao,nLista)
else:
    gabaritosInteracao = []

############################################################
# Testes
if testar:
    testarEntradas(nQuestoes,questoesComLetra,funcoesComInteracao)

if testarCorrigir:
    arquivos = ['lista7teste']

###########################################################
# Rodando o teste para cada aluno:
for nomeCodigo in arquivos:
        
    
    n,erros = corrigirLista(nomeCodigo,nQuestoes,questoesComLetra,gabaritosInteracao)

    n = notasManuais(n,nomeCodigo)

    # Calculo da nota considerando que essa lista nao possui
    # nenhuma questão extra e que todas as notas possuem
    # mesmo peso. Como todos os pesos são iguais, a funcao
    # de calcular media recebe uma lista com numeros 1.
    nota = calcularMedia(n[:],[1]*(nQuestoes))
    if parte != '':
        nota = nota/2
    nota = round(nota,2)
    # Atualizacao do arquivo com totas as notas
    arqNotas.write(nomeCodigo+' '+str(n)+' '+str(nota)+'\n')


    #########################################################
    # Escrevendo o arquivo com erros:
    # Se o arquivo do aluno existe, erros serah diferente de
    # [-1]*nQuestoes. Neste caso, este aluno eh considerado 
    # no arquivo de erros: uma linha eh criada para ele.
    
    if erros != [-1]*nQuestoes:
        arqErros.write(nomeCodigo+' - '+str(nota)+'\n')
        print("Erros: ", erros)
        # Escreve cada erro acompanhado do numero da questao
        for questao,erro in enumerate(erros):
            # Se o aluno nao errou a questao, pula a linha da escrita
            # Logo, se o aluno nao cometeu erros, somente a linha com
            # o nome do arquivo dele e a nota serao escritos.
            if erro == -1 or erro == ():
                continue
            if erro == -2:
                arqErros.write('   Codigo com erros, nao foi possivel executa-lo.\n')
                break
            strEscrever = 'Questao '+str(questao+1)+'\n'
            for detalhe in erro:
                if type(detalhe) == tuple:
                    strEscrever += '   Ao tentar executar o codigo para a entrada '+\
                                   str(detalhe[1])+', o Python gerou o erro: '+\
                                   str(detalhe[0])+'\n'
                else:
                    strEscrever += '   Entrada: '+str(detalhe[0])+\
                                   '; Saída incorreta: '+str(detalhe[1])+\
                                   '; Saída correta: '+str(detalhe[2])+'\n'
            
            arqErros.write(strEscrever)
        
        arqErros.write('\n')
        
    print(nomeCodigo,n, nota)
arqNotas.close()
arqErros.close()
  
