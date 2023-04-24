from datetime import datetime
from typing import List, Optional, Union
from models import Player
from databases import Database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

app = FastAPI()
metadata = MetaData()

players = [
   
]

events = [
    
]

@app.get("/players", response_model=List[Player])
def get_players():
    
    return players

class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class PlayerResponse(BaseModel):
    id: int

@app.post("/players", response_model=PlayerResponse, status_code=201)
async def create_player(player_create: PlayerCreate):
    new_player = Player(id=len(players) + 1, name=player_create.name)
    players.append(new_player)
    return {"id": new_player.id}

@app.get("/players/{id}", response_model=Player)
async def get_player(id: int):
    player = next((p for p in players if p.id == id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_events = [e for e in events if e["player_id"] == id]
    return {"id": player.id, "name": player.name, "events": player_events}

class EventCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    detail: str = Field(..., min_length=1, max_length=50)

class EventResponse(BaseModel):
    id: int

@app.post("/events", response_model=EventResponse, status_code=201)
async def create_event(event_create: EventCreate, player_id: int):
    player = next((p for p in players if p.id == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    new_event = {
        "id": len(events) + 1,
        "type": event_create.type,
        "detail": event_create.detail,
        "timestamp": str(datetime.now()),
        "player_id": player_id,
    }
    events.append(new_event)
    return {"id": new_event["id"]}

