import json
import os

def save_interview(user, role, level, score):

    file = f"data/{user}_history.json"

    data=[]

    if os.path.exists(file):
        with open(file,"r") as f:
            data=json.load(f)

    data.append({
        "role":role,
        "level":level,
        "score":score
    })

    with open(file,"w") as f:
        json.dump(data,f)