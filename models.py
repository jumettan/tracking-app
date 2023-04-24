from typing import List
from fastapi import HTTPException, Query
from datetime import datetime
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    events: List["Event"] = []

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    type: str
    detail: str


class EventCreate(EventBase):
    pass

class Event(BaseModel):
    id: int
    type: str
    detail: str
    timestamp: datetime
    player_id: int
    
    Types = ["level_started", "level_solved"]
    
    class Config:
        orm_mode = True


Player.update_forward_refs()

players = {
    1: Player(id=1, name="Reijo", events=[Event(id=1, type="level_started", detail="level_1212_001", timestamp=datetime(2023, 1, 13, 12, 1, 22), player_id=1)])
}
# GET /players/{id}
def get_player(id: int):
    if id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    player = players[id]
    events = [{"id": e.id, "type": e.type, "detail": e.detail, "timestamp": e.timestamp, "player_id": e.player_id} for e in player.events]
    return {"id": player.id, "name": player.name, "events": events}

# POST /events?player_id={player_id}
def create_event(player_id: int, event: EventCreate):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    event_dict = event.dict()
    event_dict["id"] = len(players[player_id].events) + 1
    event_dict["timestamp"] = datetime.now()
    event_dict["player_id"] = player_id
    players[player_id].events.append(Event(**event_dict))
    return {"message": "Event created successfully"}

# GET /players/{id}/events
def get_player_events(id: int, type: str = None):
    if id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    player = players[id]
    if not player.events:
        return []
    if type:
        if type not in [e.type for e in player.events]:
            raise HTTPException(status_code=400, detail="Invalid event type")
        events = [{"id": e.id, "type": e.type, "detail": e.detail, "timestamp": e.timestamp, "player_id": e.player_id} for e in player.events if e.type == type]
    else:
        events = [{"id": e.id, "type": e.type, "detail": e.detail, "timestamp": e.timestamp, "player_id": e.player_id} for e in player.events]
    return events