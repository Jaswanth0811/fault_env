from fastapi import FastAPI
from models import Action, StepResult
from my_env import FaultEnv

app = FastAPI(title="Industrial Machine Fault Diagnosis Environment")

# Create a global environment instance
env = FaultEnv()

@app.post("/reset", response_model=StepResult)
async def reset_env():
    return await env.reset()

@app.post("/step", response_model=StepResult)
async def step_env(action: Action):
    return await env.step(action)

@app.get("/state")
async def get_state():
    return await env.state()
