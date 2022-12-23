# Computacao 1 - 2022-1
# Correcao automatica da lista de exercicios 8


import sys
import importlib
import lista8gabarito
import os


# O import abaixo deve ser feito somente para listas em que os alunos
# precisam usar a funcao input.
from funcoesParaListaComInteracao import chamarFuncaoComStd,\
                                         criarArquivosGabarito,\
                                         escreverArquivoSaidaCompleto,\
                                         testarEntradasInteracao


###########################################################
# Colocar o numero da lista abaixo:
nLista = 8
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
questoesComLetra ={}
###########################################################

###########################################################
# A variavel testar deve ser True se desejamos testar as
# entradas que serao utilizadas com o gabarito:
testar = False
###########################################################

###########################################################
# A variavel testarCorrigir deve ser True se desejamos 
# testar a funcao de corrigir:
testarCorrigir = True
###########################################################

###########################################################
# A variavel funcoesComInteracao deve ser uma lista vazia 
# se a lista de exercicios nao tiver iteracao, ou uma lista
# com o numero das questoes que contem interacao
funcoesComInteracao = [4]
###########################################################

###########################################################
# Criando o arquivo com os nomes dos alunos:
if nLista == 1:
    from criarListaNomes import criarArqNomes
    criarArqNomes('nomesAlunos.txt','alunos.txt')
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
            ([1,2,2,2,8.9], "A"), \

            ([2,2,2,2],), \

            ([3,4,10,32,1,0], "G"), \

            ([1,2,3,4], "H"), \

            ([0,0,0],"M"), \

            ([3],"G"), \

            )
    elif questao == 2:
        return (

            ([1,2,3],[3,3,2]), \

            ([1,2,3],[1,2,"a"]), \

            ([3,4,6],[3,3,3,3]), \

            ([1,23,4],[1,1]), \

            ([1,2,3],[1,2,2,"a"]),\

            )
    elif questao == 3:
        return (

            ("temp1.txt",), \

            ("temp2.txt",), \

            ("temp3.txt",), \

            ("temp4.txt",), \

        )

    elif questao == 4:
        return ("questao4t1.txt",\
                "questao4t2.txt",\
                "questao4t3.txt",\
                "questao4t4.txt")

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
                funcao = getattr(lista8gabarito, 'questao%i'%questao)
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
                    funcao = getattr(lista8gabarito, 'questao%i%s'%(questao,letra))
                    for teste in testesLetra:
                        gabarito = funcao(*teste)
                        print(gabarito)
                    print('---------------')
                    inicio = fim
                    fim = fim + len(testes)//len(questoesComLetra[questao])
        else:
            funcao = getattr(lista8gabarito, 'questao%i'%questao)
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

                gabarito = lista8gabarito.questao1(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta or abs(gabarito-resposta) < 0.01:
                    casos.append(10)
                else:
                    erros.append(teste)
                    
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

                gabarito = lista8gabarito.questao2(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta:
                    casos.append(10)
                else:
                    erros.append(teste)
                    
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

                gabarito = lista8gabarito.questao3(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta:
                    casos.append(10)
                else:
                    erros.append(teste)
                    
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

            bkpIn = sys.stdin

            bkpOut = sys.stdout

            # Cada teste eh o nome de um arquivo com as
            # entradas do input.
            testes = gerarEntradas(questao)

            n = 1
            for teste in testes:
                # Nas funcoes com interacao, o arquivo com o gabarito nao eh
                # executado aqui. Por outro lado, ha um arquivo de texto
                # com tudo o que foi impresso na tela durante a execucao do
                # gabarito; e ha uma variavel com os valores de retorno.
                # A saida do gabarito estah salva no arquivo texto 
                # cujo nome eh definido abaixo.
                nomeOutGabarito = './SaidaInteracao/q4lista8gabarito'+str(n)+'.txt'
                # O valor de retorno do gabarito estah salvo na variável abaixo.
                gabarito = gabaritosComInteracao[0][n-1]
                # O arquivo de teste eh usado no lugar do input.
                sys.stdin = open(teste,'r')

                # Tudo o que for impresso na tela eh salvo em um arquivo txt
                nomeOut = './SaidaInteracao/q4'+nomeLista+str(n)+'.txt'
                n = n+1
                sys.stdout = open(nomeOut,'w')

                # A funcao do aluno eh executada e variavel resposta
                # guarda o valor de retorno.
                resposta = questoes[questao-1]()

                ########
                # Stdin e stdout voltam aos valores padrao:
                sys.stdout.close()
                sys.stdout = bkpOut

                sys.stdin.close()
                sys.stdin = bkpIn
                ########

                ########
                # Tudo o que foi escrito na tela tanto para o gabarito
                # quanto para a funcao do aluno sao lidos aqui.
                arqGabarito = open(nomeOutGabarito,'r')
                textoGabarito = arqGabarito.read()
                arqGabarito.close()

                arq = open(nomeOut,'r')
                texto = arq.read()
                arq.close()
                
                #####################################################################
                # Caracteres especiais sao retirados do que foi escrito na
                # execucao do gabarito e da funcao do aluno.
                textoGabarito = retirarCaracteresEspeciais(textoGabarito)
                texto = retirarCaracteresEspeciais(texto)

                #if texto[-1] != '.':
                #    texto = texto+'.'
                #if texto[-2] != 'm':
                #    texto = texto[:-1]+'m'+'.'
                # print(texto)
                #####################################################################
                
                notaq4 = 0
                
                # Prints para comparacao:
                #print('------------------------')
                #print(n)
                #print(nomeLista)
                #print(gabarito)
                #print(resposta)
                #print(gabarito == resposta)
                #print('------------------------')

                
                # Verifica se os valores de retorno sao iguais
                if gabarito == resposta:
                    #print(teste)
                    notaq4 = 8
                else:
                    #print(resposta)
                    #print(gabarito)
                    #print(teste)
                    #input()
                    
                    # Se nao forem iguais, verifica par a par.
                    # Esse else ajuda se o aluno retornou os valores
                    # certos, mas o tipo de dado estah incorreto.
                    
                    #print(gabarito)
                    #print(resposta)
                    try:
                        # Ordena
                        gabarito = sorted(gabarito)
                        resposta = sorted(resposta)
                        # Cria pares com cada tupla interna de
                        # gabarito e de resposta.
                        juntos = zip(gabarito,resposta)
                        contador = 0
                        for solucoes in juntos:
                            if solucoes[0][0] == solucoes[1][0]  and\
                               solucoes[0][1] == solucoes[1][1]:
                                contador += 1
                        if contador == len(gabarito):
                            notaq4 = 3
                    except:
                        if resposta == None: # Entra nesse if se o aluno esqueceu o return.
                            print('Erro None')

                # Verifica se o que foi impresso na tela eh
                # igual para o gabarito e para a funcao do aluno.
                # Como a parte de formacao de string nessa parte da lista
                # era tranquila, eu coloquei só 2 pontos para o texto.
                if texto == textoGabarito:
                    notaq4 = notaq4+2
                else:
                    # Esse else existe só para teste.
                    pass
                    #print (texto)
                    #print (textoGabarito)
                    
                if notaq4!=0:
                    casos.append(notaq4)
                    if notaq4!=10:
                        erros.append(teste)
                else:
                    erros.append(teste)

            escreverArquivoSaidaCompleto('./SaidaInteracao/q4',nomeLista,len(testes))

            notas[questao-1] = round(sum(casos)/len(testes),2)
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            '''
            for teste in testes:

                gabarito = lista6gabarito.questao4(*teste)
                resposta = questoes[questao-1](*teste)
                
                if  gabarito == resposta:
                    casos.append(10)
                else:
                    erros.append(teste)
            notas[questao-1] = round(sum(casos)/len(testes),2)
            errosQuestoes[questao-1] = tuple(erros)
            questao = questao+1
            '''
            
        except:
            if sys.stdin != bkpIn:
                sys.stdin.close()
                sys.stdin = bkpIn

            if sys.stdout != bkpOut:
                sys.stdout.close()
                sys.stdout = bkpOut
            print('------------------------------------------')
            print('Questao 4')
            if type(questoes[questao-1]) == list:
                if 0 in questoes[questao-1]:
                    print('Funcao nao encontrada!')
            elif questoes[questao-1] == 0:
                print('Funcao nao encontrada!')
            else:
                print(sys.exc_info())
            print('------------------------------------------')
            notas[questao-1] = round(sum(casos)/len(testes),2)
            erros.append(teste)
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

def criarGabaritosDeFuncoesComInteracao(questoes):
    '''Funcao utilizada somente em listas que possuem
    interacao com o usuario (input). questoes deve ser do
    tipo lista e deve conter os numeros das funcoes
    com interacao'''
    
    respostas = []
    for questao in questoes:
        testes = gerarEntradas(questao)
        funcao = getattr(lista8gabarito, 'questao%i'%questao)
        path = './SaidaInteracao/q%ilista8gabarito'%questao
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
    gabaritosInteracao = criarGabaritosDeFuncoesComInteracao(funcoesComInteracao)

############################################################
# Testes
if testar:
    testarEntradas(nQuestoes,questoesComLetra,funcoesComInteracao)

if testarCorrigir:
    arquivos = ['lista8teste']

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
        arqErros.write(nomeCodigo+'\n')

        # Escreve cada erro acompanhado do numero da questao
        for questao,erro in enumerate(erros):
            # Se o aluno nao errou a questao, pula a linha da escrita
            # Logo, se o aluno nao cometeu erros, somente a linha com
            # o nome do arquivo dele serah escrita.
            if erro == -1 or erro == ():
                continue
            arqErros.write('Questao '+str(questao+1)+ ' '+str(erro)+'\n')
        
        arqErros.write('\n')
        
    print(nomeCodigo,n, nota)
arqNotas.close()
arqErros.close()
  
