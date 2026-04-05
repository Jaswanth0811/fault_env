from pydantic import BaseModel
from typing import Any, Dict

class Observation(BaseModel):
    temperature: float
    vibration: float
    noise: float

class Action(BaseModel):
    diagnosis: str
    action: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
