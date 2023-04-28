from typing import List
from fastapi import HTTPException, Query
from datetime import datetime
from pydantic import BaseModel,Field


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    events: List["Event"] = []

    class Config:
        orm_mode = True
class PlayerGet(PlayerBase):
    id: int
    


    
class EventCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    detail: str = Field(..., min_length=1, max_length=50)

class EventResponse(BaseModel):
    id: int

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

    _max_id = 0

class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class PlayerResponse(BaseModel):
    id: int
    name: str

class PlayerInfo(BaseModel):
    id: int
    name: str
    events: List[Event] = []
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.__class__._max_id += 1
            self.id = self.__class__._max_id

    @classmethod
    def create_event(cls, type: str, detail: str, timestamp: datetime, player_id: int):
        return cls(id=None, type=type, detail=detail, timestamp=timestamp, player_id=player_id)
            
    class Config:
        orm_mode = True


Player.update_forward_refs()





