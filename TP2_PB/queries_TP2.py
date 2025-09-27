import pandas as pd

file_path = 'Dados-para-TP2-2025.csv'

try:
    df = pd.read_csv(file_path, decimal=',', thousands='.')

    df['data_inscricao'] = pd.to_datetime(df['data_inscricao'], dayfirst=True)

    print("--- Tarefa 1: Selecionar todos os clientes cuja área de profissão é 'TI'. ---")
    query1 = df[df['area_profissao'] == 'TI']
    print(query1)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 2: Selecionar os nomes dos clientes com mensalidade maior que 5000. ---")
    query2 = df[df['valor_mensalidade'] > 5000]['nome']
    print(query2)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 3: Selecionar o nome e a data de inscrição dos clientes que se inscreveram após 01/01/2022. ---")
    query3 = df[df['data_inscricao'] > '2022-01-01'][['nome', 'data_inscricao']]
    print(query3)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 4: Selecionar a área de profissão e a mensalidade média de cada área. ---")
    query4 = df.groupby('area_profissao')['valor_mensalidade'].mean()
    print(query4)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 5: Selecionar o nome e a profissão dos clientes que possuem 'da Silva' no nome. ---")
    query5 = df[df['nome'].str.contains("da Silva", case=False)][['nome', 'profissao']]
    print(query5)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 6: Selecionar todos os clientes com plano premium. ---")
    query6 = df[df['plano_premium'] == 1]
    print(query6)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 7: Selecionar o nome e a área de profissão dos clientes com profissão 'Analista'. ---")
    query7 = df[df['profissao'] == 'Analista'][['nome', 'area_profissao']]
    print(query7)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 8: Selecionar o nome e a mensalidade dos clientes, ordenados de forma decrescente pela mensalidade. ---")
    query8 = df[['nome', 'valor_mensalidade']].sort_values(by='valor_mensalidade', ascending=False)
    print(query8)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 9: Selecionar o nome e o ID dos clientes que se inscreveram em 2023. ---")
    query9 = df[df['data_inscricao'].dt.year == 2023][['nome', 'id_cliente']]
    print(query9)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 10: Selecionar o nome dos clientes da área 'Jurídico' com mensalidade menor ou igual a 3000. ---")
    query10 = df[(df['area_profissao'] == 'Jurídico') & (df['valor_mensalidade'] <= 3000)]['nome']
    print(query10)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 11: Selecionar o nome dos clientes que são 'Gerente' ou 'Diretor'. ---")
    profissoes_desejadas = ['Gerente', 'Diretor']
    query11 = df[df['profissao'].isin(profissoes_desejadas)]['nome']
    print(query11)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 12: Selecionar o nome do cliente e há quantos anos ele é cliente (considerando 2025). ---")
    df['anos_de_assinatura'] = 2025 - df['data_inscricao'].dt.year
    query12 = df[['nome', 'anos_de_assinatura']]
    print(query12)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 13: Selecionar o nome e a área de profissão dos clientes, ordenados pelo nome. ---")
    query13 = df[['nome', 'area_profissao']].sort_values(by='nome')
    print(query13)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 14: Selecionar o nome e a profissão dos clientes cujo nome começa com 'João'. ---")
    query14 = df[df['nome'].str.startswith('João')][['nome', 'profissao']]
    print(query14)
    print("\n" + "="*50 + "\n")

    print("--- Tarefa 15: Selecionar a quantidade de clientes em cada área de profissão. ---")
    query15 = df.groupby('area_profissao')['id_cliente'].count()
    print(query15)
    print("\n" + "="*50 + "\n")

except FileNotFoundError:
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    print("Por favor, verifique se o arquivo está na mesma pasta que o script.")