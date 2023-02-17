from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from envs.SpyEnv_v3 import SpyEnv_v3
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.flights import flights
import itertools

state = {
  "spyPosition": 0, 
  "agent1Position": 1, 
  "agent2Position": 13,
  "targetPosition": 24
}

spy_env = SpyEnv_v2(state, flights)
spy_model = Model.Model(spy_env, isNew=False)
spy_model.test_model(20)
spy_model.learn(50000)
spy_env.reset_stats()
spy_model.test_model(20)


# path = spy_env.shortest_path(0, 2)
# print(path)

# duplicates = []
# results = []
# first = True
# num_list = [x for x in range(len(flights)-1)]

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
#       if first:
#         first = False
#         spy_model = Model.Model(spy_env, isNew=True)
#       else:
#         spy_model = Model.Model(spy_env, isNew=False)
#       spy_model.learn(20000)
#       # model.evaluate_model(10000)
#       spy_env.reset_stats()
#       res = spy_model.test_model(20)
#       if res:
#         f = open('initial_states.txt', 'a')
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













