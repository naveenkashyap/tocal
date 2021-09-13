import click

from ..clients.todo import TodoItem, TodoList
from ..commands.util import TODOLIST_FILEPATH

@click.group()
def todo():
    pass

@todo.command("add")
@click.option('-n', '--name', prompt=True, help='Name of Todo item')
@click.option('-p', '--priority', prompt=True, type=click.IntRange(1, 5), help='Priority of Todo item (min=1, max=5)')
@click.option('-d', '--duration', type=click.INT, default=30, help='Duration of Todo item in minutes')
def todo_add(name, priority, duration):
    todo_list = TodoList.load(TODOLIST_FILEPATH)
    todo_list.add(TodoItem(name, priority, duration))
    todo_list.save(TODOLIST_FILEPATH)

@todo.command("list")
def todo_list():
    click.echo(TodoList.load(TODOLIST_FILEPATH))

@todo.command("clear")
@click.confirmation_option(prompt='Are you sure you want to clear the Todo list? This cannot be undone!')
def todo_empty():
    try:
        TODOLIST_FILEPATH.unlink()
    except FileNotFoundError:
        pass

@todo.command("delete")
def todo_delete():
    todo_list = TodoList.load(TODOLIST_FILEPATH)

    if len(todo_list) == 0:
        click.echo(f'Todo list is empty!')
        return

    idx = int(input(f"{todo_list}\nWhich item do you want to delete? "))

    if 0 > idx or idx >= len(todo_list):
        click.echo(f"Must choose a item number between 1 and {len(todo_list)}")
        raise click.Abort()

    todo_list.remove(idx-1)
    click.echo(todo_list)
    todo_list.save(TODOLIST_FILEPATH)

@todo.command("edit")
def todo_edit():
    pass
