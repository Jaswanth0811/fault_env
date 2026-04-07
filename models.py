from pydantic import BaseModel
from typing import Optional


class Observation(BaseModel):
    temperature: float
    vibration: Optional[float] = None
    noise: float


class Action(BaseModel):
    action_type: str
    target: str
    decision: str


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict