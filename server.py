from flask import Flask, redirect, url_for
from Controller.MLBBController import MLBB_in_game, MPL_ID
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
  return MLBB_in_game.check_username(user_id, zone_id)


# dashboard to count winrat target
@app.route('/winrate-target', methods=['GET'])
def calculate_winrate_help():
  return HelpController.calculate_winrate_help()


# to know win without lose by target winrate
@app.route('/winrate-target/<int:tMatch>/<float:tWr>/<float:wrReq>',
           methods=['GET'])
def calculate_winrate_route(tMatch, tWr, wrReq):
  return MLBB_in_game.calculate_winrate_response(tMatch, tWr, wrReq)


# to know win and lose by total match and winrate
@app.route('/wr-winlose/<int:total_matches_played>/<float:win_rate>',
           methods=['GET'])
def calculate_wr_winlose(total_matches_played, win_rate):
  return MLBB_in_game.wr_winlose(total_matches_played, win_rate)


@app.route('/mpl-id/transfer', methods=['GET'])
def get_mpl_id_transfer():
  return MPL_ID.transfer()


@app.route('/mpl-id/standings', methods=['GET'])
def get_mpl_id_standings():
  return MPL_ID.standings()


@app.route('/mpl-id/teams', methods=['GET'])
def get_mpl_id_teams():
  return MPL_ID.teams()


@app.route('/mpl-id/teams/<string:team_name>', methods=['GET'])
def get_mpl_id_team_players(team_name):
  return MPL_ID.team_players(team_name)
