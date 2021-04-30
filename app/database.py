"""Defines all the functions related to the database"""
from app import db

def fetch_teams() -> dict:
    conn = db.connect()
    results = conn.execute("SELECT * FROM teams LIMIT 100;")
    conn.close()
    teams_list = []
    for r in results:
        team = {
            "id": r[22],
            "TeamName": r[0],
            "Conference": r[1],
            "GamesPlayed": r[2],
            "Wins": r[3]
        }
        teams_list.append(team)
    return teams_list

def update_team_entry(team_id: int, team_name: str, conference: str, games_played: int, wins: int) -> None:
    conn = db.connect()
    query = 'Update teams set TeamName = "{}", Conference = "{}", GamesPlayed = {}, Wins = {} where TeamID = {};'.format(team_name, conference, games_played, wins, team_id)
    conn.execute(query)
    conn.close()

def insert_new_team(team_name: str, conference: str, games_played: int, wins: int) ->  int:
    """Insert new task to todo table.
    Args:
        text (str): Task description
    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into teams (TeamName, Conference, GamesPlayed, Wins) VALUES ("{}", "{}", {}, {});'.format(team_name, conference, games_played, wins)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_team_by_id(team_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From teams where TeamID={};'.format(team_id)
    conn.execute(query)
    conn.close()



def fetch_upsets() -> dict:
    conn = db.connect()
    results = conn.execute("SELECT Team1.Seed as Team1Seed, Team1.TeamName as Team1Name, Team2.Seed as Team2Seed, Team2.TeamName as Team2Name,  matches.Team1Score, matches.Team2Score FROM (SELECT teams.Seed, matches.MatchID, teams.TeamName FROM matches JOIN teams on matches.Team1ID=teams.TeamID) as Team1 JOIN(SELECT teams.Seed, matches.MatchID, teams.TeamName FROM matches JOIN teams on matches.Team2ID=teams.TeamID) as Team2 ON Team1.MatchID=Team2.MatchID JOIN matches ON Team1.MatchID=matches.MatchID AND Team2.MatchID=matches.MatchID WHERE Team1.Seed < Team2.Seed AND Team1.Seed != 0 AND Team2.Seed != 0 AND matches.Team1Score < matches.Team2Score ORDER BY (Team2.Seed - Team1.Seed) desc LIMIT 100;")
    conn.close()
    teams_list = []
    for r in results:
        team = {
            "Team1Seed": r[0],
            "Team1Name": r[1],
            "Team2Seed": r[2],
            "Team2Name": r[3],
            "Team1Score": r[4],
            "Team2Score": r[5]
        }
        teams_list.append(team)
    return teams_list