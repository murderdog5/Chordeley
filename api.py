from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database as db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/progressions")
def get_progressions():
    return db.get_all_progressions()

@app.post("/save")
def save_progression(data: dict):
    db.add_progression(
        data["title"],
        data["chords"],
        data.get("key_root", ""),
        data.get("memo", ""),
        data.get("tags", ""),
    )
    return {"status": "ok"}

@app.delete("/progressions/{progression_id}")
def delete_progression(progression_id: int):
    db.delete_progression(progression_id)
    return{"status":"ok"}