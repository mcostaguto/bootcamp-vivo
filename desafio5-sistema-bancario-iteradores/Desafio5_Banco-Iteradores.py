from abc import ABC, abstractmethod
from datetime import datetime

def log_transacao(func):
    def envelope(*args, **kwargs):
        if "Depositar" in str(args[len(args)-1]):
            print(f"\nOperação Depositar realizada em {datetime.now()}\n")
        elif "Sacar" in str(args[len(args)-1]):
            print(f"\nOperação Sacar realizada em {datetime.now()}\n")
        else:
            print(f"\nOperação {func.__name__} realizada em {datetime.now()}\n")
        func(*args, **kwargs)
    
    return envelope

class Banco:
    def __init__(self, agencia):
        self._agencia = agencia
        self._clientes = []
        self._contas = []

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def clientes(self):    #Gerador de clientes
        for cliente in self._clientes:
            yield cliente
    
    def addCliente(self, cliente: PessoaFisica):
        self._clientes.append(cliente)

    def cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente

    @property
    def contas(self):
        return self._contas

    def addConta(self, conta):
        self._contas.append(conta)
    
    def conta(self, numero):
        for conta in self._contas:
            if conta.numero == numero:
                return conta
    
        
    def isCliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return True
        return False
        
    def temConta(self, numero):
        for conta in ContaIterador(self.contas):
            if conta.numero == numero:
                return True
        return False
    
    @log_transacao
    def criar_conta(self, cpf):
        if self.isCliente(cpf):
            cliente = self.cliente(cpf)
    
            if len(self.contas) == 0:
                conta = ContaCorrente.nova_conta(self.agencia, '1', cliente)
            else:
                numero = str(int(max(self.contas)) + 1)
                conta = ContaCorrente.nova_conta(self.agencia, numero, cliente)
        
            self.addConta(conta)
            return conta
        else:
            print("Esse usuário não possui cadastro neste banco.")


class Transacao(ABC):
    def __init__(self, valor: float):
        self._valor = valor
        self._datetime = datetime.now()
    
    @property
    def valor(self):
        return self._valor

    @property
    def datetime(self):
        return self._datetime

    @abstractmethod
    def registrar(self, conta):
        pass

class Depositar(Transacao):
    def __init__(self, valor: float):
        super().__init__(valor)

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta._historico.adicionar_transacao(self)
        
class Sacar(Transacao):
    def __init__(self, valor: float):
        super().__init__(valor)

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(self)
    
class Historico:
    def __init__(self):
        self._historico = []

    def adicionar_transacao(self, transacao):
        self._historico.append(transacao)

    '''
    def gerar_relatorio(self, tipo_transacao = None):
        extrato = ""
        for transacao in self._historico:
            if (type(transacao) == Depositar) and (tipo_transacao == Depositar or tipo_transacao == None):
                extrato += "       Deposito          +R$"
                extrato += f"{transacao.valor:05.2f}\n"
            elif (type(transacao) == Sacar) and (tipo_transacao == Sacar or tipo_transacao == None):
                extrato += "       Saque             -R$"
                extrato += f"{transacao.valor:05.2f}\n"

        print("\n================ EXTRATO ================")
        print("   Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n       Saldo:             R$ {conta.saldo}")
        print("==========================================")
        '''
    def gerador_relatorio(self, tipo_transacao = None):
        if len(self._historico) == 0:
            yield "   Não foram realizadas movimentações."
        else:
            for transacao in self._historico:
                extrato = ""
                if (type(transacao) == Depositar) and (tipo_transacao == Depositar or tipo_transacao == None):
                    extrato += "       Deposito          +R$"
                    extrato += f"{transacao.valor}"
                elif (type(transacao) == Sacar) and (tipo_transacao == Sacar or tipo_transacao == None):
                    extrato += "       Saque             -R$"
                    extrato += f"{transacao.valor}"
                yield str(extrato)
            


class Cliente:
    def __init__(self, telefone, endereco):
        self._telefone = telefone
        self._endereco = endereco
        self._contas = []
        self._historico = []
        self._data_criacao = datetime.now()

    @property
    def contas(self):
        return self._contas

    @log_transacao
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)
        return conta
    
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

