from fastapi import FastAPI
from my_env import FaultEnv
from models import Action

app = FastAPI()
env = FaultEnv()


@app.post("/reset")
async def reset():
    return await env.reset()


@app.post("/step")
async def step(action: Action):
    return await env.step(action)


@app.get("/state")
async def state():
    return await env.state()