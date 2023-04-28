from datetime import datetime
from typing import List, Optional
from models import Player, Event, PlayerCreate, PlayerInfo, PlayerResponse,PlayerGet, EventCreate,EventResponse
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

VALID_EVENT_TYPES = ["level_started", "level_solved","string"]
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

app = FastAPI()
metadata = MetaData()

events = [
   
]

players = [
   
]

@app.get("/players", response_model=List[PlayerGet])
def get_players():
    
    return players


@app.post("/players", response_model=PlayerResponse, status_code=201)
async def create_player(player_create: PlayerCreate):
    new_player = Player(id=len(players) + 1, name=player_create.name)
    players.append(new_player)
    return {"id": new_player.id, "name": new_player.name}

@app.get("/players/{id}", response_model=PlayerInfo)
async def get_player(id: int):
    player = next((p for p in players if p.id == id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_events = [e for e in events if e.player_id == id]
    return PlayerInfo(id=player.id, name=player.name, events=player_events)

@app.get("/players/{id}/events", response_model=List[Event])
async def get_player_events(id: int, type: str = None):
    player = next((p for p in players if p.id == id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if type and type not in VALID_EVENT_TYPES:
            raise HTTPException(status_code=400, detail="Invalid event type")
    player_events = player.events
    if type:
        player_events = [e for e in player_events if e.type == type]
    return [
        Event(
            id=e.id,
            type=e.type,
            detail=e.detail,
            player_id=e.player_id,
            timestamp=e.timestamp
        ).dict()
        for e in player_events
    ]
    
@app.post("/players/{id}/events", response_model=EventResponse, status_code=201)
async def create_event(event_create: EventCreate, player_id: int):
    player = next((p for p in players if p.id == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    
    used_ids = [e.id for e in player.events]
    new_id = max(used_ids) + 1 if used_ids else 1
    
    new_event = Event(id=new_id, type=event_create.type, detail=event_create.detail, timestamp=datetime.now(), player_id=player_id)
    player.events.append(new_event)
    events.append(new_event)
    return {"id": new_event.id}
@app.get("/events", response_model=List[Event])
async def get_events(type: Optional[str] = None):
    events_filtered = events
    if type and type not in VALID_EVENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid event type")
    if type:
        events_filtered = [e for e in events_filtered if e.type == type]
    return [
        Event(
            id=e.id,
            type=e.type,
            detail=e.detail,
            player_id=e.player_id,
            timestamp=e.timestamp
        ).dict()
        for e in events_filtered
    ]