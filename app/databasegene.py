"""Defines all the functions related to the database"""
from app import db

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = 'Select * from brackets;'
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list

def fetch_some(keyword:str) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = 'Select * from brackets WHERE description RLIKE "{}";'.format(keyword)
    #query = 'Select * from brackets;'
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list

def get_winners() -> dict:

    conn = db.connect()
    query = "SELECT teams.TeamName, COUNT(brackets.BracketID) as num_brackets FROM brackets JOIN predictions ON brackets.BracketID=predictions.BracketID JOIN teams ON predictions.WinnerID=teams.TeamID GROUP BY teams.TeamName ORDER BY num_brackets desc LIMIT 15;"

    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1]
        }
        todo_list.append(item)

    return todo_list

def update_task_entry(task_id: int, text: str, userid: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update brackets set Description = "{}" where BracketId = {};'.format(text, task_id)
    conn.execute(query)
    query = 'Update brackets set UserId = {} where BracketId = {};'.format(int(userid), task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str, userid: str) ->  None:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute("Select MAX(BracketID) FROM brackets")
    query_results = [x for x in query_results]
    task_id = query_results[0][0] + 1
    query = 'Insert Into brackets (BracketId, UserId, Description) VALUES ({}, {}, "{}");'.format(
        task_id, int(userid), text)
    conn.execute(query)
    conn.close()


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From brackets where BracketID={};'.format(task_id)
    conn.execute(query)
    conn.close()
