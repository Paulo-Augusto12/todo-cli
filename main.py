from enum import Enum
from pathlib import Path
import argparse
import json
import datetime


class PossibleStatus(Enum):
  todo = 0
  in_progress = 1
  done = 2
  
parser = argparse.ArgumentParser(description='Gerencie sua lista de tarefas')

parser.add_argument('command', help='Comando a ser executado (list, add, remove, update, mark-todo, mark-inprogress, mark-done)')
parser.add_argument('task_title', nargs='?',help='Tarefa a ser adicionada ou removida')
parser.add_argument('task_description', nargs='?', help='Descrição da tarefa que está sendo adicionada')
parser.add_argument('--status', choices=[0, 1, 2], type=int, help='Insira um status de tarefa para exibir os resultados de acordo com esse status')
parser.add_argument('--task_id', type=int, help='Id da tarefa que você está selecionando')
args = parser.parse_args()

  
if args.command == 'add':
  if not args.task_title:
    print("O título da tarefa não pode ser vazio")
    exit(1)
  
  task = {"title": args.task_title, "description": args.task_description,"status": PossibleStatus.todo.value }
  
  print(f"Adicionando a tarefa {task['title']} a lista de tarefas")
  
  try:
    with open('tasks.json', 'r') as file:
      tasks = json.load(file)
  except FileNotFoundError:
    tasks = {'tasks': []}
  
  task_id = tasks['tasks'][-1]['id'] + 1 if len(tasks['tasks']) >= 1 else 1
  
  datetime_now = str(datetime.datetime.now())
  task.update({'id': task_id, 'created_at': datetime_now, 'updated_at': datetime_now})
  
  tasks['tasks'].append(task)
  
  with open('tasks.json', 'w') as file:
    json.dump(tasks, file, indent=2)
      
      
  print(f"Tarefa {task['title']} adicionada com o status inicial de {task['status']}")

if args.command == 'list':
  try:
    with open('tasks.json', 'r') as f:
      tasks = json.load(f)
  except FileNotFoundError:
    print('O arquivo tasks.json ainda não existe, adicione uma tarefa com o commando add para cria-lo')
    exit(1)
  
  if args.status:
    filtered_tasks = [task for task in tasks['tasks'] if task['status'] == args.status]
    if filtered_tasks:
      for task in filtered_tasks:
        print(f"- {task['title']}, Status: {PossibleStatus(task['status']).name}")
    else:
      print('Não foram encontradas tarefas com o status fornecido')
  else:
    for task in tasks['tasks']:
      print(f"- {task['title']}, Status: {PossibleStatus(task['status']).name}")

if args.command == 'delete':
  try:
    with open('tasks.json', 'r') as f:
      tasks = json.load(f)
      if args.task_id:
        new_task_list = [task for task in tasks['tasks'] if task['id'] != args.task_id]
        with open('tasks.json', 'w') as f:
          tasks['tasks'] = new_task_list
          json.dump(tasks, f, indent=2)
          print(f"Tarefa deletada")
      else:
        print('Você deve passar um Id para a task que deseja deletar')
        exit(1)
  except FileNotFoundError:
    print('Arquivo de tarefas não encontrado, por favor adicione uma tarefa com o comando add para criar o arquivo')

def update_task_status(tasks, task_id, status, task_title):
  for task in tasks:
    if task['id'] == task_id:
      task['status'] = status
      task['title'] = task_title
      return tasks
  return tasks


if args.command == 'update':
  try:
    with open('tasks.json', 'r') as f:
      tasks = json.load(f)
      if args.task_id:
        if args.status:
          updated_tasks = update_task_status(tasks['tasks'], args.task_id, args.status, args.task_title)
          
          with open('tasks.json', 'w') as f:
            tasks['tasks'] = updated_tasks
            json.dump(tasks, f, indent=2)
        else:
          print('O status que você inseriu é inválido para ser assignado a esta tarefa')
      else:
        print('Não foi encontrada uma tarefa para o id especificado por você')
  except FileNotFoundError:
    print('Arquivo de tarefas não encontrado, por favor adicione uma tarefa com o comando add para criar o arquivo') 