"""Defines all the functions related to the database"""
from app import db

def fetch_matches() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from matches;").fetchall()
    conn.close()
    match_list = []
    for result in query_results:
        item = {
            "Team1ID":      result[0],
            "Team2ID":      result[1],
            "Team1Score":   result[2],
            "Team2Score":   result[3],
            "T1FG":         result[4],
            "T1FGA":        result[5],
            "T13P":         result[6],
            "T13PA":        result[7],
            "T1FT":         result[8],
            "T1FTA":        result[9],
            "T1ORB":        result[10],
            "T1DRB":        result[11],
            "T1AST":        result[12],
            "T1STL":        result[13],
            "T1BLK":        result[14],
            "T1TOV":        result[15],
            "T1PF":         result[16],

            "T2FG":         result[17],
            "T2FGA":        result[18],
            "T23P":         result[19],
            "T23PA":        result[20],
            "T2FT":         result[21],
            "T2FTA":        result[22],
            "T2ORB":        result[23],
            "T2DRB":        result[24],
            "T2AST":        result[25],
            "T2STL":        result[26],
            "T2BLK":        result[27],
            "T2TOV":        result[28],
            "T2PF":         result[29],

            "MatchID":      result[30]
        }
        match_list.append(item)

    return match_list


def update_match_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`
    Args:
        task_id (int): Targeted task_id
        text (str): Updated description
    Returns:
        None
    """

    conn = db.connect()
    query = 'Update matches set Team1Score = {} where MatchID = {};'.format(int(text), task_id)
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


def insert_new_match(t1score: str, t2score: str, t1id: str, t2id: str) ->  int:
    """Insert new task to todo table.
    Args:
        text (str): Task description
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query_results = conn.execute("select MAX(MatchID) from matches")
    query_results = [x for x in query_results]
    task_id = query_results[0][-1] + 1
    query = 'Insert Into matches (Team1ID, Team2ID, Team1Score, Team2Score, T1FG, T1FGA, T13P, T13PA, T1FT, T1FTA, T1ORB, T1DRB, T1AST, T1STL, T1BLK, T1TOV, T1PF, T2FG, T2FGA, T23P, T23PA, T2FT, T2FTA, T2ORB, T2DRB, T2AST, T2STL, T2BLK, T2TOV, T2PF, MatchID) VALUES ({}, {}, {}, {}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, {});'.format(
        int(t1id), int(t2id), int(t1score), int(t2score), task_id)
    conn.execute(query)
    conn.close()

    return task_id


def remove_match_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From matches where MatchID={};'.format(task_id)
    conn.execute(query)
    conn.close()

def fetch_by_keyword(teamid: int) -> dict:
    """searches all matches based on team1id
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from matches where Team1ID={};".format(teamid))
    conn.close()
    match_list = []
    for result in query_results:
        item = {
            "Team1ID":      result[0],
            "Team2ID":      result[1],
            "Team1Score":   result[2],
            "Team2Score":   result[3],
            "T1FG":         result[4],
            "T1FGA":        result[5],
            "T13P":         result[6],
            "T13PA":        result[7],
            "T1FT":         result[8],
            "T1FTA":        result[9],
            "T1ORB":        result[10],
            "T1DRB":        result[11],
            "T1AST":        result[12],
            "T1STL":        result[13],
            "T1BLK":        result[14],
            "T1TOV":        result[15],
            "T1PF":         result[16],

            "T2FG":         result[17],
            "T2FGA":        result[18],
            "T23P":         result[19],
            "T23PA":        result[20],
            "T2FT":         result[21],
            "T2FTA":        result[22],
            "T2ORB":        result[23],
            "T2DRB":        result[24],
            "T2AST":        result[25],
            "T2STL":        result[26],
            "T2BLK":        result[27],
            "T2TOV":        result[28],
            "T2PF":         result[29],

            "MatchID":      result[30]
        }
        match_list.append(item)

    return match_list

def get_wl_diffs() -> dict:
    conn = db.connect()
    query = "SELECT Team, sum(ifnull(diff1,0) + ifnull(diff2,0)) as win_lose_diff FROM ((select Team1ID as Team, avg(Team1Score - Team2Score) as diff1, null as diff2 from matches group by Team1ID) UNION (select Team2Id as Team2, null, avg(Team2Score - Team1Score) as diff2 from matches group by Team2ID)) B GROUP  BY Team ORDER BY Team;"

    query_results = conn.execute(query).fetchall()
    conn.close()
    diff_list = []
    for result in query_results:
        item = {
            "TeamID":   result[0],
            "WLDiff":   result[1]
        }
        diff_list.append(item)

    return diff_list