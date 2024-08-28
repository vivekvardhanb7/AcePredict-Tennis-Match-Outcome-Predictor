import requests
import json

# Load data from backtesting.json
with open('backtesting.json', 'r') as f:
    team_details = json.load(f)

print(f"Number of records: {len(team_details)}")

# Function to get predictions from the FastAPI server
def test2(team_details):
    dataList = []
    for info in team_details:
        url = "http://127.0.0.1:8000/prediction"

        # Keep fields as floats
        player_one_ht = float(info["player_one_ht"])
        player_two_ht = float(info["player_two_ht"])
        player_one_age = float(info["player_one_age"])
        player_two_age = float(info["player_two_age"])
        player_one_win_percentage = float(info["player_one_win_percentage"])
        player_two_win_percentage = float(info["player_two_win_percentage"])
        player_one_rank = float(info["player_one_rank"])
        player_two_rank = float(info["player_two_rank"])
        player_one_rank_points = float(info["player_one_rank_points"])
        player_two_rank_points = float(info["player_two_rank_points"])
        player_one_df = float(info["player_one_df"])
        player_two_df = float(info["player_two_df"])

        if player_one_win_percentage == 0 or player_two_win_percentage == 0:
            dataList.append(info)
        else:
            payload = json.dumps({
                "surface": info["surface"],
                "player_one_ht": player_one_ht,
                "player_two_ht": player_two_ht,
                "player_one_age": player_one_age,
                "player_two_age": player_two_age,
                "player_one_hand": info["player_one_hand"],
                "player_two_hand": info["player_two_hand"],
                "player_one_ace": info["player_one_ace"],
                "player_two_ace": info["player_two_ace"],
                "player_one_df": player_one_df,
                "player_two_df": player_two_df,
                "player_one_break_point_saved": info["player_one_break_point_saved"],
                "player_two_break_point_saved": info["player_two_break_point_saved"],
                "player_one_break_point_faced": info["player_one_break_point_faced"],
                "player_two_break_point_faced": info["player_two_break_point_faced"],
                "player_one_rank": player_one_rank,
                "player_two_rank": player_two_rank,
                "player_one_rank_points": player_one_rank_points,
                "player_two_rank_points": player_two_rank_points,
                "player_one_win_percentage": player_one_win_percentage,
                "player_two_win_percentage": player_two_win_percentage
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                info.update(data)
                dataList.append(info)
            else:
                print(f"Failed to get prediction. Status code: {response.status_code}, Response: {response.text}")

    return dataList

# Get predictions and save the updated data to a new file
raw_data_1 = test2(team_details)

with open("tennis_predictions.json", 'w') as f:
    f.write(json.dumps(raw_data_1, indent=3))
