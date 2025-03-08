from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class Activity(BaseModel):
    types: List[str] = Field(default_factory=list)
    level: Optional[str] = None
    limits: List[str] = Field(default_factory=list)

    class Config:
        extra = 'allow'


class Person(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    food_preference: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    license: Optional[bool] = None
    activity: Activity = Field(default_factory=Activity)

    class Config:
        extra = 'allow'


class Trip(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    activities: List[str] = Field(default_factory=list)
    people: List[Person] = Field(default_factory=list)
    season: Optional[str] = None
    transport: Optional[str] = None
    budget: Optional[str] = None
    notes: Dict[str, str] = Field(default_factory=dict)

    class Config:
        extra = 'allow'