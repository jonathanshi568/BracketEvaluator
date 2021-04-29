""" Specifies routing for the application"""
from flask import render_template, request, jsonify, session
from flask_mysqldb import MySQL
from app import app, mysql, id_dict
from app import database as db_helper

team_map = None

@app.route("/teams/delete/<int:team_id>", methods=['POST'])
def delete(team_id):
    """ recieved post requests for entry delete """
    try:
        db_helper.remove_team_by_id(team_id)
        result = {'success': True, 'response': 'Removed team'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/teams/edit", methods=['POST'])
def update():
    """ recieved post requests for entry updates """    
    try:
        print(request.form)
        db_helper.update_team_entry(request.form['team-id'], request.form['team-name'], request.form['conference'], request.form['games-played'], request.form['wins'])
        result = {'success': True, 'response': 'Team Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/teams/create", methods=['POST'])
def create():
    # """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_team(request.form['team-name'], request.form['conference'], request.form['games-played'], request.form['wins'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/teams")
def teams():
    teams = db_helper.fetch_teams()
    return render_template("teams.html", teams=teams)

@app.route("/biggestUpsets")
def upsets():
    teams = db_helper.fetch_upsets()
    return render_template("upsets.html", teams=teams)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = {}
    return render_template("index.html", items=items)

@app.route("/home")
def home():
    return render_template("zuhairindex.html")

@app.route("/search", methods = ["POST"])
def zsearch():
    limit = request.form['Limit']
    keyword = request.form['keyword']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM predictions WHERE Team1ID IN (Select TeamID FROM teams WHERE TeamName LIKE \'%{}%\' AND SeasonYear=2021) OR Team2ID IN (Select TeamID FROM teams WHERE TeamName LIKE \'%{}%\' AND SeasonYear=2021) LIMIT {}'.format(keyword, keyword, limit))
    results = cur.fetchall()
    ids = [res[0] for res in results]
    team1 = [id_dict[res[1]] for res in results]
    team2 = [id_dict[res[2]] for res in results]
    winners = [id_dict[res[3]] for res in results]
    rounds = [res[4] for res in results]
    print(rounds[:5])
    return render_template('zuhairsearchresults.html', type = type, preds = zip(ids, team1, team2, winners, rounds))

@app.route("/create", methods = ["POST"])
def zcreate():
    Team1ID = request.form['Team1ID']
    Team2ID = request.form['Team2ID']
    WinnerID = request.form['WinnerID']
    BracketID = request.form['BracketID']
    Round = request.form['Round']
    cur = mysql.connection.cursor()
    query_str = "INSERT INTO Predictions(Team1ID, Team2ID, WinnerID, Round, BracketID) VALUES({}, {}, {}, {}, {})".format(Team1ID, Team2ID, WinnerID, Round, BracketID)
    cur.execute(query_str)
    mysql.connection.commit()
    return render_template("zuhairindex.html")

@app.route("/delete", methods = ["POST"])
def zdelete():
    PredictionID = request.form['PredictionID']
    cur = mysql.connection.cursor()
    query_str = "DELETE FROM Predictions WHERE PredictionID={}".format(PredictionID)
    cur.execute(query_str)
    mysql.connection.commit()
    return render_template("zuhairindex.html")

@app.route("/update", methods = ["POST"])
def zupdate():
    PredictionID = request.form['PredictionID']
    WinnerID = request.form['WinnerID']
    cur = mysql.connection.cursor()
    query_str = "UPDATE Predictions SET WinnerID={} WHERE PredictionID={}".format(WinnerID, PredictionID)
    cur.execute(query_str)
    mysql.connection.commit()
    return render_template("zuhairindex.html")

@app.route("/upsets", methods = ['POST'])
def zupsets():
    limit = request.form['Limit']
    cur = mysql.connection.cursor()
    query_str = "SELECT COUNT(*) as numUpsets, bracket FROM (SELECT b.BracketID as bracket, p.WinnerID AS winner \
    FROM brackets b JOIN predictions p ON b.BracketID=p.BracketID JOIN teams t ON t.teamID=p.WinnerID \
    WHERE t.SeasonYear=2021 AND ((SELECT Seed From teams t WHERE t.TeamID=p.WinnerID AND t.SeasonYear=2021) <  (SELECT Seed From teams t WHERE t.TeamID=p.Team1ID AND t.SeasonYear=2021) OR (SELECT Seed From teams t WHERE t.TeamID=p.WinnerID AND t.SeasonYear=2021) <  (SELECT Seed From teams t WHERE t.TeamID=p.Team2ID AND t.SeasonYear=2021))) AS PredictionUpsets \
    GROUP BY bracket ORDER BY numUpsets DESC LIMIT {};".format(limit)
    cur.execute(query_str)
    results = cur.fetchall()
    return render_template('zuhairupsets.html', upsets = results)