import sqlalchemy
from sqlalchemy import create_engine, text
import json

DATABASE_URL = "postgresql://postgres:Rroch%402019@localhost/gymlog_db"

def get_connection():
    try:
        engine = create_engine(DATABASE_URL)
        return engine.connect()
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def show_users(connection, message):
    """Função auxiliar para conferir os dados (Tarefas 4 e 6)"""
    print(f"\n--- {message} ---")
    
    query = text('SELECT * FROM "Users" ORDER BY user_id;')
    result = connection.execute(query)
    
    for row in result:
        print(dict(row._mapping))

def run_upsert(connection):
    """Executa a Tarefa 3"""
    print("\n>>> Iniciando UPSERT massivo (Tarefas 3 e 4)...")
    
    with open('upsert_users.json', 'r') as f:
        data_upsert = json.load(f)

    upsert_sql = text("""
        INSERT INTO "Users" (user_id, full_name, experience_level)
        VALUES (:user_id, :full_name, :experience_level)
        ON CONFLICT (user_id) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            experience_level = EXCLUDED.experience_level;
    """)
    
    try:
        connection.execute(upsert_sql, data_upsert)
        connection.commit()
        print(">>> UPSERT concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o UPSERT: {e}")
        connection.rollback()

def main_upsert():
    connection = get_connection()
    if not connection:
        return

    with connection:
        show_users(connection, 'Dados ANTES do UPSERT')
        
        run_upsert(connection)
        
        show_users(connection, 'Dados DEPOIS do UPSERT')

    print("\nProcesso de UPSERT finalizado.")

if __name__ == "__main__":
    main_upsert()