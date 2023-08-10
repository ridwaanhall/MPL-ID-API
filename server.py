from flask import Flask, redirect, url_for
from Controller.MLBBController import MLBBController

app = Flask(__name__)


@app.route("/")
def hello_world():
  return redirect(url_for('check_username_help'))


@app.route('/check-username', methods=['GET'])
def check_username_help():
  return MLBBController.check_username_help()


@app.route('/check-username/<int:user_id>/<int:zone_id>', methods=['GET'])
def check_username(user_id, zone_id):
  return MLBBController.check_username(user_id, zone_id)

@app.route('/winrate-count/<int:tMatch>/<float:tWr>/<float:wrReq>', methods=['GET'])
def calculate_winrate_route(tMatch, tWr, wrReq):
  return MLBBController.calculate_winrate_response(tMatch, tWr, wrReq)

