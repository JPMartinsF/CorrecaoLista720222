def criarArqNomes(arqEntrada,arqSaida):
    f = open(arqEntrada,'r')

    linha = f.readline()
    texto = ''

    while linha != '':
        pEspacoAntesNome = linha.find(' ')
        linha = linha[pEspacoAntesNome+1:]
        pDRE = linha.find('1')
        linha = linha[:pDRE-1]
        texto = texto+linha+'\n'
        linha = f.readline()

    f.close()

    f2 = open(arqSaida,'w')
    f2.write(texto)
    f2.close()
