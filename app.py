from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import numpy as np
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# Load your model
model1 = pickle.load(open("xgb_tennis_model.pkl", "rb"))

class InputData(BaseModel):
    surface: int
    player_one_ht: float  # Height as float
    player_two_ht: float  # Height as float
    player_one_age: float  # Age as float
    player_two_age: float  # Age as float
    player_one_hand: int
    player_two_hand: int
    player_one_ace: int
    player_two_ace: int
    player_one_df: float  # Double faults as float
    player_two_df: float  # Double faults as float
    player_one_break_point_saved: int
    player_two_break_point_saved: int
    player_one_break_point_faced: int
    player_two_break_point_faced: int
    player_one_rank: float  # Rank as float
    player_two_rank: float  # Rank as float
    player_one_rank_points: float  # Rank points as float
    player_two_rank_points: float  # Rank points as float
    player_one_win_percentage: float  # Win percentage as float
    player_two_win_percentage: float  # Win percentage as float

@app.post('/prediction')
def get_prediction(data: InputData):
    try:
        received = pd.DataFrame([data.dict()])

        # Ensuring columns are in the expected order
        cols_new = ['surface', 'player_one_ht', 'player_two_ht', 'player_one_age', 
                    'player_two_age', 'player_one_hand', 'player_two_hand', 
                    'player_one_ace', 'player_two_ace', 'player_one_df', 
                    'player_two_df', 'player_one_break_point_saved', 
                    'player_two_break_point_saved', 'player_one_break_point_faced', 
                    'player_two_break_point_faced', 'player_one_rank', 
                    'player_two_rank', 'player_one_rank_points', 
                    'player_two_rank_points', 'player_one_win_percentage', 
                    'player_two_win_percentage']
        
        received = received[cols_new]
        
        # Making prediction
        pred_name = model1.predict(received)[0]
        
        # Getting probabilities
        Prob = model1.predict_proba(received) * 100
        probability_percent = {
            "Loss": round(float(Prob[0][0]), 2),
            "Win": round(float(Prob[0][1]), 2)
        }
        decimal_odds = {
            "Loss_odds": round(float(100 / Prob[0][0]), 2),
            "Win_odds": round(float(100 / Prob[0][1]), 2)
        }

        return {
            'prediction': int(pred_name),  # Ensure this is a native Python int
            'probability_percent': probability_percent,
            "predicted_decimal_odds": decimal_odds
        }
    
    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
