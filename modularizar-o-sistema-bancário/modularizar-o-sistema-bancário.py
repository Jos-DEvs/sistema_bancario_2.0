from datetime import datetime

# Declaração dos variáveis
i = 0
y = 0

titulo = "EXTRATO"
hora_limite_de_operacao = " "
iteracao = 0

# O dicionário que estoca as informações
operacao = {"saldo": 0, "numero_saques": 0, "limite_saques": 10, "inicio": 0, "reloginho": ""}

filtragem = dict()
cliente = list()
conta = list()

# Função que gera a data e horas
def relogio():
    data_de_hoje = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    return data_de_hoje

# Função de confirmação da operação
def confirmacao_de_sucesso_da_operacao(status = False, **meu_dict):   
                
    if meu_dict.get("deposito"): # Verifica se "deposito" existe e é True
        print(f'{"Deposito realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()}: DEPOSITAR"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
    
    elif meu_dict.get("saque"):  # Verifica se "saque" existe e é True
        print(f'{"Saque realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()}: SACAR"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
    
    elif meu_dict.get("cliente"):  # Verifica se "cliente" existe e é True
        print(f'{"Cadastro realizado com sucesso!":=^50}') # Centralizar o texto
        pe_pagina = f"{relogio()}: CADASTRO DO CLIENTE"
        print(f"{pe_pagina:^50}") # Centralizar o texto
        meu_dict.clear()
    else:
        print("Nenhuma operação identificada.")

# Função de depósito
def deposito(valor_depositado):
    
    if valor_depositado > 0:
                
        operacao["saldo"] += valor_depositado
        
        global i        
        
        operacao[f"extrato{i}"] = {"tipo": "Depósito", "valor": f"{valor_depositado}", "data": f"{relogio()}"}            
        i += 1
        
        confirmacao_de_sucesso_da_operacao(deposito = True)
                
    else:
        print("Operação falhou! O valor informado é inválido.")

# Função de validação de saque
def validar_o_saque():
    
    if operacao["inicio"] == 1:
        if relogio() > operacao["reloginho"]:  # Se já é um outro dia, reiniciar a variável numero_saques
            operacao["numero_saques"] = 0
            operacao["reloginho"] = ""
            operacao["inicio"] = 0
            
                    
    if operacao["numero_saques"] >= operacao["limite_saques"]:  # Nem deixar entrar um valor se o número máximo de saques foi excedido
        print("Operação falhou! O número máximo de saques diário já foi excedido.")
        return False
                    
    elif operacao["saldo"] == 0:
        print("Operação falhou! Você precisa fazer um depósito primeiro para poder sacar.")
        return False
    else:
        return True

# Função de saque
def saque(valor_a_sacar):

    if valor_a_sacar > operacao["saldo"]:
                print("Operação falhou! Você não tem saldo suficiente.")

    elif valor_a_sacar > 500:
                print("Operação falhou! O valor do saque excede o limite.")

    elif valor_a_sacar > 0:
                                        
        if operacao["inicio"] == 0:  
            hora_limite_de_operacao = f"{relogio()}"                    
            operacao["reloginho"] = hora_limite_de_operacao.replace(f'{hora_limite_de_operacao[9:]}','24:00:00')   # Definir a hora limite de operação diária            
            operacao["inicio"] = 1
                    
        operacao["saldo"] -= valor_a_sacar

        global i

        operacao[f"extrato{i}"] = {"tipo": "Saque", "valor": f"{valor_a_sacar}", "data": f"{relogio()}"}
        i += 1
        operacao["numero_saques"] += 1
        
        confirmacao_de_sucesso_da_operacao(saque = True)       
                
    else:
        print("Operação falhou! O valor informado é inválido.")

# Função de exibição de extrato
def exibir_extrato():
    if operacao["saldo"] == 0:
        print("Operação falhou! Você precisa fazer um depósito primeiro para poder exibir um extrato.")
        
    else:
                    
        # Organizar as transações por tipo
        
        global y, iteracao
        
        # Iterar o dicionário operacao, toda vez que encontrar uma transação de tipo "Depósito" coloque-a no dicionário "filtragem"
        for chave, valor in operacao.items():
            if chave.startswith('extrato'):  
                                                    
                if valor['tipo'] == "Depósito":
                                                                                        
                    # print(f"{valor['tipo']}:\n{valor['valor']:>15} {11 * '-'} {valor['data']:>17}") 
                    filtragem[f"extrato{y}"] = {"tipo": f"{valor['tipo']}", "valor": f"{valor['valor']}", "data": f"{valor['data']}"} 
                    y += 1
        
        # Iterar o dicionário operacao novamente, toda vez que encontrar uma transação de tipo "Saque" adicione-a no dicionário "filtragem"
        for chave, valor in operacao.items():
            if chave.startswith('extrato'):  
                
                if valor['tipo'] == "Saque":
                    
                    # print(f"{valor['tipo']}:\n{valor['valor']:>15} {11 * '-'} {valor['data']:>17}") 
                    filtragem[f"extrato{y}"] = {"tipo": f"{valor['tipo']}", "valor": f"{valor['valor']}", "data": f"{valor['data']}"} 
                    y += 1
            
        print(f"\n {titulo:=^50}") # Centralizar o texto 
        
        # Exibir o dicionário filtragem
        for chave, valor in filtragem.items():
            if chave.startswith('extrato'):  
                                    
                if iteracao == 0:
                        print(f"{valor['tipo']}:\n{valor['valor']:>15} {11 * '-'} {valor['data']:>17}") # Alinhar o texto a direita
                        iteracao = 1  
                else:
                    if valor['tipo'].strip().lower() == "depósito":
                        print(f"{valor['valor']:>15} {11 * '-'} {valor['data']:>17}") # Alinhar o texto a direita
                                                    
                    elif valor['tipo'].strip().lower() == "saque" and iteracao == 1:
                        print(f"{valor['tipo']}: \n {valor['valor']:>10} {15 * '-'} {valor['data']:>17}") # Alinhar o texto a direita
                        iteracao = 2
                    else:
                        print(f" {valor['valor']:>10} {15 * '-'} {valor['data']:>17}")  # Alinhar o texto a direita
                                                    
        print(f"\nSaldo: R$ {operacao["saldo"]:.2f}")
        print("=" * 50)
        pe_pagina = f"{relogio()}: EXIBIR EXTRATO"
        iteracao = 0
        filtragem.clear()
        print(f"{pe_pagina:>50}") # Alinhar o texto a direita

# Função de criação de cliente
def criar_cliente(cpf_cliente, nome_cliente, data_nascimento, nome_endereço):
    cliente.append([cpf_cliente, nome_cliente, data_nascimento, nome_endereço])   
    
    confirmacao_de_sucesso_da_operacao(cliente = True)

# Função de validação de CPF
def validar_cpf(cpf_cliente):
        
    for i in range(0, len(cliente)):
        
        if cpf_cliente == cliente[i][0]:  # cliente[i][0] é uma seleção da coluna CPF
            return True
    return False    # Essa linha não é obrigatória. Mas evita que a função retorna NONE caso ela não retorne True

# Função de criação de conta
def criar_conta(cpf_cliente):
    
    global conta
    
    # Testar se a lista conta está vazia antes de adicionar uma conta nela 
    if not conta:  # Se essa lista está vazia
        conta.append([cpf_cliente, 1, "0001"])
    else:        
        
        minha_lista = list()
        
        for i in range(0, len(conta)):          # Copiar a coluna do número da conta numa outra lista "minha_lista"
            minha_lista.append(conta[i][1])     # para poder identificar o número da última conta que foi aberta       
        
        conta.append([cpf_cliente, max(minha_lista) + 1, "0001"])
        
    print(conta)

while 1 == 1:
    
    # Construir o menu
    print(35 * "-")
    print("Bem-vindo! O que deseja fazer hoje? \n")
    print(" [d] Depositar\n [s] Sacar \n [e] Extrato \n [ncl] Novo Cliente \n [ncc] Nova Conta Corrente \n [a] Alterar data \n [t] Exibir o BD \n [q] Sair")

    # Entrada de dados do usuário
    opcao = input("=> ")
    
    # Operação de depósito
    if opcao == "d":
        
        valor_depositado = float(input("Informe o valor do depósito: "))
        
        deposito(valor_depositado)
        
    # Operação de saque
    elif opcao == "s":
        
        if (validar_o_saque()):
            valor_do_saque = float(input("Informe o valor do saque: "))
            saque(valor_a_sacar = valor_do_saque)
    
    # Operação de exibir o extrato  
    elif opcao == "e":
        
        exibir_extrato()
    
    # Operação de criar um cliente
    elif opcao == "ncl":
        
        cpf = True
        
        while cpf:
            cpf_cliente = int(input("Informe o CPF do cliente: "))
                        
            cpf = validar_cpf(cpf_cliente)
            
            if cpf:
                print("Operação falhou! Esse CPF já pertence a um outro cliente")
        
        nome_cliente = str(input("Informe seu nome: "))
        
        data_nascimento = str(input("Informe sua data de nascimento: "))
        
        nome_endereço = str(input("Informe seu endereço (logradouro, nro - bairro - cidade/sigla do estado): "))
        
        criar_cliente(cpf_cliente, nome_cliente, data_nascimento, nome_endereço)
    
    # Operação de criar uma conta
    elif opcao == "ncc":
        
        cpf = True
        
        while cpf:
            cpf_cliente = int(input("Por favor, informe o CPF que deseja vincular a esta conta: "))
                        
            cpf = validar_cpf(cpf_cliente)
            
            if not cpf:
                print("Operação falhou! Esse CPF não pertence a nenhum cliente")
            else:
                criar_conta(cpf_cliente)
                break
            
            
    # Sair do aplicativo
    elif opcao == "q":
        print("Até logo!")
        break
    
    # Alterar a data da operação    
    elif opcao == "a":
        print("Forma da data: dd/mm/aaaa")
        print("Ela deve ser inferior que a data de hoje para poder fazer esse teste")
        operacao["reloginho"] = valor = str(input("Informe a data: "))
    
    # Exibir o BD do sistema
    elif opcao == "t":
        print("Ainda não foi cadastrada uma operação no BD do sistema." if not operacao else operacao)
        
        print("Ainda não foi cadastrado um cliente no BD do sistema." if not cliente else cliente)
        
        print("Ainda não foi cadastrada uma conta no BD do sistema." if not conta else conta)
        
    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.\n")
        
