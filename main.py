from envs.model import Model
from envs.SpyEnv import SpyEnv_v3
from envs.flights import flights
import itertools
import collections
from sb3_contrib.common.wrappers import ActionMasker
import numpy as np
from stable_baselines3.common.vec_env import DummyVecEnv
from envs.AgentsEnv import AgentsEnv_v1



state = {
  "spyPosition": 0, 
  "agent1Position": 6, 
  "agent2Position": 14,
  "targetPosition": 9
}

def mask_fn(env):
  return env.mask_actions()


spy_env = SpyEnv_v3(state, flights, train_against_model=True)
spy_env = ActionMasker(spy_env, mask_fn)
spy_model = Model.Model(spy_env, name='SpyEnv', isNew=False)
spy_model.learn(250000)
# agents_env = AgentsEnv_v1(state, flights, train=True, train_against_model=True)
# agents_env = ActionMasker(agents_env, mask_fn)
# agents_model = Model.Model(agents_env, name='AgnetsEnv', isNew=True)
# agents_model.learn(50000)


# counter = 0
# while counter < 1:

#   print('Spy')
 
#   spy_env = ActionMasker(spy_env, mask_fn)
#   spy_model = Model.Model(spy_env, name='SpyEnv_v3', isNew=False)
#   spy_model.learn(20000)
#   print('agents')
#   agents_env = AgentsEnv_v1(state, flights, train=True, train_against_model=True)
#   agents_env = ActionMasker(agents_env, mask_fn)
#   agents_model = Model.Model(agents_env, name='AgnetsEnv_v1', isNew=False)
#   agents_model.learn(20000)

#   counter +=1

spy_env.reset_stats()
print(spy_model.test_model(1000))
# agents_env.reset_stats()
# print(agents_model.test_model(1000))

# order_for_train = []
# # BFS algorithm
# def bfs(root):

#   visited = set() 
#   queue = collections.deque([root])
#   visited.add(root)
#   while queue:
#     # Dequeue a vertex from queue
#     vertex = queue.popleft()
#     if(vertex != root):
#       order_for_train.append(vertex)
#     # If not visited, mark it as visited, and
#     # enqueue it
#     for neighbour in flights[vertex]['destinations']:
#       if neighbour not in visited:
#         visited.add(neighbour)
#         queue.append(neighbour)
#   visited = set() 
#   queue = collections.deque([root])
#   visited.add(root)
#   while queue:
#     # Dequeue a vertex from queue
#     vertex = queue.popleft()
#     if(vertex != root):
#       order_for_train.append(vertex)
#     # If not visited, mark it as visited, and
#     # enqueue it
#     for neighbour in flights[vertex]['destinations']:
#       if neighbour not in visited:
#         visited.add(neighbour)
#         queue.append(neighbour)

# bfs(0)

# first = True
# counter = 0
# f = open('learning_process-bfs.txt', 'a')
# f.write("iteration, target, wins, loses, tie\n") 
# f.close()
# while counter < 2:
#   for i in order_for_train:
#     state['targetPosition'] = i
#     if(len(set(state.values())) < 4):
#       continue
    
#     spy_env = SpyEnv_v3(state, flights, train_against_model=True)
#     spy_env = ActionMasker(spy_env, mask_fn)
#     agents_env = AgentsEnv_v1(state, flights, train=True, train_against_model=True)
#     agents_env = ActionMasker(agents_env, mask_fn)
#     if first:
      
#       spy_model = Model.Model(spy_env, name='SpyEnv_BFS', isNew=True)
#       agents_model = Model.Model(agents_env, name='AgentsEnv_BFS', isNew=True)
#     else:
#       spy_model = Model.Model(spy_env, name='SpyEnv_BFS', isNew=False)
#       agents_model = Model.Model(agents_env, name='AgentsEnv_BFS', isNew=False)
    
#     distance = spy_env.shortest_path(state['spyPosition'], state['targetPosition'])
#     distance = len(distance) - 1
#     if distance > 2:
      
#       spy_model.learn(10000 * distance)
#       agents_model.learn(10000 * distance)
#       spy_env.reset_stats()
#       res = spy_model.test_model(20)
#       if res:
#         f = open('learning_process-bfs.txt', 'a')
#         f.write(f"{counter+1} SPY, {res['state']['targetPosition']}, {res['win']}, {res['lose']}, {res['ilegal']}, {res['tie']}\n") 
#         f.close()
      
#       agents_env.reset_stats()
#       res = agents_model.test_model(20)
#       if res:
#         f = open('learning_process-bfs.txt', 'a')
#         f.write(f"{counter+1} Agents, {res['state']['targetPosition']}, {res['win']}, {res['lose']}, {res['ilegal']}, {res['tie']}\n") 
#         f.close()
   
#   counter+=1












# first = True
# num_list = [x for x in range(len(flights))]
# legal_comb = []

# all_combinations = list(itertools.permutations(num_list, 4))
# for comb in all_combinations:
#   if(len(set(comb)) == len(comb)):
#     tmp_list = list(comb).copy()
#     if(tmp_list[0] == 0 and tmp_list[1] == 2 and tmp_list[2] == 1 and tmp_list[3] == 5):
#       print('hi')
#     tmp = tmp_list[2]
#     tmp_list[2] = tmp_list[1]
#     tmp_list[1] = tmp
#     if tmp_list not in legal_comb:
      
#       state = {
#         "spyPosition": comb[0], 
#         "agent1Position": comb[1], 
#         "agent2Position": comb[2],
#         "targetPosition": comb[3]
#         }
#       # spy vs stupid agents
#       spy_env = SpyEnv_v3(state, flights, train=True, train_against_model=True)
#       spy_env = ActionMasker(spy_env, mask_fn)
#       spy_to_target = spy_env.shortest_path(state['spyPosition'], state['targetPosition'])
#       spy_to_target = len(spy_to_target) - 1
#       agent1_to_target = spy_env.shortest_path(state['agent1Position'], state['targetPosition'])
#       agent1_to_target = len(agent1_to_target) - 1
#       agent2_to_target = spy_env.shortest_path(state['agent2Position'], state['targetPosition'])
#       agent2_to_target = len(agent2_to_target) - 1
#       if(spy_to_target > 2 and (spy_to_target > agent1_to_target or spy_to_target > agent2_to_target)):
#         legal_comb.append(list(comb))
#         if first:
#           first = False
#           spy_model = Model.Model(spy_env, name='SpyEnv_all', isNew=True)

#         else:
#           spy_model = Model.Model(spy_env, name='SpyEnv_all', isNew=False)

#         spy_model.learn(5000)
#         spy_env.reset_stats()
#         res = spy_model.test_model(20)
#         if res:
#           f = open('spy-all-combinations-airports.txt', 'a')
#           f.write(f"{res['state']}, {res['win']}, {res['lose']}, {res['tie']}\n") 
#           f.close()

# print(legal_comb)

# agents_v0 vs spy_v2

# agents_env = AgentsEnv_v0(flights, state)
# agents_model = Model.Model(agents_env, isNew=True)
# agents_model.learn(20000)
# # agents_model.evaluate_model(10000)
# agents_env.reset_stats()
# agents_model.test_model(5)

# spy_v3 vs agents_v0
# spy_env = SpyEnv_v3(flights)
# spy_model = Model.Model(spy_env, isNew=False)
# spy_model.learn(500000)
# model.evaluate_model(10000)


# spy_env.reset_stats()
# spy_model.test_model(5)













