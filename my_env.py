import random
from models import Observation, Action, StepResult


class FaultEnv:
    def __init__(self):
        self.state_data = None
        self.done = False
        self.step_count = 0
        self.max_steps = 5

    async def reset(self):
        self.state_data = {
            "temperature": random.randint(60, 80),
            "vibration": round(random.uniform(0.2, 0.6), 2),
            "noise": random.randint(40, 70),
            "fault": random.choice(["normal", "bearing_fault", "overheating"])
        }

        self.done = False
        self.step_count = 0

        return StepResult(
            observation=self._get_observation(),
            reward=0.0,
            done=False,
            info={}
        )

    def _get_observation(self):
        # Safe partial observability
        vib = self.state_data["vibration"]
        if random.random() < 0.3:
            vib = None

        return Observation(
            temperature=float(self.state_data["temperature"]),
            vibration=vib,
            noise=float(self.state_data["noise"])
        )

    async def step(self, action: Action):
        if self.done:
            return StepResult(
                observation=self._get_observation(),
                reward=0.0,
                done=True,
                info={"error": "Episode already done"}
            )

        reward = 0.0
        self.step_count += 1
        fault = self.state_data["fault"]

        # 🔥 SAFE dynamic updates
        if fault == "overheating":
            self.state_data["temperature"] += random.randint(1, 3)

        elif fault == "bearing_fault":
            self.state_data["vibration"] = round(
                self.state_data["vibration"] + random.uniform(0.05, 0.1), 2
            )

        # 🟢 INSPECT
        if action.action_type == "inspect":
            reward += 0.1

        # 🟡 DIAGNOSE
        elif action.action_type == "diagnose":
            if action.target == fault:
                reward += 0.4
            else:
                reward -= 0.2

        # 🔵 REPAIR
        elif action.action_type == "repair":
            correct_map = {
                "normal": ("motor", "ignore"),
                "bearing_fault": ("bearing", "replace"),
                "overheating": ("cooling", "monitor")
            }

            correct_target, correct_decision = correct_map[fault]

            if action.target == correct_target:
                reward += 0.3
            else:
                reward -= 0.2

            if action.decision == correct_decision:
                reward += 0.3
            else:
                reward -= 0.2

        # ⚡ Efficiency bonus
        if self.step_count <= 2:
            reward += 0.1

        # 🛑 Ending conditions
        if self.step_count >= self.max_steps:
            self.done = True

        if reward >= 0.8:
            self.done = True

        return StepResult(
            observation=self._get_observation(),
            reward=reward,
            done=self.done,
            info={"step_count": self.step_count}
        )

    async def state(self):
        return self.state_data

    async def close(self):
        pass