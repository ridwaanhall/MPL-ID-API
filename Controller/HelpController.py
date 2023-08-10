import json


class HelpController:

  @staticmethod
  def global_help():
    with open('json/help.json', 'r') as json_file:
      data = json.load(json_file)
    return data
  
  @staticmethod
  def check_username_help():
    with open('json/check_username.json', 'r') as json_file:
      data = json.load(json_file)
    return data

  @staticmethod
  def calculate_winrate_help():
    with open('json/winrate_target.json', 'r') as json_file:
      data = json.load(json_file)
    return data