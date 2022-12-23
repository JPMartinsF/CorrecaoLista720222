import sys
import os

###########################################################
# Funcoes usadas somente nas lista que contem interacao
# com o usuario
def chamarFuncaoComStd(funcao,argumentos,flagStdIn,flagStdOut,arqOut='stdout.txt',arqIn=''):
       
    if flagStdIn and flagStdOut:
        bkpIn = sys.stdin
        bkpOut = sys.stdout
        
        sys.stdin = open(arqIn,'r')
        try:
            sys.stdout = open(arqOut,'w')
        except FileNotFoundError:
            pathList = arqOut.split('/')
            os.mkdir(pathList[1])
            sys.stdout = open(arqOut,'w')

        try:
            gabarito = funcao(*argumentos)
        except:
            return None
        finally:
            sys.stdout.close()
            sys.stdout = bkpOut

            sys.stdin.close()
            sys.stdin = bkpIn
        
    elif flagStdOut:
        bkpOut = sys.stdout
        sys.stdout = open(arqOut,'w')
        try:
            gabarito = funcao(*argumentos)
        except:
            return None
        finally:
            sys.stdout.close()
            sys.stdout = bkpOut
        
    return gabarito

def criarArquivosGabarito(testes,nomeArquivo,questao):
    bkpIn = sys.stdin

    bkpOut = sys.stdout
    
    n = 1
    gabarito = []
    for teste in testes:
                        
        sys.stdin = open(teste,'r')
        nomeOutGabarito = nomeArquivo+str(n)+'.txt'
        try:
            sys.stdout = open(nomeOutGabarito,'w')
        except FileNotFoundError:
            pathList = nomeOutGabarito.split('/')
            os.mkdir(pathList[1])
            sys.stdout = open(nomeOutGabarito,'w')
        
        gabarito.append(questao())
        
        sys.stdout.close()
        
        sys.stdout = bkpOut

        sys.stdin.close()
        sys.stdin = bkpIn

        n = n+1

    escreverArquivoSaidaCompleto(nomeArquivo,'',len(testes))

    return gabarito[:]

def testarEntradasInteracao(teste,questao):
    bkpIn = sys.stdin
                        
    sys.stdin = open(teste,'r')

    questao()

    sys.stdin.close()
    sys.stdin = bkpIn


def escreverArquivoSaidaCompleto(nomeArquivo,nomeLista,nMax):
    
    for n in range(1,nMax+1):
                
            nomeOut = nomeArquivo+nomeLista+str(n)+'.txt'

                       
            arq = open(nomeOut,'r')
            texto = arq.read()
            arq.close()
            
            texto = texto.replace('á','a')

            
            nome = nomeArquivo+nomeLista+'.txt'

            if n == 1:
                try:
                    arq = open(nome,'w')
                except FileNotFoundError:
                    pathList = nome.split('/')
                    os.mkdir(pathList[1])
                    sys.stdout = open(nome,'w')
            else:
                arq = open(nome,'a')
            arq.write(texto)
            arq.write('\n\n\n\n')
            arq.close()
    return 0
              
