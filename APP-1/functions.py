FILEPATH = "todos.txt"

#custom function to read file 
def get_todos(filepath=FILEPATH):
    """Read a text file and return a list of
    todo items.
    """
    with open(filepath, 'r') as file_local:
        todos_loacal = file_local.readlines()
    return todos_loacal

def write_todos(todos_arg, filepath=FILEPATH):
    """Write a Todos item in a text file."""
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
 