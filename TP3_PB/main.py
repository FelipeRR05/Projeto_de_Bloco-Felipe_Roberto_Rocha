import sqlalchemy
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:Rroch%402019@localhost/gymlog_db"

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
        print("--- VERIFIQUE A STRING 'DATABASE_URL' ---")
        return None

def consume_queries_to_dicts(connection):
    """
    Tarefas 5 e 6.
    """
    print("\n" + "="*45)
    print("TAREFAS 5 e 6: CONSUMINDO PARA DICIONÁRIOS")
    print("="*45)
    
    queries = {
        "INNER JOIN": query_inner_join,
        "LEFT JOIN": query_left_join,
        "RIGHT JOIN": query_right_join
    }
    
    for query_name, query_sql in queries.items():
        print(f"\n--- Resultado da Consulta {query_name} (Dicionários) ---")
        
        result = connection.execute(text(query_sql))
        
        dict_list = result.mappings().all()
            
        if not dict_list:
            print("Nenhum resultado encontrado.")
        for item in dict_list:
            print(dict(item))

def consume_queries_to_lists(connection):
    """
    Tarefas 7 e 8.
    """
    print("\n" + "="*45)
    print("TAREFAS 7 e 8: CONSUMINDO PARA LISTAS (TUPLAS)")
    print("="*45)
    
    queries = {
        "INNER JOIN": query_inner_join,
        "LEFT JOIN": query_left_join,
        "RIGHT JOIN": query_right_join
    }
    
    for query_name, query_sql in queries.items():
        print(f"\n--- Resultado da Consulta {query_name} (Listas/Tuplas) ---")
        
        result = connection.execute(text(query_sql))
        
        tuple_list = result.fetchall()
            
        if not tuple_list:
            print("Nenhum resultado encontrado.")
        for item in tuple_list:
            print(item)

def main():
    connection = get_connection()
    if connection:
        with connection:
            consume_queries_to_dicts(connection)
            consume_queries_to_lists(connection)
        
        print("\nProcesso concluído e conexão fechada.")

if __name__ == "__main__":
    main()