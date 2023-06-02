import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from observation import Observation
from envs.model import Model
from envs.AgentsEnv  import AgentsEnv
from envs.SpyEnv import SpyEnv


from envs.flights import flights

class gameState(BaseModel):
  spy_position: str
  agent1_position: str
  # agent2_position: str
  target_position: str
  isNew: bool


class LastActions:
  spy_last_action = None
  agents_last_actions = None


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
  obs = Observation(item.spy_position, item.agent1_position, item.target_position)
  env = AgentsEnv(obs.state, flights)

  env.last_action = LastActions.agents_last_actions
  # if len(LastActions.agents_last_actions) > 0:
  #   env.last_actions = LastActions.agents_last_actions
  model = Model.Model(env, name='AgentsEnv', isNew=not item.isNew)

  print(obs.state)
  res = model.predict(env.state)
  res = res.item()
  LastActions.agents_last_actions = env.state[1]
  # LastActions.agents_last_actions = [env.state[1], env.state[2]]

  res = obs.get_air_port_id_by_index(res)
  # res2 = obs.get_air_port_id_by_index(res[1])
  return {'result':res}

  # return {'result':1}


@app.post('/spy')
async def whereToFlySPY(item: gameState):
  print(item)
  obs = Observation(item.spy_position, item.agent1_position, item.target_position)
  env = SpyEnv(obs.state, flights)
  env.last_action = LastActions.spy_last_action
  model = Model.Model(env, name='SpyEnv', isNew=not item.isNew)
  print(obs.state)
  res = model.predict(env.state)
  res = res.item()
  LastActions.spy_last_action = env.state[0]

  res = obs.get_air_port_id_by_index(res)
  print(res)
  return {'result':res}
  # return {'result':1}



@app.get('/')
async def ping():
  return {'ping'}


if __name__ == "__main__":
  uvicorn.run("modelAPI:app", host="0.0.0.0", port=8000, reload=True)