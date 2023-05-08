# import uvicorn
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from observation import Observation
from envs.model import Model
from envs.AgentsEnv  import AgentsEnv_v1
from envs.SpyEnv import SpyEnv_v3
from flask import Flask,request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import json

from envs.flights import flights

class gameState(BaseModel):
  spy_position: str
  agent1_position: str
  agent2_position: str
  target_position: str
  isNew: bool

# app = FastAPI()
app = Flask(__name__)

CORS(app)
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



@app.route('/agents', methods=['POST'])
async def whereToFlyAgents():
  item = request.data
  resp = json.loads(item)
  obs = Observation(resp['spy_position'], resp['agent1_position'],resp['agent2_position'],resp['target_position'])
  env = AgentsEnv_v1(obs.state, flights)
  model = Model.Model(env, name='AgentsEnv', isNew=not resp['isNew'])

  print(obs.state)
  res = model.predict(env.state)
  res1 = obs.get_air_port_id_by_index(res[0])
  res2 = obs.get_air_port_id_by_index(res[1])
  return {'result':[res1, res2]}


@app.route('/spy', methods=['POST'])
async def whereToFlySPY():
  item = request.data
  resp = json.loads(item)

  obs = Observation(resp['spy_position'], resp['agent1_position'],resp['agent2_position'],resp['target_position'])
  env = SpyEnv_v3(obs.state, flights)

  model = Model.Model(env, name='spy_300k_vs_agents_50k', isNew=not resp['isNew'])
  print(obs.state)
  res = model.predict(env.state)
  res = res.item()

  res = obs.get_air_port_id_by_index(res)
  print(res)
  return {'result':res}




# @app.get('/')
# async def ping():
#   return {'ping'}


if __name__ == '__main__':
    # Debug/Development
    app.run(debug=True, host="0.0.0.0", port="8000")

    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


# if __name__ == "__main__":
#   uvicorn.run("modelAPI:app", host="0.0.0.0", port=8000, reload=True)