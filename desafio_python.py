import re
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

# def realizar_deposito(saldo, extrato):
#     valorDeposito = float(input("Valor a ser depositado: "))

#     if valorDeposito < 0:
#         print("Valor inválido.")
#         return (saldo, extrato)

#     return (saldo + valorDeposito, extrato + f"""\n\t + R$ {valorDeposito:.2f}\n-----------------------------------------""")

# def realizar_saque(*, saldo, extrato, valor_limite, limite_saques, numero_saques):
    
    
#     return (numero_saques, saldo, extrato)

# def imprime_extrato(saldo, *, extrato):
#     print("\n================ EXTRATO ================")

#     if extrato:
#         print(extrato)
#     else:
#         print("Não foram realizadas movimentações.")

#     print(f"\nSaldo: R$ {saldo:.2f}")
#     print("==========================================")
    
# def cria_usuario(usuarios):
#     nome = input("Digite o nome do usuário: ")

#     try:
#         dt_nascimento = input("Digite a data de nascimento no formato DD-MM-YYYY: ")
#         datetime.strptime(dt_nascimento, "%d-%m-%Y")
#     except ValueError:
#         print("Data inválida.")
#         return usuarios
    
#     cpf = input("Digite o CPF do usuário: ")

#     cpf = re.sub(r"\D", "", cpf)
#     if(not len(cpf) == 11):
#         print("CPF inválido")
#         return usuarios
    
#     if(busca_usuario_por_cpf(usuarios, cpf)):
#         print("CPF já possui cadastro")
#         return usuarios
    
#     logradouro = input("Digite o logradouro da residencia: ")
#     numero = input("Digite o numero da residencia: ")
#     bairro = input("Digite o bairro da residencia: ")
#     estado = input("Digite a sigla da UF: ")
#     if(not len(estado) == 2):
#         print("Sigla do estado inválida")
#         return usuarios
#     cidade = input("Digite a cidade da residencia: ")

#     usuario = {
#         "nome": nome,
#         "nascimento": dt_nascimento,
#         "cpf": cpf,
#         "endereco": f"{logradouro} - {numero} - {bairro} - {cidade}/{estado}"
#     }

#     usuarios.append(usuario)
#     print("Usuário cadastrado com sucesso!")
#     return usuarios

# def cria_conta_corrente(contas, usuarios):
#     cpf = input("Digite o CPF do usuário: ")

#     cpf = re.sub(r"\D", "", cpf)
#     if(not len(cpf) == 11):
#         print("CPF inválido")
#         return contas
    
#     if(not busca_usuario_por_cpf(usuarios, cpf)):
#         print("CPF não possui cadastro")
#         return contas
    
#     conta_corrente = {
#         "agencia": "0001",
#         "conta": len(contas)+1,
#         "cpf_usuario": cpf
#     }

#     contas.append(conta_corrente)
#     print("Conta cadastrada com sucesso!")
#     return contas

# def busca_usuario_por_cpf(usuarios, cpf):
#     for usuario in usuarios:
#         if (usuario['cpf'] == cpf): return True

#     return False

# count_contas = 1
# menu = """

# [d] Depositar
# [s] Sacar
# [e] Extrato
# [u] Cadastra usuário
# [c] Cadastra Conta Corrente
# [q] Sair

# => """

# saldo = 0
# limite = 500
# extrato = ""
# numero_saques = 0
# LIMITE_SAQUES = 3

# contas = []
# usuarios = []

# while True:

#     opcao = input(menu)

#     if opcao == "d":
#         saldo, extrato = realizar_deposito(saldo, extrato)

#     elif opcao == "s":
#         numero_saques, saldo, extrato = realizar_saque(saldo=saldo, extrato=extrato, valor_limite=limite, limite_saques=LIMITE_SAQUES, numero_saques=numero_saques)

#     elif opcao == "e":
#         imprime_extrato(saldo, extrato=extrato)

#     elif opcao == "u":
#         usuarios = cria_usuario(usuarios)

#     elif opcao == "c":
#         contas = cria_conta_corrente(contas, usuarios)

#     elif opcao == "q":
#         break

#     else:
#         print("Operação inválida, por favor selecione novamente a operação desejada.")

class Conta():
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.historico = Historico()
        self.saldo = 0
        self.agencia = "0001"

    @classmethod
    def nova_conta(class_conta, cliente, numero):
        return class_conta(numero, cliente)
    
    def sacar(self, valorSaque):
        if valorSaque < 0 :
            print("Valor incorreto!")
        if valorSaque > self._saldo:
            print("Saldo insuficiente.")
        else: # só retorna valores alterados se nao entrar em nenhuma condição
            self._saldo -= valorSaque

            return True
        
        return False
    
    def depositar(self, valor):
        if valor < 0:
            print("Valor inválido.")
        else:
            self._saldo += valor
            return True
        
        return False
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saques):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valorSaque):
        qtd_historico = len(self.historico.transacoes())

        if qtd_historico > self.limite_saques:
            print("Número máximo de saques excedido!")
        elif valorSaque > self.limite:
            print("Valor do saque acima do máximo permitido!")
        else:
            return super().sacar(valorSaque)

        return False
    
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)