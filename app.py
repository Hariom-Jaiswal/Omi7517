from fastapi import FastAPI
from env.environment import OpsDeskEnv

app = FastAPI()
env = OpsDeskEnv()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/reset")
def reset():
    return {"message": "env reset"}

@app.get("/state")
def state():
    return {"state": "ok"}