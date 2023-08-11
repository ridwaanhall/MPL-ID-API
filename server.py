from flask import Flask, redirect, url_for
from Controller.MLBBController import MLBB_in_game, MPL_ID, JSONtoXML
from Controller.HelpController import HelpController

app = Flask(__name__)


@app.route("/")
def home():
  return redirect(url_for('global_help_xml'))


# dashboard to Help
@app.route('/help.json', methods=['GET'])
def global_help_json():
  return HelpController.global_help()


# dashboard to Help
@app.route('/help.xml', methods=['GET'])
def global_help_xml():
  help = HelpController.global_help()
  return JSONtoXML.convert_json_to_xml(help)


# dashboard to check username help
@app.route('/check-username', methods=['GET'])
def check_username_help():
  return HelpController.check_username_help()



# to get username by userid and zoneid
# example https://mlbb-api.ridwaanhall.repl.co/check-username/688700997/8742
@app.route('/check-username/<int:user_id>/<int:zone_id>', methods=['GET'])
def check_username(user_id, zone_id):
  return MLBB_in_game.check_username(user_id, zone_id)


# dashboard to count winrat target help
@app.route('/winrate-target', methods=['GET'])
def calculate_winrate_help():
  return HelpController.calculate_winrate_help()


# to know win without lose by target winrate. tMatch/tWr/wrReq. wr must dot (80 --> 80.0)
# example https://mlbb-api.ridwaanhall.repl.co/winrate-target/100/50.0/60.0
@app.route('/winrate-target/<int:tMatch>/<float:tWr>/<float:wrReq>',
           methods=['GET'])
def calculate_winrate_route(tMatch, tWr, wrReq):
  return MLBB_in_game.calculate_winrate_response(tMatch, tWr, wrReq)


# to know win and lose by total match and winrate. total_matches_played/win_rate (80 --> 80.0)
# example https://mlbb-api.ridwaanhall.repl.co/wr-winlose/100/75.5
@app.route('/wr-winlose/<int:total_matches_played>/<float:win_rate>',
           methods=['GET'])
def calculate_wr_winlose(total_matches_played, win_rate):
  return MLBB_in_game.wr_winlose(total_matches_played, win_rate)


# home mpl id redirect to standings
@app.route('/mpl-id', methods=['GET'])
def get_mpl_id():
  return redirect(url_for('get_mpl_id_standings'))


# to know transfer player in mpl id
@app.route('/mpl-id/transfer', methods=['GET'])
@app.route('/mpl-id/transfer.xml', methods=['GET'])
def get_mpl_id_transfer_xml():
  transfer_data = MPL_ID.transfer()
  return JSONtoXML.convert_json_to_xml(transfer_data)


@app.route('/mpl-id/transfer.json', methods=['GET'])
def get_mpl_id_transfer_json():
  return MPL_ID.transfer()


# to know standings in mpl id
@app.route('/mpl-id/standings', methods=['GET'])
@app.route('/mpl-id/standings.xml', methods=['GET'])
def get_mpl_id_standings_xml():
  standings_data = MPL_ID.standings()
  return JSONtoXML.convert_json_to_xml(standings_data)


@app.route('/mpl-id/standings.json', methods=['GET'])
def get_mpl_id_standings_json():
  return MPL_ID.standings()


# to know any teams who play in mpl id
@app.route('/mpl-id/teams', methods=['GET'])
def get_mpl_id_teams():
  return redirect(url_for('get_mpl_id_teams_xml'))


@app.route('/mpl-id/teams.json', methods=['GET'])
def get_mpl_id_teams_json():
  return MPL_ID.teams()


@app.route('/mpl-id/teams.xml', methods=['GET'])
def get_mpl_id_teams_xml():
  teams_data = MPL_ID.teams()
  return JSONtoXML.convert_json_to_xml(teams_data)


# to know player name in mpl id by team
@app.route('/mpl-id/teams/<string:team_name>', methods=['GET'])
def get_mpl_id_team_players(team_name):
  return MPL_ID.team_players(team_name)


