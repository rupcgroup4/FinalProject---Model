from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from envs.SpyEnv_v3 import SpyEnv_v3
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.flights import flights



# spy vs stupid agents
spy_env = SpyEnv_v2(flights)
spy_model = Model.Model(spy_env, isNew=False)
spy_model.learn(250000)
# model.evaluate_model(10000)
spy_env.reset_stats()
spy_model.test_model(5)

# agents_v0 vs spy_v2

# agents_env = AgentsEnv_v0(4,4)
# agents_model = Model.Model(agents_env, isNew=False)
# agents_model.learn(500000)
# # agents_model.evaluate_model(10000)
# agents_env.reset_stats()
# agents_model.test_model(100)

#spy_v3 vs agents_v0
# spy_env = SpyEnv_v3(4,4)
# spy_model = Model.Model(spy_env, isNew=False)
# spy_model.learn(500000)
# model.evaluate_model(10000)


# spy_env.reset_stats()
# spy_model.test_model(1)













