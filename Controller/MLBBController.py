import requests


class MLBBController:

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