@app.route('/mpl-id/teams/<string:team_name>.xml', methods=['GET'])
def get_mpl_id_team_players_xml(team_name):
  team_players = MPL_ID.team_players(team_name)
  return JSONtoXML.convert_json_to_xml(team_players)


# to know statistics of teams in mpl id
@app.route('/mpl-id/statistics-teams', methods=['GET'])
def get_teams_statistics():
  return redirect(url_for('get_teams_statistics_xml'))


@app.route('/mpl-id/statistics-.json', methods=['GET'])
def get_teams_statistics_json():
  return MPL_ID.statistics_teams()


@app.route('/mpl-id/statistics-teams.xml', methods=['GET'])
def get_teams_statistics_xml():
  teams_stats_data = MPL_ID.statistics_teams()
  return JSONtoXML.convert_json_to_xml(teams_stats_data)


# to know statistics of players in mpl id
@app.route('/mpl-id/statistics-players', methods=['GET'])
def get_players_statistics():
  return redirect(url_for('get_players_statistics_json'))


@app.route('/mpl-id/statistics-players.json', methods=['GET'])
def get_players_statistics_json():
  return MPL_ID.statistics_players()


@app.route('/mpl-id/statistics-players.xml', methods=['GET'])
def get_players_statistics_xml():
  players_stats_data = MPL_ID.statistics_players()
  return JSONtoXML.convert_json_to_xml(players_stats_data)


# to know statistics of heroes winrate pick in mpl id
@app.route('/mpl-id/statistics-heroes', methods=['GET'])
def get_heroes_statistics():
  return redirect(url_for('get_heroes_statistics_xml'))


@app.route('/mpl-id/statistics-heroes.json', methods=['GET'])
def get_heroes_statistics_json():
  return MPL_ID.statistics_heroes()


@app.route('/mpl-id/statistics-heroes.xml', methods=['GET'])
def get_heroes_statistics_xml():
  heroes_stats_data = MPL_ID.statistics_heroes()
  return JSONtoXML.convert_json_to_xml(heroes_stats_data)


# to know player who use by hero pools
@app.route('/mpl-id/statistics-hero-pools', methods=['GET'])
def get_hero_pools_statistics():
  return redirect(url_for('get_hero_pools_statistics_xml'))


@app.route('/mpl-id/statistics-hero-pools.json', methods=['GET'])
def get_hero_pools_statistics_json():
  return MPL_ID.statistics_hero_pools()


@app.route('/mpl-id/statistics-hero-pools.xml', methods=['GET'])
def get_hero_pools_statistics_xml():
  hero_pools_stats_data = MPL_ID.statistics_hero_pools()
  return JSONtoXML.convert_json_to_xml(hero_pools_stats_data)


# to know hero who use by player pools
@app.route('/mpl-id/statistics-player-pools', methods=['GET'])
def get_player_pools_statistics():
  return redirect(url_for('get_player_pools_statistics_xml'))


@app.route('/mpl-id/statistics-player-pools.json', methods=['GET'])
def get_player_pools_statistics_json():
  return MPL_ID.statistics_player_pools()


@app.route('/mpl-id/statistics-player-pools.xml', methods=['GET'])
def get_player_pools_statistics_xml():
  player_pools_stats_data = MPL_ID.statistics_player_pools()
  return JSONtoXML.convert_json_to_xml(player_pools_stats_data)


# to know mvp player
@app.route('/mpl-id/statistics-player-mvp', methods=['GET'])
def get_player_mvp_statistics():
  return redirect(url_for('get_player_mvp_statistics_xml'))


@app.route('/mpl-id/statistics-player-mvp.json', methods=['GET'])
def get_player_mvp_statistics_json():
  return MPL_ID.statistics_player_mvp()


@app.route('/mpl-id/statistics-player-mvp.xml', methods=['GET'])
def get_player_mvp_statistics_xml():
  player_mvp_stats_data = MPL_ID.statistics_player_mvp()
  return JSONtoXML.convert_json_to_xml(player_mvp_stats_data)
