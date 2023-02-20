from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from envs.SpyEnv_v3 import SpyEnv_v3
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.flights import flights
import itertools
import collections
from sb3_contrib.common.wrappers import ActionMasker
import numpy as np

state = {
  "spyPosition": 0, 
  "agent1Position": 1, 
  "agent2Position": 7,
  "targetPosition": 27
}

def mask_fn(env):
  return env.mask_actions()



agents_env = AgentsEnv_v0(state, flights)
agents_env = ActionMasker(agents_env, mask_fn)
agents_model = Model.Model(agents_env, name='AgnetsEnv_v0', isNew=True)
agents_model.learn(20000)
# agents_model.evaluate_model(10000)
agents_env.reset_stats()
print(agents_model.test_model(20))















