from app import app
from flask import render_template, url_for, request, redirect, jsonify
import connections
import timetable
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
def index(name = None):
    return render_template('cse6242.html', name = name)

@app.route('/Page1InputPost', methods=['POST','GET'])
def getinput():
    data = request.get_json()
    res = connections.connection_main(data['departAddress'],data['arriveAddress'],data['typeCheckList'],data['startTime'],data['endTime'])
    #return render_template('page2NoKey.html', json=res)
    return jsonify(dict(redirect=url_for('.page2', json = json.dumps(res))))


@app.route('/Page2InputPost', methods=['POST','GET'])
def getinput2():
    data = request.get_json()
    timetable_json = timetable.createtimetable(data)
    return jsonify(dict(redirect=url_for('.timetable_render', json = timetable_json)))

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/timetable')
def timetable_render():
    return render_template('timetable.html')

if __name__ == '__main__':
    app.run()

