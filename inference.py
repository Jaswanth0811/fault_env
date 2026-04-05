import asyncio
import os
from typing import List

import requests

API_BASE = os.getenv("API_BASE_URL", "http://localhost:7860")
TASK_NAME = "fault_diagnosis"
BENCHMARK = "fault_env"
MODEL_NAME = os.getenv("MODEL_NAME", "local-test")

MAX_STEPS = 1


def log_start():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(success, steps, score, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


def simple_agent(obs):
    # Simple rule-based logic
    if obs["temperature"] > 90:
        return {"diagnosis": "overheating", "action": "cool_system"}
    elif obs["vibration"] > 0.7:
        return {"diagnosis": "bearing_fault", "action": "replace_bearing"}
    else:
        return {"diagnosis": "normal", "action": "no_action"}


async def main():
    log_start()

    rewards = []
    steps = 0

    try:
        # RESET
        res = requests.post(f"{API_BASE}/reset").json()
        obs = res["observation"]

        for step in range(1, MAX_STEPS + 1):
            action = simple_agent(obs)

            res = requests.post(f"{API_BASE}/step", json=action).json()

            reward = res.get("reward", 0.0)
            done = res.get("done", True)

            rewards.append(reward)
            steps = step

            log_step(step, action, reward, done)

            if done:
                break

        score = max(0.0, min(1.0, sum(rewards)))
        success = score > 0.5

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)
        score = 0.0
        success = False

    log_end(success, steps, score, rewards)


if __name__ == "__main__":
    asyncio.run(main())
