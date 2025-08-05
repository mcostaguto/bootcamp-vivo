from abc import ABC, abstractmethod

class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Depositar(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta._historico.adicionar_transacao(self)
        
class Sacar(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(self)
    
class Historico:
    def __init__(self):
        self._historico = []

    def adicionar_transacao(self, transacao):
        self._historico.append(transacao)

class Cliente:
    def __init__(self, telefone, endereco):
        self._telefone = telefone
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)
        return conta
    
    def tem_conta(self, numero):
        for conta in self._contas:
            if conta._numero == numero:
                return True
        return False
    
    @staticmethod
    def isTelefone(telefone):
        if (8 <= len(telefone) <= 9) and telefone.isdigit():
            return True
        else:
            return False
    
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, telefone, endereco):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(telefone, endereco)
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome

    @staticmethod
    def isCPF(cpf):
        if (len(cpf) == 11) and cpf.isdigit():
            return True
        else:
            return False
        
    @staticmethod
    def isNascimento(nascimento):
        if (len(nascimento) == 8) and (nascimento[2] == nascimento[5] == "-"):
            if (int(nascimento[:2]) <= 31) and (int(nascimento[3:5]) <= 12) and (int(nascimento[6:]) < 100):
                return True
            
        return False

class Conta:
    def __init__(self, agencia, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico._historico
    
    @historico.setter
    def historico(self, transacao):
        self._historico.adicionar_transacao(transacao)

    @classmethod
    def nova_conta(cls, numero, cliente):
        conta = Conta(numero, '1', cliente)
        cliente.adicionar_conta(conta)
        print(f"Conta {int(conta._numero):04d} criada para o usuario {cliente._nome}")
        return conta

    def sacar(self, valor):
        if valor > self.saldo(): #Testa se tem saldo suficiente
            print("Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("Valor inválido.")
    
        return False

    def depositar(self, valor):
        if valor > 0: #Testa se o valor informado é válido
            self._saldo += valor
            print(f"Depósito de R${valor} realizado com sucesso.")
            return True

        return False

class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, numero_saques, agencia, numero, cliente):
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = numero_saques
        super().__init__(agencia, numero, cliente)

    @classmethod
    def nova_conta(cls, numero, cliente):
        conta = ContaCorrente(500, 3, 0, '1', numero, cliente)
        cliente.adicionar_conta(conta)
        print(f"Conta {int(conta._numero):04d} criada para o usuario {cliente.nome}")
        return conta

    def sacar(self, valor):
        if valor > self.saldo: #Testa se tem saldo suficiente
            print("Saldo insuficiente.")

        elif valor > self._limite: #Testa o valor limite da operação
            print("Limite excedido para esta operação.")

        elif self._numero_saques >= self._limite_saques: #Testa a quantidade de operações executadas
            print("Número máximo de transações excedido.")

        elif valor > 0:
            self._saldo -= valor
            self._numero_saques += 1
            print(f"Saque de R${valor} realizado com sucesso.")
            return True
        else:
            print("Valor inválido.")
   

def entrar(clientes):
    cpf = input("Informe o CPF do usuário: ")

    for usuario in clientes:
        if cpf == usuario.cpf:
            numero = input("Informe o número da conta: ")
            for conta in usuario.contas:
                print(conta.numero)
                if numero == conta.numero:
                    print(f"Bem vindo {usuario.nome}. Você entrou na sua conta")
                    return usuario, conta
            
            print("Não existe uma conta com esse número vinculada a este usuário.")
            return 0, 0
    
    print("Usuário não encontrado. Favor informar o CPF de um cliente deste banco")        
    return 0, 0

def criar_usuario(cpf):
    nome = input("Informe o nome do usuário: ")
    
    nascimento = input("Informe data de nascimento(dd-mm-aa): ")
    if Cliente.isNascimento(nascimento):
        pass
    else:
        print("data inválida")
        return
    
    telefone = input("Informe telefone de contato: ")
    if Cliente.isTelefone(telefone):
        pass
    else:
        print("Telefone inválido.")
        return
    
    logradouro = input("Informe endereço de residência: ")

    usuario = PessoaFisica(cpf, nome, nascimento, telefone, logradouro)
    print(f"\nCadastro de {usuario.nome} realizado com sucesso!")
    return usuario
                  
def criar_conta(usuario):
    contas = []
    numero = 0
    for conta in usuario.contas:
        contas.append(conta.numero)

    if len(contas) == 0:
        conta = ContaCorrente.nova_conta('1', usuario)
    else:
        print("Não vazio")
        numero = str(int(max(contas)) + 1)
        conta = ContaCorrente.nova_conta(numero, usuario)
    
    return conta

    
def extrato(conta):
    extrato = ""
    for transacao in conta.historico:
        if type(transacao) == Depositar:
            extrato += "    Deposito    +R$"
            extrato += f"{transacao.valor}\n"
        elif type(transacao) == Sacar:
            extrato += "    Saque       -R$"
            extrato += f"{transacao.valor}\n"

    print("\n================ EXTRATO ================")
    print("   Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\n    Saldo:     R$ {conta.saldo}")
    print("==========================================")

class Menu(ABC):
    def __init__(self):
        self._opcao = 0

    @abstractmethod
    def display_menu(self):
        pass

class MenuUsuario(Menu):
    def __init__(self):
        super().__init__()
        self._menu = '''
    
    ===========================

        [1] Entrar
        [2] Criar usuário
        [3] Criar conta
        [0] Sair
    
    ===========================


    => '''

    def display_menu(self):
        _opcao = input(self._menu)

        if _opcao == "1":
            #print("Entrar")
            usuario, conta = entrar(clientes)
            if conta:
                return usuario, conta
        elif _opcao == "2":
            #print("Usuario")
            usuario = 0
            cpf = input("Informe o CPF do usuário: ")
            if Cliente.isCPF(cpf):
                for usuario in clientes:
                    if cpf == usuario.cpf:
                        print("Usuário já possui cadastro nesse banco")
                usuario = criar_usuario(cpf)
            else:
                print("CPF inválido. Por favor, forneca um CPF válido")

            if usuario:
                clientes.append(usuario)
        elif _opcao == "3":
            #print("Conta")
            cpf = input("Informe o CPF do usuário: ")
            if (len(cpf) == 11) and cpf.isdigit():
                for usuario in clientes:
                    if cpf == usuario.cpf:
                        conta = criar_conta(usuario)
                        return 0,0
                print("Esse usuário não possui cadastro neste banco.")
            else:
                print("CPF inválido. Por favor, forneca um CPF válido")

        elif _opcao == "0":
            print("Volte sempre. Obrigado por escolher nossos serviços.")
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        return 0, 0
        
class MenuConta(Menu):
    def __init__(self):
        super().__init__()
        self._menu = '''
    
    ======================

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [0] Sair
    
    ======================


    => '''

    def display_menu(self, usuario, conta):
        _opcao = input(self._menu)

        if _opcao == "1":
            transacao = Depositar(float(input("Informe valor a ser depositado: ")))
            usuario.realizar_transacao(conta, transacao)

        elif _opcao == "2":
            transacao = Sacar(float(input("Informe valor do saque: ")))
            usuario.realizar_transacao(conta, transacao)

        elif _opcao == "3":
            extrato(conta)

        elif _opcao == "0":
            global menu
            menu = 1
            print("Você saiu da sua conta.")

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")



menu = 1
menu_usuario = MenuUsuario()
menu_conta = MenuConta()
clientes = []

#Operações para testes
'''
gustavo = PessoaFisica("12345678901", "Gustavo", "26-02-91", "15975346", "gsdfaa")
ContaCorrente.nova_conta('1', gustavo)
conta = ContaCorrente.nova_conta('2', gustavo)
transacao = Depositar(1000)
gustavo.realizar_transacao(conta, transacao)
transacao = Sacar(500)
gustavo.realizar_transacao(conta, transacao)
transacao = Sacar(300)
gustavo.realizar_transacao(conta, transacao)
clientes.append(gustavo)
'''

while True:
    if menu == 1:
        #print("Menu de usuário.")
        usuario, conta = menu_usuario.display_menu()
        if usuario and conta:
            menu = 2
    elif menu == 2:
        #print("Menu de conta.")
        if usuario and conta:
            menu_conta.display_menu(usuario, conta)
        else:
            print("Usuário inválido.")
            menu = 1
    else:
        print("Valor de menu inválido.")
        menu = 1


