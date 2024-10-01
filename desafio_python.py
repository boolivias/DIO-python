menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valorDeposito = float(input("Valor a ser depositado: "))

        if valorDeposito < 0:
            print("Valor inválido.")
            continue

        saldo += valorDeposito
        extrato += f"""
\t + R$ {valorDeposito:.2f}
-----------------------------------------"""

    elif opcao == "s":
        valorSaque = float(input("Valor do saque: "))

        if valorSaque <0:
            print("Valor inválido.")
        elif valorSaque > saldo:
            print("Saldo insuficiente.")
        elif valorSaque > limite:
            print("Valor do saque acima do limite.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Saques diários excedidos.")

        saldo -= valorSaque
        extrato += f"""
\t - R$ {valorSaque:.2f}
-----------------------------------------"""
        numero_saques += 1

    elif opcao == "e":
        print("\n================ EXTRATO ================")

        if extrato:
            print(extrato)
        else:
            print("Não foram realizadas movimentações.")

        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")