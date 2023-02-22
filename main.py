from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from envs.SpyEnv_v3 import SpyEnv_v3
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.flights import flights
import itertools
import collections
from sb3_contrib.common.wrappers import ActionMasker
import numpy as np
from stable_baselines3.common.vec_env import DummyVecEnv


state = {
  "spyPosition": 0, 
  "agent1Position": 1, 
  "agent2Position": 7,
  "targetPosition": 24
}

def mask_fn(env):
  return env.mask_actions()

order_for_train = []
# BFS algorithm
def bfs(root):
order_for_train = []
# BFS algorithm
def bfs(root):

  visited = set() 
  queue = collections.deque([root])
  visited.add(root)
  while queue:
    # Dequeue a vertex from queue
    vertex = queue.popleft()
    if(vertex != root):
      order_for_train.append(vertex)
    # If not visited, mark it as visited, and
    # enqueue it
    for neighbour in flights[vertex]['destinations']:
      if neighbour not in visited:
        visited.add(neighbour)
        queue.append(neighbour)
  visited = set() 
  queue = collections.deque([root])
  visited.add(root)
  while queue:
    # Dequeue a vertex from queue
    vertex = queue.popleft()
    if(vertex != root):
      order_for_train.append(vertex)
    # If not visited, mark it as visited, and
    # enqueue it
    for neighbour in flights[vertex]['destinations']:
      if neighbour not in visited:
        visited.add(neighbour)
        queue.append(neighbour)

bfs(0)
bfs(0)

first = True
counter = 0
f = open('learning_process-with_callBack.txt', 'a')
f.write("iteration, target, wins, loses, tie\n") 
f.close()
while counter < 9:
  for i in order_for_train:
    state['targetPosition'] = i
    if(len(set(state.values())) < 4):
      continue
    
    spy_env = SpyEnv_v2(state, flights)
    env = DummyVecEnv([lambda: spy_env])

    spy_env = ActionMasker(spy_env, mask_fn)

    if first:
      first = False
      spy_model = Model.Model(spy_env, name='SpyEnv_v2', isNew=True)
    else:
      spy_model = Model.Model(spy_env, name='SpyEnv_v2', isNew=False)
    
    distance = spy_env.shortest_path(state['spyPosition'], state['targetPosition'])
    distance = len(distance) - 1
  
    spy_model.learn(10000 * distance)
    spy_env.reset_stats()
    res = spy_model.test_model(20)
    if res:
      f = open('learning_process-with_callBack.txt', 'a')
      f.write(f"{counter+1}, {res['state']['targetPosition']}, {res['win']}, {res['lose']}, {res['ilegal']}, {res['tie']}\n") 
      f.close()
   
  counter+=1





# spy_env = SpyEnv_v2(state, flights)
# spy_env = ActionMasker(spy_env, mask_fn)
# spy_model = Model.Model(spy_env, name='SpyEnv_v2', isNew=False)
# print(spy_model.test_model(20))






# duplicates = []
# results = []
# first = True
# num_list = [x for x in range(len(flights))]

# all_combinations = list(itertools.permutations(num_list, 4))
# for comb in all_combinations:
#   set_comb = set(comb)
#   if(len(set_comb) == len(comb)):
#     tmp_list = list(set_comb)
#     tmp = tmp_list[2]
#     tmp_list[2] = tmp_list[1]
#     tmp_list[1] = tmp
#     if tmp_list not in duplicates:
#       duplicates.append(list(set_comb))
#       state = {
#         "spyPosition": comb[0], 
#         "agent1Position": comb[1], 
#         "agent2Position": comb[2],
#         "targetPosition": comb[3]
#         }
#       # spy vs stupid agents
#       spy_env = SpyEnv_v2(state, flights)
#       spy_env = ActionMasker(spy_env, mask_fn)
#       if first:
#         first = False
#         spy_model = Model.Model(spy_env, isNew=True)
#       else:
#         spy_model = Model.Model(spy_env, isNew=False)
#       spy_model.learn(10000)
#       spy_env.reset_stats()
#       res = spy_model.test_model(20)
#       if res:
#         f = open('initial_states-35-airports.txt', 'a')
#         f.write(f"{res['state']}, {res['win']}, {res['lose']}, {res['ilegal']}\n") 
#         f.close()
# print(results)
# agents_v0 vs spy_v2

# agents_env = AgentsEnv_v0(flights, state)
# agents_model = Model.Model(agents_env, isNew=True)
# agents_model.learn(20000)
# # agents_model.evaluate_model(10000)
# agents_env.reset_stats()
# agents_model.test_model(5)

#spy_v3 vs agents_v0
# spy_env = SpyEnv_v3(flights)
# spy_model = Model.Model(spy_env, isNew=False)
# spy_model.learn(500000)
# model.evaluate_model(10000)


# spy_env.reset_stats()
# spy_model.test_model(5)













