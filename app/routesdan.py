  
""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import databasedan as db_helper

@app.route("/matches/delete/<int:task_id>", methods=['POST'])
def ddelete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_match_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/matches/edit/<int:task_id>", methods=['POST'])
def dupdate(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "t1score" in data:
            db_helper.update_match_entry(task_id, data["t1score"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': data}

    return jsonify(result)


@app.route("/matches/create", methods=['POST'])
def dcreate():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_match(data['t1id'], data['t2id'], data['t1score'], data['t2score'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/dan")
def dhomepage():
    """ returns rendered homepage """
    items = db_helper.fetch_matches()
    return render_template("indexdan.html", items=items)


@app.route("/matches/search/<int:team_id>", methods=['POST','GET'])
def dsearch(team_id):
    data = request.get_json()
    items = db_helper.fetch_by_keyword(team_id)
    return render_template("indexdan.html", items=items)


@app.route("/wldiff/", methods=['POST', 'GET'])
def avgwldiff():
    items = db_helper.get_wl_diffs()
    return render_template("index2dan.html", items=items)