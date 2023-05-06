import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from observation import Observation
from envs.model import Model
from envs.AgentsEnv  import AgentsEnv_v1
from envs.SpyEnv import SpyEnv_v3


from envs.flights import flights

class gameState(BaseModel):
  spy_position: str
  agent1_position: str
  agent2_position: str
  target_position: str
  isNew: bool

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/agents')
async def whereToFlyAgents(item: gameState):
  print(item)
  obs = Observation(item.spy_position, item.agent1_position, item.agent2_position, item.target_position)
  env = AgentsEnv_v1(obs.state, flights)
  model = Model.Model(env, name='AgentsEnv', isNew=not item.isNew)

  print(obs.state)
  res = model.predict(env.state)
  res1 = obs.get_air_port_id_by_index(res[0])
  res2 = obs.get_air_port_id_by_index(res[1])
  return {'result':[res1, res2]}

  # return {'result':1}


@app.post('/spy')
async def whereToFlySPY(item: gameState):
  print(item)
  obs = Observation(item.spy_position, item.agent1_position, item.agent2_position, item.target_position)
  env = SpyEnv_v3(obs.state, flights)

  model = Model.Model(env, name='spy_300k_vs_agents_50k', isNew=not item.isNew)
  print(obs.state)
  res = model.predict(env.state)
  res = res.item()

  res = obs.get_air_port_id_by_index(res)
  print(res)
  return {'result':res}
  # return {'result':1}



@app.get('/')
async def ping():
  return {'ping'}


if __name__ == "__main__":
  uvicorn.run("modelAPI:app", host="0.0.0.0", port=8000, reload=True)