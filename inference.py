import os
import requests
from openai import OpenAI

# 🔑 Set your API key (or use environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE = "http://localhost:7860"


def llm_agent(obs):
    prompt = f"""
You are an industrial machine expert.

Sensor Data:
Temperature: {obs['temperature']}
Vibration: {obs['vibration']}
Noise: {obs['noise']}

Choose the best action in JSON format ONLY:

{{
  "action_type": "inspect or diagnose or repair",
  "target": "motor or bearing or cooling or normal or bearing_fault or overheating",
  "decision": "replace or monitor or ignore"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a machine fault diagnosis AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        action = eval(content)  # simple parsing
    except:
        # fallback safe action
        action = {
            "action_type": "inspect",
            "target": "motor",
            "decision": "monitor"
        }

    return action


print("[START] task=fault env=fault_env model=openai")

res = requests.post(f"{BASE}/reset").json()
obs = res["observation"]

rewards = []

for step in range(1, 6):
    action = llm_agent(obs)

    res = requests.post(f"{BASE}/step", json=action).json()

    reward = res.get("reward", 0.0)
    done = res.get("done", True)

    rewards.append(reward)

    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    if done:
        break

    obs = res["observation"]

score = max(0.0, min(1.0, sum(rewards)))
success = score > 0.5

print(f"[END] success={str(success).lower()} steps={step} score={score:.2f} rewards={','.join(map(str,rewards))}")