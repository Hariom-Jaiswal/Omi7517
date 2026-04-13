from fastapi import FastAPI, Request
from pydantic import BaseModel
from env.environment import OpsDeskEnv
from env.models import Action

app = FastAPI(title="OpsDesk OpenEnv")
env = OpsDeskEnv(task_level="HARD")

class StepRequest(BaseModel):
    action_type: str = "ignore_email"
    email_id: str = "e1"
    metadata: dict = {}

@app.get("/")
def read_root():
    return {"name": "OpsDesk", "status": "operational"}

@app.post("/reset")
async def reset_post(request: Request):
    global env
    task_level = "HARD"
    try:
        body = await request.json()
        if isinstance(body, dict) and "task_level" in body:
            task_level = body.get("task_level", "HARD")
    except Exception:
        pass
        
    env = OpsDeskEnv(task_level=task_level)
    obs = env.reset()
    return {"observation": obs.model_dump()}

@app.get("/reset")
def reset_get(task_level: str = "HARD"):
    global env
    env = OpsDeskEnv(task_level=task_level)
    obs = env.reset()
    return {"observation": obs.model_dump()}

@app.get("/state")
def state():
    return env.state().model_dump()

@app.post("/step")
async def step(request: Request):
    try:
        req_body = await request.json()
    except Exception:
        req_body = {}

    action_data = {}
    if "action" in req_body:
        action_data = req_body["action"]
    else:
        action_data = req_body

    from pydantic import ValidationError
    try:
        act = Action(**action_data)
    except ValidationError:
        act = Action(action_type="ignore_email", email_id="e1", metadata={})
        
    obs, reward, terminated, info = env.step(act)
    return {
        "observation": obs.model_dump(),
        "reward": reward.value,
        "done": terminated,
        "info": info
    }
