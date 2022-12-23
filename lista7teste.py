# Computacao I - 2022.2
# Gabarito da lista de exercicios 7

# Funcao auxiliar para imprimir menu de opcoes
def imprimirMenu():
    print('1 - Inserir um ou mais cliente(s)')
    print('2 - Mostrar a lista de clientes')
    print('3 - Listar clientes de uma especie')
    print('4 - Listar animais de um cliente')
    print('5 - Remover um ou mais cliente(s)')
    print('6 - Sair')
    op = input('Digite uma opcao: ')
    return op

# OP1 - inserir clientes
def inserirCliente(clientesAtuais):
    sair = ''
    while sair != 'n':
        dono = input('Digite o nome do cliente: ')
        animal = input('Digite o nome do animal: ')
        especie = input('Digite a especie do animal: ')
        idade = int(input('Digite a idade do animal (anos): '))
        peso = float(input('Digite o peso do animal (kg): '))
        clientesAtuais = clientesAtuais + ((dono,animal,especie,idade,peso),)
        sair = input('Deseja inserir outro cliente?(s/n) ')
    return clientesAtuais

# OP2 - listar clientes
def listarClientes(listaClientes):
    if len(listaClientes) == 0:
        print('Nao ha clientes cadastrados.')
    else:
        for cliente in listaClientes:
            print('Dono: %s ; Animal: %s ; Especie: %s ; Idade: %d ano(s) ; Peso: %.2f kg'\
                  %(cliente[0],cliente[1],cliente[2],cliente[3],cliente[4]))

# OP3 - listar clientes por especie de animal
def listarClientesPorEspecie(listaClientes):
    if len(listaClientes) == 0:
        print('Nao ha clientes cadastrados')
    else:
        especie = input('Digite a especie que deseja procurar: ')
        especieNaoEncontrada = True
        for cliente in listaClientes:
            if especie.lower() == cliente[2].lower():
                print('Cliente: %s ; Animal: %s ; Idade: %d ano(s) ; Peso: %.2f kg'\
                      %(cliente[0],cliente[1],cliente[3],cliente[4]))
                especieNaoEncontrada = False
        if especieNaoEncontrada:
            print('Especie nao encontrada.')
            
# OP4 - listar animais de um cliente
def listarAnimaisPorDono(listaClientes):
    dono = input('Digite o nome do cliente: ')
    clienteNaoEncontrado = True
    for cliente in listaClientes:
        if dono.lower() == cliente[0].lower():
            print('Animal: %s ; Especie: %s ; Idade: %d ano(s) ; Peso: %.2f kg'\
                  %(cliente[1],cliente[2],cliente[3],cliente[4]))
            clienteNaoEncontrado = False
    if clienteNaoEncontrado:
        print('Cliente nao encontrado.')

# OP5 - remover clientes
def removerClientes(listaClientes):
    buscar = 's'
    while buscar == 's':
        clientesEncontrados = ()
        dono = input('Digite o nome do cliente: ')
        for idx in range(len(listaClientes)):
            if dono.lower() == listaClientes[idx][0].lower():
                clientesEncontrados += ((idx,listaClientes[idx][0],listaClientes[idx][1],listaClientes[idx][2],\
                                         listaClientes[idx][3],listaClientes[idx][4]),)
        if len(clientesEncontrados) == 0:
            print('Cliente nao encontrado.')
            buscar = 'n'
        else:
            print('%d cliente(s) encontrados.' % len(clientesEncontrados))
            resp = ''
            for cliente in clientesEncontrados:
                print('Cliente: %s ; Animal: %s ; Especie: %s ; Idade: %d ano(s) ; Peso: %.2f kg'\
                  %(cliente[1],cliente[2],cliente[3],cliente[4],cliente[5]))
                resp = input('Deseja excluir este cliente?(s/n) ')
                if resp.lower() == 's':
                    listaClientes = listaClientes[:cliente[0]]+listaClientes[cliente[0]+1:]
                    break
            buscar = input('Deseja excluir outro cliente?(s/n) ')
    return listaClientes

# Funcao principal
def main1():
    clientes = ()
    while True:
        opcao = imprimirMenu()
        if opcao == '1':
            clientes = inserirCliente(clientes)
        elif opcao == '2':
            listarClientes(clientes)
        elif opcao == '3':
            listarClientesPorEspecie(clientes)
        elif opcao == '4':
            listarAnimaisPorDono(clientes)
        elif opcao == '5':
            clientes = removerClientes(clientes)
        elif opcao == '6':
            break
    return clientes

if __name__=='__main__':
    print(main1())
