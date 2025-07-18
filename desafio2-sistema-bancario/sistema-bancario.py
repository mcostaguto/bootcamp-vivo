menu = '''
    
    ======================

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [0] Sair
    
    ======================


=> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"    Depósito: +R$ {valor:.2f}\n"
            print(f"Você depositou R$ {valor:.2f} com sucesso\n")

        else:
            print("Falhou! Por favor, informe um valor válido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo: #Testa se tem saldo suficiente
            print("Você não tem saldo suficiente para essa operação.")

        elif valor > limite: #Testa o valor limite da operação
            print("O valor informado excede o limite para essa operação.")

        elif numero_saques >= LIMITE_SAQUES: #Testa a quantidade de operações executadas
            print("Você excedeu o número máximo de operações de saques.")

        elif valor > 0:
            saldo -= valor
            extrato += f"    Saque:    -R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Você sacou R$ {valor:.2f} com sucesso\n")

        else:
            print("Falhou! Por favor, informe um valor válido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("   Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n    Saldo:     R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
