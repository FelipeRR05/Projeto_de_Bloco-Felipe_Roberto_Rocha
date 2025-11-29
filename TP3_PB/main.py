import sqlalchemy
from sqlalchemy import create_engine, text
import json
import os

DATABASE_URL = "postgresql://postgres:Rroch%402019@localhost/gymlog_db"

# CONSULTAS
query_inner_join = """
SELECT
    U.full_name,
    WS.session_date,
    EL.exercise_name,
    EL.weight_kg,
    EL.reps_executed
FROM
    "Users" AS U
INNER JOIN
    "Workout_Sessions" AS WS ON U.user_id = WS.user_id
INNER JOIN
    "Exercise_Logs" AS EL ON WS.session_id = EL.session_id;
"""

query_left_join = """
SELECT
    U.full_name,
    U.experience_level,
    WS.session_date
FROM
    "Users" AS U
LEFT JOIN
    "Workout_Sessions" AS WS ON U.user_id = WS.user_id;
"""

query_right_join = """
SELECT
    WS.session_id,
    WS.session_date,
    EL.exercise_name,
    EL.weight_kg
FROM
    "Exercise_Logs" AS EL
RIGHT JOIN
    "Workout_Sessions" AS WS ON EL.session_id = WS.session_id;
"""

def get_connection():
    try:
        engine = create_engine(DATABASE_URL)
        return engine.connect()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def load_json_data(filename="upsert_data.json"):
    """Lê o arquivo JSON e retorna o dicionário."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{filename}' não encontrado.")
        return None

def perform_massive_upsert(connection, data):
    """
    Realiza UPSERT nas 3 tabelas.
    """
    
    # UPSERT DOS DADOS
    sql_users = text("""
        INSERT INTO "Users" (user_id, full_name, experience_level)
        VALUES (:user_id, :full_name, :experience_level)
        ON CONFLICT (user_id) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            experience_level = EXCLUDED.experience_level;
    """)
    
    sql_sessions = text("""
        INSERT INTO "Workout_Sessions" (session_id, user_id, session_date)
        VALUES (:session_id, :user_id, :session_date)
        ON CONFLICT (session_id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            session_date = EXCLUDED.session_date;
    """)

    sql_logs = text("""
        INSERT INTO "Exercise_Logs" (log_id, session_id, exercise_name, weight_kg, reps_executed)
        VALUES (:log_id, :session_id, :exercise_name, :weight_kg, :reps_executed)
        ON CONFLICT (log_id) DO UPDATE SET
            session_id = EXCLUDED.session_id,
            exercise_name = EXCLUDED.exercise_name,
            weight_kg = EXCLUDED.weight_kg,
            reps_executed = EXCLUDED.reps_executed;
    """)

    try:
        if 'users' in data:
            connection.execute(sql_users, data['users'])
            print(f">>> {len(data['users'])} Usuários inseridos.")
        
        if 'sessions' in data:
            connection.execute(sql_sessions, data['sessions'])
            print(f">>> {len(data['sessions'])} Sessões inseridas.")
            
        if 'logs' in data:
            connection.execute(sql_logs, data['logs'])
            print(f">>> {len(data['logs'])} Logs inseridos.")

        connection.commit()

    except Exception as e:
        print(f"Erro durante o UPSERT: {e}")
        connection.rollback()

def consume_queries_to_dicts(connection):
    print("\n" + "="*45)
    print("TAREFAS 5 e 6: CONSUMINDO PARA DICIONÁRIOS")
    print("="*45)
    
    queries = {
        "INNER JOIN": query_inner_join,
        "LEFT JOIN": query_left_join,
        "RIGHT JOIN": query_right_join
    }
    
    for query_name, query_sql in queries.items():
        print(f"\n--- Resultado da Consulta {query_name} ---")
        result = connection.execute(text(query_sql))
        dict_list = result.mappings().all()
            
        if not dict_list:
            print("Nenhum resultado encontrado.")
        for item in dict_list[:5]: 
            print(dict(item))
        print(f"... (Total: {len(dict_list)} registros)")

def consume_queries_to_lists(connection):
    print("\n" + "="*45)
    print("TAREFAS 7 e 8: CONSUMINDO PARA LISTAS (TUPLAS)")
    print("="*45)
    
    queries = {
        "INNER JOIN": query_inner_join,
        "LEFT JOIN": query_left_join,
        "RIGHT JOIN": query_right_join
    }
    
    for query_name, query_sql in queries.items():
        print(f"\n--- Resultado da Consulta {query_name} ---")
        result = connection.execute(text(query_sql))
        tuple_list = result.fetchall()
            
        if not tuple_list:
            print("Nenhum resultado encontrado.")
        for item in tuple_list[:5]:
            print(item)
        print(f"... (Total: {len(tuple_list)} registros)")

def main():
    connection = get_connection()
    if connection:
        with connection:
            # Carrega o JSON
            data = load_json_data("upsert_data.json")
            
            # Faz o UPSERT Massivo
            if data:
                perform_massive_upsert(connection, data)
            
            # Roda as consultas
            consume_queries_to_dicts(connection)
            consume_queries_to_lists(connection)
        
        print("\nProcesso concluído e conexão fechada.")

if __name__ == "__main__":
    main()