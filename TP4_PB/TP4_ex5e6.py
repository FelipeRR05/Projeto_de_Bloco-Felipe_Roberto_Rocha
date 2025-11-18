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
        
def run_delete(connection):
    """Executa a Tarefa 5"""
    print("\n>>> Iniciando DELETE massivo (Tarefas 5 e 6)...")
    
    with open('delete_users.json', 'r') as f:
        data_delete = json.load(f)

    user_ids_to_delete = [item['user_id'] for item in data_delete]
    
    delete_sql = text("""
        DELETE FROM "Users"
        WHERE user_id = ANY(:user_ids);
    """)
    
    try:
        connection.execute(delete_sql, {'user_ids': user_ids_to_delete})
        connection.commit()
        print(">>> DELETE concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o DELETE: {e}")
        connection.rollback()

def main_delete():
    connection = get_connection()
    if not connection:
        return

    with connection:
        show_users(connection, 'Dados ANTES do DELETE')
        
        run_delete(connection)
        
        show_users(connection, 'Dados DEPOIS do DELETE')

    print("\nProcesso de DELETE finalizado.")

if __name__ == "__main__":
    main_delete()