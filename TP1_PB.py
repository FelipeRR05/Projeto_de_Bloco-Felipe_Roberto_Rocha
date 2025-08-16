"""
Nome do Projeto: GymLog
Tema: Registro de Atividades Físicas

Este projeto é um diário de treino de academia. Onde o usuário pode gerenciar sua 
rotina de treinos. A ferramenta permite não só adicionar os exercícios planejados, 
mas também registrar detalhes da execução (como peso e repetições) após a conclusão, 
servindo como uma base para o acompanhamento de progresso do usuário.
"""

import datetime

exercises = []

def get_next_id():
    """Calcula o proximo ID disponivel com base no maior ID existente."""
    if not exercises:
        return 1
    last_id = max(exercise['id'] for exercise in exercises)
    return last_id + 1

def show_menu():
    """Exibe o menu principal de opcoes para o usuario."""
    print("\n=== GymLog - Registro de Atividades Físicas ===")
    print("1 - Adicionar novo exercício")
    print("2 - Listar exercícios")
    print("3 - Marcar exercício como concluido")
    print("4 - Remover exercício")
    print("5 - Sair")

def add_exercise(exercice_name, description, exercise_type, series, due_date, priority):
    """
    Adiciona um novo exercicio a lista de exercicios.

    Args:
        exercice_name (str): O nome do exercicio.
        description (str): Uma descricao detalhada do exercicio.
        exercise_type (str): O tipo de exercicio (ex: 'musculação').
        series (int): O numero de series planejadas.
        due_date (str): A data planejada para realizar o exercicio (prazo final).
        priority (str): A prioridade do exercicio (ex: 'Alta', 'Média', 'Baixa').
    """
    exercise = {
        'id': get_next_id(),
        'exercice_name': exercice_name,
        'description': description,
        'type': exercise_type,
        'series': series,
        'due_date': due_date,
        'priority': priority,
        'creation_date': datetime.date.today().strftime('%d/%m/%Y'),
        'repetitions': '',
        'weight': '',
        'observation': '',
        'status': 'pending'
    }
    exercises.append(exercise)
    print("\nExercício adicionado com sucesso!")

def list_exercises():
    """Lista todos os exercicios registrados, mostrando seus detalhes."""
    if not exercises:
        print("\nNenhum exercício registrado ainda.")
        return

    print("\n--- Lista de Exercícios ---")
    for exercise in exercises:
        print(f"\nID: {exercise['id']}")
        print(f"  Exercício: {exercise['exercice_name']}")
        print(f"  Descrição: {exercise['description']}")
        print(f"  Tipo: {exercise['type']}")
        print(f"  Séries: {exercise['series']}")
        print(f"  Data Planejada: {exercise['due_date']}")
        print(f"  Prioridade: {exercise['priority']}")
        print(f"  Data de Criação: {exercise['creation_date']}")
        print(f"  Repetições: {exercise['repetitions']}")
        print(f"  Peso: {exercise['weight']} kg")
        print(f"  Observação: {exercise['observation']}")
        print(f"  Status: {exercise['status'].capitalize()}")
    print("-------------------------")

def find_exercise_by_id(exercise_id):
    """
    Encontra um exercicio na lista pelo seu ID.

    Args:
        exercise_id (int): O ID do exercicio a ser encontrado.

    Returns:
        dict: O dicionario do exercicio, se encontrado.
        None: Se nenhum exercicio com o ID fornecido for encontrado.
    """
    for exercise in exercises:
        if exercise['id'] == exercise_id:
            return exercise
    return None

def select_exercise():
    """
    Permite ao usuario buscar um exercicio pelo nome e seleciona-lo pelo ID.

    Returns:
        dict: O dicionario do exercicio selecionado pelo usuario.
        None: Se nenhum exercicio for encontrado ou a selecao for invalida.
    """
    name_to_find = input("\nDigite o nome do exercício: ")
    matching_exercises = [ex for ex in exercises if ex['exercice_name'].lower() == name_to_find.lower()]

    if not matching_exercises:
        print(f"\nNenhum exercicio com o nome '{name_to_find}' encontrado.")
        return None
    
    if len(matching_exercises) == 1:
        return matching_exercises[0]

    print("\nMultiplos exercicios encontrados com esse nome:")
    for ex in matching_exercises:
        print(f"ID: {ex['id']} - Exercício: {ex['exercice_name']} (Data: {ex['due_date']})")
    
    try:
        exercise_id = int(input("\nPor favor, digite o ID do exercicio desejado: "))
        return find_exercise_by_id(exercise_id)
    except ValueError:
        print("ID inválido. Por favor, digite um numero.")
        return None

def mark_exercise_as_completed(exercise):
    """
    Marca um exercicio como concluido, solicitando os detalhes da execucao.

    Args:
        exercise (dict): O dicionario do exercicio a ser marcado como concluido.
    """
    print(f"\nConcluindo o exercício: {exercise['exercice_name']}")
    
    while True:
        try:
            repetitions = int(input("Quantas repetições você fez? "))
            break
        except ValueError:
            print("Valor inválido. Por favor, digite um número para as repetições.")

    while True:
        try:
            weight = float(input("Qual peso você usou (kg)? "))
            break
        except ValueError:
            print("Valor inválido. Por favor, digite um número para o peso.")
            
    observation = input("Alguma observação para a próxima vez? ")

    exercise['repetitions'] = repetitions
    exercise['weight'] = weight
    exercise['observation'] = observation
    exercise['status'] = 'completed'
    print(f"\nExercício com ID {exercise['id']} marcado como concluido!")

def remove_exercise(exercise):
    """
    Remove um exercicio da lista.

    Args:
        exercise (dict): O dicionario do exercicio a ser removido.
    """
    exercises.remove(exercise)
    print(f"\nExercício com ID {exercise['id']} removido com sucesso!")

def main():
    """Funcao principal que executa o loop do programa."""
    while True:
        show_menu()
        option = input("\nEscolha uma opção: ")

        if option == "1":
            exercise_name = input("\nNome do exercício: ")
            description = input("Descrição (ex: musculo alvo, equipamento): ")
            exercise_type = input("Tipo (musculação, cardio, etc.): ")
            while True:
                try:
                    series = int(input("Séries: "))
                    break
                except ValueError:
                    print("Valor inválido. Por favor, digite um número para as séries.")
            due_date = input("Data planejada (dd/mm/aaaa): ")
            priority = input("Prioridade (Alta, Média, Baixa): ")
            add_exercise(exercise_name, description, exercise_type, series, due_date, priority)
        
        elif option == "2":
            list_exercises()
        
        elif option == "3":
            exercise_to_complete = select_exercise()
            if exercise_to_complete:
                mark_exercise_as_completed(exercise_to_complete)
            else:
                print("Operação cancelada.")
        
        elif option == "4":
            exercise_to_remove = select_exercise()
            if exercise_to_remove:
                remove_exercise(exercise_to_remove)
            else:
                print("Operação cancelada.")
        
        elif option == "5":
            print("\nSaindo do GymLog. Até mais!")
            break
        
        else:
            print("\nOpção inválida. Por favor, escolha uma opção de 1 a 5.")

if __name__ == "__main__":
    main()