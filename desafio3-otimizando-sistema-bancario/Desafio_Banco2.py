def entrar(usuario):
    cpf = input("Informe o CPF do usuário: ")

    if cpf in usuario:
        conta = input("Informe o número da conta: ")
        if conta in usuario[cpf]["contas"]:
            global menu 
            menu = 2
            print(f"Bem vindo {usuario[cpf]["nome"]}. Você entrou na sua conta")
            return usuario[cpf]["contas"][conta]
        else:
            print("Não existe uma conta com esse número vinculada a este usuário.")
    else:
        print("Usuário não encontrado. Favor informar o CPF de um cliente deste banco")
        return 0

def criar_usuario(usuario):
    nome = input("Informe o nome do usuário: ")
    
    nascimento = input("Informe data de nascimento(dd-mm-aa): ")
    if (len(nascimento) == 8) and (nascimento[2] == nascimento[5] == "-"):
        if (int(nascimento[:2]) <= 31) and (int(nascimento[3:5]) <= 12) and (int(nascimento[6:]) < 100):
            True
        else:
            print("data inválida")
            return
    else:
        print("data inválida")
        return
    
    telefone = input("Informe telefone de contato: ")
    if (8 <= len(telefone) <= 9) and telefone.isdigit():
        True
    else:
        return
    
    logradouro = input("Informe endereço de residência: ")

    cpf = input("Informe o CPF do usuário: ")
    if (len(cpf) == 11) and cpf.isdigit():
        if cpf in usuario:
            print("Usuário já possui cadastro nesse banco")
            return
        else:
            usuario.update({cpf: {"nome": nome, "nascimento": nascimento, "telefone": telefone, "Endereço": logradouro, "contas": ''}})
            print(f"\nCadastro de {usuario[cpf]["nome"]} realizado com sucesso!")
            return usuario[cpf]
    else:
        print("CPF inválido. Por favor, forneca um CPF válido")

def criar_conta(usuario):
    cpf = input("Informe o CPF do usuário: ")
    if cpf in usuario:
        True
    else:
        print("Usuário não encontrado. É preciso criar um cadastro primeiro.")
        return
    
    if len(usuario[cpf]["contas"]) == 0:
        usuario[cpf]["contas"] = {"1": {"saldo": 0, "limite": 500, "limite_saques": 3, "numero_saques": 0, "extrato": ""}}
        print(f"conta {1:04d} criada com sucesso.")
    else:
        x = max(usuario[cpf]["contas"].keys(), key=int)
        numero_conta = int(x) + 1
        usuario[cpf]["contas"].update({str(numero_conta): {"saldo": 0, "limite": 500, "limite_saques": 3, "numero_saques": 0, "extrato": ""}})
        print(f"Conta {numero_conta:04d} criada com sucesso.")


def deletar_conta(usuario):
    cpf = input("Informe o CPF do usuário: ")
    
    if cpf in usuario:
        conta = input("Informe o número da conta que deseja cancelar: ")

        if conta in usuario[cpf]["contas"]:
            if usuario[cpf]["contas"][conta]["saldo"] > 0:
                print("Não é possivel cancelar uma conta que possui saldo.")
            else:
                usuario[cpf]["contas"].pop(conta)
                print(f"Conta {int(conta):04d} cacelada com sucesso.")
        else:
            print("Esse usuário não possui uma conta com esse número. Favor informar uma conta válida")

    else:
        print("Não encontramos o usuário em nossa lista de clientes. Favor informar o CPF de um cliente deste banco")


def sacar(*, saldo, limite, limite_saques, numero_saques, extrato):
    valor = float(input("Informe o valor do saque: "))
    
    if valor > saldo: #Testa se tem saldo suficiente
        print("Você não tem saldo suficiente para essa operação.")

    elif valor > limite: #Testa o valor limite da operação
        print("O valor informado excede o limite para essa operação.")

    elif numero_saques >= limite_saques: #Testa a quantidade de operações executadas
        print("Você excedeu o número máximo de operações de saques.")

    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"    Saque:    -R$ {valor:.2f}\n"
        return True, saldo, numero_saques, extrato
    else:
        print("Falhou! Por favor, informe um valor válido.")
    
    return False, 0

def depositar(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))
                  
    if valor > 0: #Testa se o valor informado é válido
        saldo += valor
        extrato += f"    Depósito: +R$ {valor:.2f}\n"
        return True, saldo, extrato
    else:
        return False, 0

def extrato(saldo, /, *, extrato ):
    print("\n================ EXTRATO ================")
    print("   Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n    Saldo:     R$ {saldo}")
    print("==========================================")

def menu1():
    opcao = input(menu_usuario)

    if opcao == "1":
        #print("Entrar")
        return entrar(usuario)
    elif opcao == "2":
        #print("Usuario")
        criar_usuario(usuario)
    elif opcao == "3":
        print("Conta")
        criar_conta(usuario)
    elif opcao == "4":
        print("Deletar")
        deletar_conta(usuario)
    elif opcao == 0:
        print("Volte sempre. Obrigado por escolher nossos serviços.")
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    
    return 0

def menu2(conta):
    opcao = input(menu_conta)

    if opcao == "1":
        resposta = depositar(conta["saldo"], conta["extrato"])
        if resposta[0]:
            conta.update({"saldo":  resposta[1]})
            conta.update({"extrato": resposta[2]})
            print(f"Depósito realizado com sucesso\n")

        else:
            print("Falhou! Por favor, informe um valor válido.")

    elif opcao == "2":
        resposta = sacar(saldo = conta["saldo"], limite = conta["limite"], limite_saques = conta["limite_saques"], numero_saques = conta["numero_saques"], extrato = conta["extrato"])
        if resposta[0]:
            conta["saldo"] = resposta[1]
            conta["numero_saques"] = resposta[2]
            conta["extrato"] = resposta[3]
            print(f"Saque realizado com sucesso\n")

        else:
            #print("Falhou! Por favor, informe um valor válido.")
            return


    elif opcao == "3":
        extrato(conta["saldo"], extrato = conta["extrato"])

    elif opcao == "0":
        global menu
        menu = 1
        print("Você saiu da sua conta.")

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


menu_usuario = '''
    
    ===========================

        [1] Entrar
        [2] Criar usuário
        [3] Criar conta
        [4] Cancelar Conta
        [0] Sair
    
    ===========================


=> '''

menu_conta = '''
    
    ======================

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [0] Sair
    
    ======================


=> '''

menu = 1
usuario = {}

#Operações para testes
#usuario.update({"12345678901": {"nome": "Gustavo", "nascimento": "26-02-91", "telefone": "15975346", "Endereço": "Rua dos Bobos, Número zero - Maravilhas - Mundo/Lu", "contas": {'1': {'saldo': 0, 'limite': 500, 'limite_saques': 3, "numero_saques": 0, 'extrato': ''}, '4': {'saldo': 0, 'limite': 500, 'limite_saques': 3, "numero_saques": 0, 'extrato': ''}}}})
#usuario.update({"98765432109": {"nome": "Jhonny", "nascimento": "15-05-87", "telefone": "95175364", "Endereço": "Rua dos Bobos, Número zero - Maravilhas - Mundo/Lu", "contas": ''}})
#conta = usuario["12345678901"]["contas"]["1"]  
    
while True:
    if menu == 1:
        #print("Menu de usuário.")
        conta = menu1()
    elif menu == 2:
        #print("Menu de conta.")
        if conta == 0:
            print("Conta inválida.")
            menu = 1
        else:
            menu2(conta)
    else:
        print("Valor de menu inválido.")
        menu = 1


