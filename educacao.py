#atualizado no dia 15 de Outubro
# Importação dos módulos
import os
import oracledb
import pandas as pd

# Função para capturar a entrada do usuário
def get_input(margem, prompt):
    while True:
        entrada = input(margem + prompt)
        if entrada.isdigit():
            return int(entrada)
        print("Por favor, insira um número válido.")

# Função para listar trabalhadores
def listar_trabalhadores(inst_consulta):
    print("----- LISTAR TRABALHADORES -----\n")
    try:
        inst_consulta.execute('SELECT * FROM educacao')
        data = inst_consulta.fetchall()
        if not data:
            print("Não há trabalhadores cadastrados!")
            return
        
        # Cria um DataFrame e exibe
        dados_df = pd.DataFrame(data, columns=['Id', 'Nome', 'Especialidade', 'Idade'])
        print(dados_df)
        print("\n##### LISTADOS! #####")
    except Exception as e:
        print(f"Erro ao listar trabalhadores: {e}")

# Função para redefinir IDs
def resetar_ids(inst_exclusao):
    try:
        data_reset_ids = """ ALTER TABLE educacao MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) """
        inst_exclusao.execute(data_reset_ids)
        inst_exclusao.connection.commit()
    except Exception as e:
        print(f"Erro ao redefinir IDs: {e}")

# Inicializa a lista de trabalhadores
trabalhadores = []

# Tenta a conexão com o banco de dados
try:
    conn = oracledb.connect(user='rm559439', password="010170", dsn='oracle.fiap.com.br:1521/ORCL')
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    print("Erro: ", e)
    conexao = False
else:
    conexao = True 

margem = ' ' * 4  # Define uma margem para a exibição da aplicação

while conexao:
    # Limpa a tela via SO
    # os.system('cls')

    # Apresenta o menu
    print("------- CRUD - EDUCAÇÃO DO TRABALHADOR -------")
    print(""" 
    1 - Cadastrar Trabalhador
    2 - Listar Trabalhadores
    3 - Alterar Dados do Trabalhador
    4 - Excluir Trabalhador
    5 - Sair
    """)

    # Captura a escolha do usuário
    escolha = input(margem + "Escolha -> ")

    # Verifica se o número digitado é um valor numérico
    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 6
        print("Digite um número.\nReinicie a Aplicação!")

    match escolha:
        # CADASTRAR UM TRABALHADOR
        case 1:
            try:
                print("----- CADASTRAR TRABALHADOR -----\n")
                nome = input(margem + "Digite o nome........: ")
                especialidade = input(margem + "Digite a especialidade: ")
                idade = get_input(margem, "Digite a idade.......: ")  # Usando a função get_input

                # Monta o cadastro
                trabalhador = {'nome': nome, 'especialidade': especialidade, 'idade': idade}
                trabalhadores.append(trabalhador)  # Adiciona à lista de trabalhadores

                # Salva no banco de dados
                cadastro = f""" INSERT INTO educacao (campo_nome, campo_especialidade, campo_idade) VALUES ('{nome}', '{especialidade}', {idade})"""
                inst_cadastro.execute(cadastro)
                conn.commit()

                # Grava os dados no arquivo usuarios.txt
                with open('usuarios.txt', 'a') as file:
                    file.write(f"Nome: {nome}, Especialidade: {especialidade}, Idade: {idade}\n")

            except ValueError:
                print("Digite um número na idade!")
            except Exception as e:
                print("Erro na transação do BD:", e)
            else:
                print("\n##### Dados GRAVADOS #####")

        # LISTAR TODOS OS TRABALHADORES
        case 2:
            listar_trabalhadores(inst_consulta)

        # ALTERAR OS DADOS DE UM REGISTRO
        case 3:
            try:
                print("----- ALTERAR DADOS DO TRABALHADOR -----\n")

                trabalhador_id = get_input(margem, "Escolha um ID: ")  # Permite o usuário escolher um trabalhador pelo id

                # Consulta para verificar a existência do ID
                consulta = f""" SELECT * FROM educacao WHERE ID = {trabalhador_id}"""
                inst_consulta.execute(consulta)
                data = inst_consulta.fetchall()

                if not data:  # Se não há o ID
                    print(f"Não há um trabalhador cadastrado com o ID = {trabalhador_id}")
                else:
                    novo_nome = input(margem + "Digite um novo nome: ")
                    nova_especialidade = input(margem + "Digite uma nova especialidade: ")
                    nova_idade = get_input(margem, "Digite uma nova idade: ")

                    # Constrói a instrução de edição do registro com os novos dados
                    alteracao = f"""
                    UPDATE educacao SET campo_nome='{novo_nome}', campo_especialidade='{nova_especialidade}', campo_idade={nova_idade} WHERE ID={trabalhador_id}
                    """
                    inst_alteracao.execute(alteracao)
                    conn.commit()
            except ValueError:
                print("Digite um número na idade!")
            except Exception as e:
                print(margem + "Erro na transação do BD:", e)
            else:
                print("\n##### Dados ATUALIZADOS! #####")

        # EXCLUIR UM REGISTRO
        case 4:
            print("----- EXCLUIR TRABALHADOR -----\n")
            trabalhador_id = get_input(margem, "Escolha um ID: ")  # Permite o usuário escolher um trabalhador pelo ID
            consulta = f""" SELECT * FROM educacao WHERE ID = {trabalhador_id}"""
            inst_consulta.execute(consulta)
            data = inst_consulta.fetchall()

            if not data:  # Se não há o ID
                print(f"Não há um trabalhador cadastrado com o ID = {trabalhador_id}")
            else:
                # Cria a instrução SQL de exclusão pelo ID
                exclusao = f"DELETE FROM educacao WHERE ID={trabalhador_id}"
                inst_exclusao.execute(exclusao)
                conn.commit()
                print("\n##### Trabalhador APAGADO! #####")  # Exibe mensagem caso haja sucesso

        # SAI DA APLICAÇÃO
        case 5:
            conexao = False

        # CASO O NÚMERO DIGITADO NÃO SEJA UM DO MENU
        case _:
            input(margem + "Digite um número entre 1 e 6.")

# Fechar as conexões ao final
inst_cadastro.close()
inst_consulta.close()
inst_alteracao.close()
inst_exclusao.close()
conn.close()
