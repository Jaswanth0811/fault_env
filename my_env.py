import random
import asyncio
from typing import Dict, Any

from models import Observation, Action, StepResult

class FaultEnv:
    def __init__(self):
        self._current_fault = "normal"
        self._temp = 75.0
        self._vib = 0.5
        self._noise = 50.0
        self._steps = 0
        self._max_steps = 20
        self._done = False
        
    async def reset(self) -> StepResult:
        self._done = False
        self._steps = 0
        self._current_fault = random.choice(["normal", "bearing_fault", "overheating"])
        
        # Base healthy sensor values
        self._temp = random.uniform(65.0, 80.0)
        self._vib = random.uniform(0.2, 0.6)
        self._noise = random.uniform(40.0, 60.0)
            
        current_obs = Observation(temperature=self._temp, vibration=self._vib, noise=self._noise)
        
        return StepResult(
            observation=current_obs,
            reward=0.0,
            done=self._done,
            info={"fault_type": self._current_fault, "steps": self._steps}
        )
        
    async def step(self, action: Action) -> StepResult:
        if self._done:
            return StepResult(
                observation=Observation(temperature=self._temp, vibration=self._vib, noise=self._noise),
                reward=0.0,
                done=True,
                info={"error": "Episode already done"}
            )
            
        self._steps += 1
        reward = 1.0  # +1 reward for every step survived in safe state
        
        # Physics Engine Simulation: Apply actions first
        if action.action == "cool_system":
            self._temp = max(60.0, self._temp - 15.0)
            reward -= 0.1 # Slight penalty for using cooling energy
        elif action.action == "replace_bearing":
            self._vib = max(0.2, self._vib - 0.5)
            self._noise = max(40.0, self._noise - 20.0)
            reward -= 0.5 # Higher penalty for expensive downtime repairs
            
        # Simulate environment dynamics based on hidden fault
        if self._current_fault == "overheating":
            self._temp += random.uniform(5.0, 10.0)
        elif self._current_fault == "bearing_fault":
            self._vib += random.uniform(0.1, 0.3)
            self._noise += random.uniform(5.0, 10.0)
        
        # Add natural noise to all sensors
        self._temp += random.uniform(-1.0, 1.0)
        self._vib += random.uniform(-0.05, 0.05)
        self._noise += random.uniform(-2.0, 2.0)
        
        # Check critical thresholds (Machine Breakage)
        broke = False
        if self._temp > 120.0 or self._vib > 2.0 or self._noise > 100.0:
            broke = True
            reward = -10.0
            
        if broke or self._steps >= self._max_steps:
            self._done = True
            
        current_obs = Observation(temperature=self._temp, vibration=self._vib, noise=self._noise)
        
        return StepResult(
            observation=current_obs,
            reward=reward,
            done=self._done,
            info={"broke": broke, "fault": self._current_fault, "steps": self._steps}
        )
        
    async def state(self) -> Dict[str, Any]:
        return {
            "current_fault": self._current_fault,
            "steps": self._steps,
            "done": self._done,
            "temperature": self._temp,
            "vibration": self._vib,
            "noise": self._noise
        }
        
    async def close(self):
        pass
