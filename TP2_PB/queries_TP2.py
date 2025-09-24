import pandas as pd

def run_basic_queries():
    try:
        df = pd.read_csv('cadastro_usuarios.csv')
        df['data_inscricao'] = pd.to_datetime(df['data_inscricao'])
    except FileNotFoundError:
        print("Erro: Arquivo 'cadastro_usuarios.csv' não encontrado.")
        return

    print("--- 1. Seleciona todos os usuários do nível 'Avançado' ---")
    query1 = df.loc[df['nivel_experiencia'] == 'Avançado']
    print(query1)
    print("\n" + "="*80 + "\n")
    
    print("--- 2. Seleciona usuários com idade inferior a 25 anos ---")
    query2 = df.loc[df['idade'] < 25]
    print(query2)
    print("\n" + "="*80 + "\n")
    
    print("--- 3. Seleciona usuários que se inscreveram em 2023 e têm foco em 'Hipertrofia' ---")
    query3 = df.loc[(df['data_inscricao'].dt.year == 2023) & (df['foco_treino'] == 'Hipertrofia')]
    print(query3)
    print("\n" + "="*80 + "\n")
    
    print("--- 4. Seleciona usuários com foco em 'Cardio' ou 'Resistência' ---")
    query4 = df.loc[df['foco_treino'].isin(['Cardio', 'Resistência'])]
    print(query4)
    print("\n" + "="*80 + "\n")

    print("--- 5. Lista todos os usuários, ordenados por data de inscrição (do mais novo ao mais antigo) ---")
    query5 = df.sort_values(by='data_inscricao', ascending=False)
    print(query5[['nome_completo', 'data_inscricao']])
    print("\n" + "="*80 + "\n")

    print("--- 6. Lista os 10 usuários mais pesados ---")
    query6 = df.sort_values(by='peso_kg', ascending=False).head(10)
    print(query6[['nome_completo', 'peso_kg']])
    print("\n" + "="*80 + "\n")

    print("--- 7. Conta o número total de usuários na base de dados ---")
    query7 = len(df)
    print(f"Total de usuários: {query7}")
    print("\n" + "="*80 + "\n")
    
    print("--- 8. Conta quantos usuários existem em cada 'nivel_experiencia' ---")
    query8 = df['nivel_experiencia'].value_counts()
    print(query8)
    print("\n" + "="*80 + "\n")
    
    print("--- 9. Calcula a idade média de todos os usuários ---")
    query9 = df['idade'].mean().round(1)
    print(f"Idade média dos usuários: {query9} anos")
    print("\n" + "="*80 + "\n")
    
    print("--- 10. Calcula a idade média dos usuários para cada 'foco_treino' ---")
    query10 = df.groupby('foco_treino')['idade'].mean().round(1)
    print(query10)
    print("\n" + "="*80 + "\n")
    
    print("--- 11. Encontra o usuário mais velho e o mais novo ---")
    idade_max = df['idade'].max()
    idade_min = df['idade'].min()
    usuario_mais_velho = df.loc[df['idade'] == idade_max, 'nome_completo'].iloc[0]
    usuario_mais_novo = df.loc[df['idade'] == idade_min, 'nome_completo'].iloc[0]
    print(f"Usuário mais velho: {usuario_mais_velho} ({idade_max} anos)")
    print(f"Usuário mais novo: {usuario_mais_novo} ({idade_min} anos)")
    print("\n" + "="*80 + "\n")

    print("--- 12. Conta quantos usuários se inscreveram por ano ---")
    query12 = df['data_inscricao'].dt.year.value_counts().sort_index()
    print(query12)
    print("\n" + "="*80 + "\n")
    
    print("--- 13. Adiciona uma coluna de IMC (Índice de Massa Corporal) ---")
    df['imc'] = (df['peso_kg'] / ((df['altura_cm'] / 100) ** 2)).round(2)
    query13 = df[['nome_completo', 'imc']]
    print(query13.head())
    print("\n" + "="*80 + "\n")
    
    print("--- 14. Lista os 5 usuários 'Iniciantes' com o maior peso ---")
    iniciantes_df = df.loc[df['nivel_experiencia'] == 'Iniciante']
    query14 = iniciantes_df.sort_values(by='peso_kg', ascending=False).head(5)
    print(query14[['nome_completo', 'peso_kg']])
    print("\n" + "="*80 + "\n")

    print("--- 15. Para cada 'foco_treino', mostra a contagem de membros e a idade média ---")
    query15 = df.groupby('foco_treino').agg(
        total_membros=('id_usuario', 'count'),
        idade_media=('idade', 'mean')
    ).round(1)
    print(query15)
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    run_basic_queries()