class Conta(ABC):
    def __init__(self, agencia, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
        self._data_criacao = datetime.now()

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
    def addTransacao(self, transacao):
        self._historico.adicionar_transacao(transacao)

    @abstractmethod
    def nova_conta(cls, agencia, numero, cliente):
        pass

    def sacar(self, valor: float):
        if valor > self.saldo: #Testa se tem saldo suficiente
            print("Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("Valor inválido.")
    
        return False

    def depositar(self, valor: float):
        if valor > 0: #Testa se o valor informado é válido
            self._saldo += valor
            print(f"Depósito de R${valor} realizado com sucesso.")
            return True

        return False
    
    def extrato(self):
        print("\n================ EXTRATO ================")
        for extrato in self._historico.gerador_relatorio():
            print(extrato)
        print(f"\n       Saldo:             R${conta.saldo}")
        print("==========================================")

class ContaIterador:      #Iterador de contas
    def __init__(self, contas: list):
        self.contas = contas
        self.indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self.indice]
            self.indice += 1
            return conta            
        except IndexError:
                raise StopIteration

class ContaCorrente(Conta):
    def __init__(self, agencia, numero, cliente, limite = 500, limite_saques = 3, numero_saques = 0):
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = numero_saques
        super().__init__(agencia, numero, cliente)

    @classmethod
    def nova_conta(cls, agencia, numero, cliente):
        conta = ContaCorrente(agencia, numero, cliente)
        cliente.adicionar_conta(conta)
        print(f"Conta {int(conta._numero):04d} criada para o usuario {cliente._nome}")
        return conta

    def sacar(self, valor: float):
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

def entrar(banco):
    numero = str(input("Informe o número da conta: "))
    
    if banco.temConta(numero):
        conta = banco.conta(numero)
        if conta:
            usuario = conta.cliente
            print("\nVocê entrou na sua conta.")
        return usuario, conta
    else:
        print("Conta não localizada.")
        return 0, 0

@log_transacao
def criar_usuario(banco):
    #usuario = PessoaFisica("12345678901", "Gustavo", "15-05-87", "15975346", "Rua dos bobos, numero zero")
    #banco.addCliente(usuario)
    #return usuario

    cpf = str(input("Informe o CPF do usuário: "))
    
    if PessoaFisica.isCPF(cpf):
        if banco.isCliente(cpf):
            print("Usuário já possui cadastro nesse banco")
            return

        nome = str(input("Informe o nome do usuário: "))

        nascimento = str(input("Informe data de nascimento(dd-mm-aa): "))
        if not PessoaFisica.isNascimento(nascimento):
            print("data inválida")
            return

        telefone = input("Informe telefone de contato: ")
        if not PessoaFisica.isTelefone(telefone):
            print("Telefone inválido.")
            return

        logradouro = str(input("Informe endereço de residência: "))
        
        usuario = PessoaFisica(cpf, nome, nascimento, telefone, logradouro)
        banco.addCliente(usuario)
        print(f"\nCadastro de {usuario.nome} realizado com sucesso!")
        return usuario
    
    else:
        print("CPF inválido. Por favor, forneca um CPF válido")

def criar_conta(banco):
    #cpf = "12345678901"
    cpf = str(input("Informe o CPF do usuário: "))

    if PessoaFisica.isCPF(cpf):
        conta = banco.criar_conta(cpf)
        return conta
    else:
        print("CPF inválido. Por favor, forneca um CPF válido")    

class Menu:
    def __init__(self):
        self._opcao = 0

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

    def display_menu(self, banco):
        _opcao = str(input(self._menu))

        if _opcao == "1":
            #print("Entrar")
            usuario, conta = entrar(banco)
            if conta:
                return usuario, conta

        elif _opcao == "2":
            #print("Usuario")
            usuario = criar_usuario(banco)

        elif _opcao == "3":
            #print("Conta")
            criar_conta(banco)

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
        _opcao = str(input(self._menu))

        if _opcao == "1":
            transacao = Depositar(float(input("Informe valor a ser depositado: ")))
            usuario.realizar_transacao(conta, transacao)

        elif _opcao == "2":
            transacao = Sacar(float(input("Informe valor do saque: ")))
            usuario.realizar_transacao(conta, transacao)

        elif _opcao == "3":
            conta.extrato()

        elif _opcao == "0":
            global menu
            menu = 1
            print("Você saiu da sua conta.")

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


menu = 1
menu_usuario = MenuUsuario()
menu_conta = MenuConta()
banco = Banco("0001")

#Operações para testes
'''
gustavo = PessoaFisica("12345678901", "Gustavo", "15-05-87", "15975346", "Rua dos bobos, numero zero")
banco.addCliente(gustavo)
banco.criar_conta("12345678901")
transacao = Depositar(1000)
gustavo.realizar_transacao(conta, transacao)
transacao = Sacar(500)
gustavo.realizar_transacao(conta, transacao)
transacao = Sacar(300)
gustavo.realizar_transacao(conta, transacao)
'''

while True:
    if menu == 1:
        #print("Menu de usuário.")
        usuario, conta = menu_usuario.display_menu(banco)
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


