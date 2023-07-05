import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from observation import Observation
from envs.model import Model
from envs.AgentsEnv  import AgentsEnv
from envs.SpyEnv import SpyEnv


from envs.flights import flights

#Utilities
class gameState(BaseModel):
  spy_position: str
  agent1_position: str
  agent2_position: str
  target_position: str
  isNew: bool
  model: str

class LastActions:
  spy_last_action = None
  agents_last_actions = []


#Create FastAPI app
app = FastAPI()

#Allow CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Agents route
@app.post('/agents')
async def whereToFlyAgents(item: gameState):
  obs = Observation(item.spy_position, item.agent1_position, item.agent2_position, item.target_position)
  env = AgentsEnv(obs.state, flights)
  if len(LastActions.agents_last_actions) > 0:
    env.last_actions = LastActions.agents_last_actions
  model = Model.Model(env, name=item.model, isNew=not item.isNew)

  res = model.predict(env.state)
  LastActions.agents_last_actions = [env.state[1], env.state[2]]
  res1 = obs.get_air_port_id_by_index(res[0])
  res2 = obs.get_air_port_id_by_index(res[1])
  return {'result':[res1, res2]}


#Spy route
@app.post('/spy')
async def whereToFlySPY(item: gameState):
  obs = Observation(item.spy_position, item.agent1_position, item.agent2_position, item.target_position)
  env = SpyEnv(obs.state, flights)
  env.last_action = LastActions.spy_last_action
  model = Model.Model(env, name=item.model, isNew=not item.isNew)
  res = model.predict(env.state)
  res = res.item()
  LastActions.spy_last_action = env.state[0]

  res = obs.get_air_port_id_by_index(res)
  return {'result':res}



@app.get('/')
async def ping():
  return {'ping'}


if __name__ == "__main__":
  uvicorn.run("modelAPI:app", host="0.0.0.0", port=8000, reload=True)