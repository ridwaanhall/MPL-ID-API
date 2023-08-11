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


@app.route('/mpl-id/statistics-teams', methods=['GET'])
def get_mpl_id_statistics():
  return MPL_ID.statistics_teams()


@app.route('/mpl-id/statistics-players', methods=['GET'])
def get_players_statistics():
  return MPL_ID.statistics_players()


@app.route('/mpl-id/statistics-heroes', methods=['GET'])
def get_heroes_staatistics():
  return MPL_ID.statistics_heroes()


@app.route('/mpl-id/statistics-hero-pools', methods=['GET'])
def get_hero_pools_statistics():
  return MPL_ID.statistics_hero_pools()


@app.route('/mpl-id/statistics-player-pools', methods=['GET'])
def get_player_pools_statistics():
  return MPL_ID.statistics_player_pools()


@app.route('/mpl-id/statistics-player-mvp', methods=['GET'])
def get_player_mvp_statistics():
  return MPL_ID.statistics_player_mvp()
