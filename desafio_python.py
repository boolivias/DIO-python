import re
from datetime import datetime

def realizar_deposito(saldo, extrato):
    valorDeposito = float(input("Valor a ser depositado: "))

    if valorDeposito < 0:
        print("Valor inválido.")
        return (saldo, extrato)

    return (saldo + valorDeposito, extrato + f"""\n\t + R$ {valorDeposito:.2f}\n-----------------------------------------""")

def realizar_saque(*, saldo, extrato, valor_limite, limite_saques, numero_saques):
    valorSaque = float(input("Valor do saque: "))

    if valorSaque <0:
        print("Valor inválido.")
    elif valorSaque > saldo:
        print("Saldo insuficiente.")
    elif valorSaque > valor_limite:
        print("Valor do saque acima do limite.")
    elif numero_saques >= limite_saques:
        print("Saques diários excedidos.")
    else: # só retorna valores alterados se nao entrar em nenhuma condição
        return (numero_saques+1, saldo - valorSaque, extrato + f"""\n\t - R$ {valorSaque:.2f}\n-----------------------------------------""")
    
    return (numero_saques, saldo, extrato)

def imprime_extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")

    if extrato:
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")

    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    
def cria_usuario(usuarios):
    nome = input("Digite o nome do usuário: ")

    try:
        dt_nascimento = input("Digite a data de nascimento no formato DD-MM-YYYY: ")
        datetime.strptime(dt_nascimento, "%d-%m-%Y")
    except ValueError:
        print("Data inválida.")
        return usuarios
    
    cpf = input("Digite o CPF do usuário: ")

    cpf = re.sub(r"\D", "", cpf)
    if(not len(cpf) == 11):
        print("CPF inválido")
        return usuarios
    
    if(busca_usuario_por_cpf(usuarios, cpf)):
        print("CPF já possui cadastro")
        return usuarios
    
    logradouro = input("Digite o logradouro da residencia: ")
    numero = input("Digite o numero da residencia: ")
    bairro = input("Digite o bairro da residencia: ")
    estado = input("Digite a sigla da UF: ")
    if(not len(estado) == 2):
        print("Sigla do estado inválida")
        return usuarios
    cidade = input("Digite a cidade da residencia: ")

    usuario = {
        "nome": nome,
        "nascimento": dt_nascimento,
        "cpf": cpf,
        "endereco": f"{logradouro} - {numero} - {bairro} - {cidade}/{estado}"
    }

    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuarios

def cria_conta_corrente(contas, usuarios):
    cpf = input("Digite o CPF do usuário: ")

    cpf = re.sub(r"\D", "", cpf)
    if(not len(cpf) == 11):
        print("CPF inválido")
        return contas
    
    if(not busca_usuario_por_cpf(usuarios, cpf)):
        print("CPF não possui cadastro")
        return contas
    
    conta_corrente = {
        "agencia": "0001",
        "conta": len(contas)+1,
        "cpf_usuario": cpf
    }

    contas.append(conta_corrente)
    print("Conta cadastrada com sucesso!")
    return contas

def busca_usuario_por_cpf(usuarios, cpf):
    for usuario in usuarios:
        if (usuario['cpf'] == cpf): return True

    return False

count_contas = 1
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastra usuário
[c] Cadastra Conta Corrente
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

contas = []
usuarios = []

while True:

    opcao = input(menu)

    if opcao == "d":
        saldo, extrato = realizar_deposito(saldo, extrato)

    elif opcao == "s":
        numero_saques, saldo, extrato = realizar_saque(saldo=saldo, extrato=extrato, valor_limite=limite, limite_saques=LIMITE_SAQUES, numero_saques=numero_saques)

    elif opcao == "e":
        imprime_extrato(saldo, extrato=extrato)

    elif opcao == "u":
        usuarios = cria_usuario(usuarios)

    elif opcao == "c":
        contas = cria_conta_corrente(contas, usuarios)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")