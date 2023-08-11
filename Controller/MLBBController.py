import requests
from bs4 import BeautifulSoup


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
        "name": result.get('name'),
        "ok": True,
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
    result_num = MLBBController.calculate_winrate(tMatch, tWr, wrReq)
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
    import requests
    from bs4 import BeautifulSoup

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
