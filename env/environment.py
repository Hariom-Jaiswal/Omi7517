class OpsDeskEnv:
    def reset(self):
        return {"msg": "reset done"}

    def step(self, action):
        return {"obs": "ok"}, 0.5, False, {}

    def state(self):
        return {"state": "running"}