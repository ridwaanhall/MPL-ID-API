import requests
from bs4 import BeautifulSoup
from flask import Response


class JSONtoXML:

  @staticmethod
  def convert_json_to_xml(json_data):
    from dicttoxml import dicttoxml
    xml_data = dicttoxml(json_data,
                         attr_type=False)  # attr_type is to hide type or not
    response = Response(xml_data, content_type='application/xml')
    return response


class MLBB_in_game:

  @staticmethod
  def check_username(user_id, zone_id):
    url = "https://mainlagiaja.com/ajax/games/check/mobile-legend"
    payload = {"user_id": user_id, "zone_id": zone_id}

    response = requests.post(
      url,
      data=payload,
      headers={"Content-Type": "application/x-www-form-urlencoded"})
    result = response.json()

    if result.get('ok'):
      formatted_response = {
        "msg": "data player ditemukan",
        "username": result.get('name'),
        "ok": True,
        "game":"Mobile Legends Bang Bang (MLBB)",
        "user_id": user_id,
        "zone_id": zone_id
      }
    else:
      formatted_response = {
        "msg": "Invalid User ID Or Zone ID",
        "ok": False,
        "user_id": user_id,
        "zone_id": zone_id
      }

    return formatted_response

  @staticmethod
  def calculate_winrate_response(tMatch, tWr, wrReq):
    result_num = MLBB_in_game.calculate_winrate(tMatch, tWr, wrReq)
    response_text = f"You need about {result_num} win(s) without losing (WS/win streak) to get a win rate of {wrReq}%"
    response = {
      "2_total_match": tMatch,
      "3_total_wr": tWr,
      "4_winrate_target": wrReq,
      "5_response": response_text
    }
    return response

  @staticmethod
  def calculate_winrate(tMatch, tWr, wrReq):
    tWin = tMatch * (tWr / 100)
    tLose = tMatch - tWin
    sisaWr = 100 - wrReq
    wrResult = 100 / sisaWr
    seratusPersen = tLose * wrResult
    final = seratusPersen - tMatch
    return round(final)

  @staticmethod
  def wr_winlose(total_matches_played, win_rate):
    matches_won = (win_rate / 100) * total_matches_played
    matches_lost = total_matches_played - matches_won
    response = {
      "total_match":
      total_matches_played,
      "winrate":
      win_rate,
      "matches_won":
      matches_won,
      "matches_lost":
      matches_lost,
      "message":
      f"with a total of {total_matches_played} matche(s) and a win rate of {win_rate}%, you have a total of {matches_won} win(s) and {matches_lost} lose(s)"
    }
    return response


