from flask import Flask, redirect, url_for
from Controller.MLBBController import MLBBController
from Controller.HelpController import HelpController

app = Flask(__name__)


@app.route("/")
def hello_world():
  return redirect(url_for('global_help'))


# dashboard to Help
@app.route('/help', methods=['GET'])
def global_help():
  return HelpController.global_help()


# dashboard to check username
@app.route('/check-username', methods=['GET'])
def check_username_help():
  return HelpController.check_username_help()


# to get username by userid and zoneid
@app.route('/check-username/<int:user_id>/<int:zone_id>', methods=['GET'])
def check_username(user_id, zone_id):
  return MLBBController.check_username(user_id, zone_id)


# dashboard to count winrat target
@app.route('/winrate-target', methods=['GET'])
def calculate_winrate_help():
  return HelpController.calculate_winrate_help()


# to target winrate
@app.route('/winrate-target/<int:tMatch>/<float:tWr>/<float:wrReq>',
           methods=['GET'])
def calculate_winrate_route(tMatch, tWr, wrReq):
  return MLBBController.calculate_winrate_response(tMatch, tWr, wrReq)