class MPL_ID:

  @staticmethod
  def transfer():

    url = "https://id-mpl.com/transfer"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      data_table = soup.find("table", id="table-transfers")

      if data_table:
        transfer_data = []

        rows = data_table.find_all("tr")
        for row in rows[1:]:
          cells = row.find_all("td")
          if len(cells) == 5:
            date = cells[0].get_text(strip=True)
            player = cells[1].get_text(strip=True)
            role = cells[2].get_text(strip=True)
            from_team = ' '.join(cells[3].stripped_strings)
            to_team = ' '.join(cells[4].stripped_strings)

            from_team = from_team.replace('\n', '').replace(' ', '')
            to_team = to_team.replace('\n', '').replace(' ', '')

            transfer_data.append({
              "Date": date,
              "Player": player,
              "Role": role,
              "From": from_team,
              "To": to_team
            })

        return transfer_data
      else:
        return "Data table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def standings():

    url = "https://id-mpl.com/"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      data_table = soup.find("table", class_="table-standings")

      if data_table:
        standings_data = []

        rows = data_table.find_all("tr")
        for row in rows[1:]:
          cells = row.find_all("td")
          if len(cells) == 6:
            team_info = cells[0].find(
              "div",
              class_="d-flex flex-row justify-content-start align-items-center"
            )

            team_rank = team_info.find("div",
                                       class_="team-rank").get_text(strip=True)
            team_logo = team_info.find("img")["src"]
            short_name = team_info.find(
              "span", class_="d-lg-none").get_text(strip=True)
            long_name = team_info.find(
              "span", class_="d-none d-lg-block").get_text(strip=True)

            # Extract and format match record
            match_wl = cells[1].get_text(strip=True)
            match_wl = match_wl.replace(' ', '').replace('\n', '')

            match_rate = cells[2].get_text(strip=True)
            game_wl = cells[3].get_text(strip=True)

            # Extract and format game record
            game_wl = game_wl.replace(' ', '').replace('\n', '')

            game_rate = cells[4].get_text(strip=True)
            agg_points = cells[5].get_text(strip=True)

            standings_data.append({
              "No": team_rank,
              "Team Logo": team_logo,
              "Short Name": short_name,
              "Long Name": long_name,
              "Match W-L": match_wl,
              "Match Rate": match_rate,
              "Game W-L": game_wl,
              "Game Rate": game_rate,
              "Agg Points": agg_points
            })

        return standings_data
      else:
        return "Data table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def teams():

    url = "https://id-mpl.com/teams"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      content_wrap = soup.find("div", class_="content-wrap")

      if content_wrap:
        h4_element = content_wrap.find("h4", class_="text-center")

        if h4_element and h4_element.get_text(strip=True) == "TEAMS":
          team_data = []

          team_card_outers = content_wrap.find_all("div",
                                                   class_="team-card-outer")

          for team_card_outer in team_card_outers:
            team_image = team_card_outer.find(
              "div", class_="team-image").find("img")["src"]
            team_name_element = team_card_outer.find("div", class_="team-name")

            if team_name_element:
              team_name = team_name_element.get_text(strip=True)
              team = {"Team Image": team_image, "Team Name": team_name}
              team_data.append(team)

          return team_data
        else:
          return "H4 element not found or TEAMS text not present."
      else:
        return "Content wrap not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def team_players(team_name):

    url = f"https://id-mpl.com/team/{team_name}"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")

      team_name = soup.find(
        "div", class_="col-xs-12 team-name").find("h2").get_text(strip=True)
      team_logo = soup.find("div",
                            class_="col-xs-12 team-logo").find("img")["src"]
      player_divs = soup.find_all("div", class_="col-md-3 col-xs-6")

      player_data = []

      for player_div in player_divs:
        player_image_bg = player_div.find(
          "div", class_="player-image-bg").find("img")["src"]
        player_name = player_div.find(
          "div", class_="player-name").get_text(strip=True)

        player_info = {
          "Player Image Background": player_image_bg,
          "Player Name": player_name
        }
        player_data.append(player_info)

      match_team_divs = soup.find_all("div", class_="match-team")

      match_team_data = []

      for match_team_div in match_team_divs:
        match_logo_first = match_team_div.find(
          "div", class_="match-logo").get_text(strip=True)
        match_score = match_team_div.find(
          "div",
          class_="match-score-team").find("div",
                                          class_="score").get_text(strip=True)
        match_logo_second = match_team_div.find_all(
          "div", class_="match-logo")[1].get_text(strip=True)
        match_detail = match_team_div.find(
          "div", class_="match-detail").find_all("div", class_="col-xs-12")
        week = match_detail[0].get_text(strip=True)
        date_time = match_detail[1].get_text(strip=True)
        match_status = match_team_div.find(
          "div", class_="match-status-wl").get_text(strip=True)

        match_team_info = {
          "Match Logo First": match_logo_first,
          "Match Score": match_score,
          "Match Logo Second": match_logo_second,
          "Match Detail": {
            "Week": week,
            "Date and Time": date_time,
            "Match Status": match_status
          }
        }
        match_team_data.append(match_team_info)

      team_info = {
        "Team Name": team_name,
        "Team Logo": team_logo,
        "Team Players": player_data,
        "Match Team": match_team_data
      }

      return team_info
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_teams():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      data_table = soup.find("table", id="table-team-statistics")

      if data_table:
        team_stats = []
        rows = data_table.find_all("tr")
        for row in rows[1:]:
          cells = row.find_all("td")
          if len(cells) == 9:
            team_info = cells[0]

            team_logo = team_info.find(
              "div", class_="team-logo me-2").find("img")["src"]
            short_name = team_info.find(
              "span", class_="d-lg-none").get_text(strip=True)
            long_name = team_info.find(
              "span", class_="d-none d-lg-block").get_text(strip=True)

            kills = cells[1].get_text(strip=True)
            deaths = cells[2].get_text(strip=True)
            assists = cells[3].get_text(strip=True)
            gold = cells[4].get_text(strip=True)
            damage = cells[5].get_text(strip=True)
            lord = cells[6].get_text(strip=True)
            tortoise = cells[7].get_text(strip=True)
            tower = cells[8].get_text(strip=True)

            team_stat = {
              "Team Logo": team_logo,
              "Short Name": short_name,
              "Long Name": long_name,
              "Kills": kills,
              "Deaths": deaths,
              "Assists": assists,
              "Gold": gold,
              "Damage": damage,
              "Lord": lord,
              "Tortoise": tortoise,
              "Tower": tower
            }
            team_stats.append(team_stat)

        return team_stats
      else:
        return "Data table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_players():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      player_table = soup.find("table", class_="table-players-statistics")

      if player_table:
        player_stats = []
        rows = player_table.find_all("tr")
        for row in rows[1:]:
          cells = row.find_all("td")
          if len(cells) == 11:
            player_name_div = cells[0].find("div", class_="player-name")
            player_name = player_name_div.find("b").get_text(strip=True)
            team_logo_img = cells[0].find("img")["src"]

            lanes = cells[1].get_text(strip=True)
            total_games = cells[2].get_text(strip=True)
            total_kills = cells[3].get_text(strip=True)
            avg_kills = cells[4].get_text(strip=True)
            total_deaths = cells[5].get_text(strip=True)
            avg_deaths = cells[6].get_text(strip=True)
            total_assists = cells[7].get_text(strip=True)
            avg_assists = cells[8].get_text(strip=True)
            avg_kda = cells[9].get_text(strip=True)
            kill_participation = cells[10].get_text(strip=True)

            player_stat = {
              "Player Name": player_name,
              "Team Logo Image": team_logo_img,
              "Lanes": lanes,
              "Total Games": total_games,
              "Total Kills": total_kills,
              "Avg Kills": avg_kills,
              "Total Deaths": total_deaths,
              "Avg Deaths": avg_deaths,
              "Total Assists": total_assists,
              "Avg Assists": avg_assists,
              "Avg KDA": avg_kda,
              "Kill Participation": kill_participation
            }
            player_stats.append(player_stat)

        return player_stats
      else:
        return "Player table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_heroes():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      heroes_table = soup.find("table", class_="table-heroes-statistics")

      if heroes_table:
        heroes_stats = []
        rows = heroes_table.find_all("tr", class_="row-heroes")
        for row in rows:
          cells = row.find_all("td")
          if len(cells) == 5:
            hero_name_div = cells[0].find("div", class_="hero-name")
            hero_name = hero_name_div.find("b").get_text(strip=True)
            hero_image = cells[0].find("img")["src"]

            pick = cells[1].get_text(strip=True)
            ban = cells[2].get_text(strip=True)
            win = cells[3].get_text(strip=True)
            win_rate = cells[4].get_text(strip=True)

            hero_stat = {
              "Hero Name": hero_name,
              "Hero Image": hero_image,
              "Pick": pick,
              "Ban": ban,
              "Win": win,
              "Win Rate": win_rate
            }
            heroes_stats.append(hero_stat)

        return heroes_stats
      else:
        return "Heroes table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_hero_pools():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      hero_pools_table = soup.find("table", class_="table-hero-pools")

      if hero_pools_table:
        hero_pools_stats = []
        rows = hero_pools_table.find_all("tr", class_="col-hero-pools")
        for row in rows:
          cells = row.find_all("td")
          if len(cells) == 4:
            player_info_div = cells[0].find(
              "div",
              class_="d-flex flex-row justify-content-start align-items-center"
            )
            player_name = player_info_div.find("b").get_text(strip=True)
            player_image = player_info_div.find("img")["src"]

            lanes = cells[1].get_text(strip=True)
            total = cells[2].get_text(strip=True)

            hero_pool_data = []
            hero_pool_div = cells[3].find("div", class_="hero-pool-outer")
            hero_pool_items = hero_pool_div.find_all(
              "div", class_="position-relative")
            for hero_pool_item in hero_pool_items:
              hero_image = hero_pool_item.find("img")["src"]
              hero_pick = hero_pool_item.find(
                "div", class_="hero-pool-pick").get_text(strip=True)
              hero_pool_count = hero_pool_item.find(
                "div", class_="hero-pool-count").get_text(strip=True)

              hero_pool_info = {
                "Hero Image": hero_image,
                "Hero Pick": hero_pick,
                "Hero Pool Count": hero_pool_count
              }
              hero_pool_data.append(hero_pool_info)

            player_hero_pool = {
              "Player Name": player_name,
              "Player Image": player_image,
              "Lanes": lanes,
              "Total": total,
              "Hero Pool": hero_pool_data
            }
            hero_pools_stats.append(player_hero_pool)

        return hero_pools_stats
      else:
        return "Hero Pools table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_player_pools():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      player_pools_table = soup.find("table", class_="table-player-pools")

      if player_pools_table:
        player_pools_stats = []
        rows = player_pools_table.find_all("tr", class_="col-player-pools")
        for row in rows:
          cells = row.find_all("td")
          if len(cells) == 3:
            hero_info_div = cells[0].find(
              "div",
              class_="d-flex flex-row justify-content-start align-items-center"
            )
            hero_name = hero_info_div.find("b").get_text(strip=True)
            hero_image = hero_info_div.find("img")["src"]

            total = cells[1].get_text(strip=True)

            player_pool_data = []
            player_pool_div = cells[2].find("div", class_="player-pool-outer")
            player_pool_items = player_pool_div.find_all(
              "div", class_="player-pool-card")
            for player_pool_item in player_pool_items:
              player_image = player_pool_item.find(
                "img", class_="player-pool-image")["src"]
              player_name = player_pool_item.find(
                "div", class_="player-pool-info").get_text(strip=True)
              player_pick = player_pool_item.find(
                "div", class_="player-pool-pick").get_text(strip=True)
              player_pool_count = player_pool_item.find(
                "div", class_="player-pool-count").get_text(strip=True)

              player_pool_info = {
                "Player Name": player_name,
                "Player Image": player_image,
                "Player Pick": player_pick,
                "Player Pool Count": player_pool_count
              }
              player_pool_data.append(player_pool_info)

            hero_player_pool = {
              "Hero Name": hero_name,
              "Hero Image": hero_image,
              "Total": total,
              "Player Pool": player_pool_data
            }
            player_pools_stats.append(hero_player_pool)

        return player_pools_stats
      else:
        return "Player Pools table not found on the page."
    else:
      return "Failed to retrieve the webpage."

  @staticmethod
  def statistics_player_mvp():

    url = "https://id-mpl.com/statistics"
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      mvp_table = soup.find("table", class_="table-mvp")

      if mvp_table:
        mvp_stats = []
        rows = mvp_table.find_all("tr")
        for row in rows[1:]:
          cells = row.find_all("td")
          if len(cells) == 3:
            rank = cells[0].find("div",
                                 class_="team-rank").get_text(strip=True)
            player_info_div = cells[1].find(
              "div",
              class_="d-flex flex-row justify-content-start align-items-center"
            )
            player_name = player_info_div.find("b").get_text(strip=True)
            player_image = player_info_div.find("img")["src"]

            mvp_points = cells[2].find("div",
                                       class_="mvp-point").get_text(strip=True)

            player_mvp_info = {
              "Rank": rank,
              "Player Name": player_name,
              "Player Image": player_image,
              "MVP Points": mvp_points
            }
            mvp_stats.append(player_mvp_info)

        return mvp_stats
      else:
        return "MVP Player table not found on the page."
    else:
      return "Failed to retrieve the webpage."
