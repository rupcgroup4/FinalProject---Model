import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from stable_baselines3 import PPO



SPY_POSITION = 32
AGENT1_POSITION = 13
AGENT2_POSITION = 22
TARGET_POSITION = 14


class AgentsEnv_v0(Env):

  def __init__(self, flights, state):

    self.flights = flights
    self.initial_state = state.copy()

    self.state = state.copy()

    self.observation_space = Dict({
      "spyPosition": Discrete(len(flights)),
      "agent1Position": Discrete(len(flights)),
      "agent2Position": Discrete(len(flights)),
      "targetPosition": Discrete(len(flights))
      })

    self.action_space = MultiDiscrete([len(flights)-1, len(flights)-1]) 

    self.win = 0
    self.lose = 0
    self.ilegal_step = 0

    spy_env = SpyEnv_v2(flights, state)
    self.spyModel = Model.Model(spy_env, isNew=False)

  

  #action = represent index of airpor in array
  def step(self, actions):
    reward = 0
    done = False
    info = {}

    for i in range(len(actions)):
      #check if actions are legal
      legal_flights = self.getPossibleFlightsFromCurrentPosition(self.state[f"agent{i+1}Position"])
      if(actions[i] not in legal_flights):
        self.ilegal_step +=1
        reward = -100
        return self.state, reward, True, info
    
    #The spy moving first
    self.moveOpponentSpy()

    #move agents
    for i in range(len(actions)):
      self.state[f"agent{i+1}Position"] = actions[i]

    #Calculate reward
    if self.isSpyAndAgentInSamePosition(): 
      self.win +=1
      reward = 10
      done = True

    elif self.state['spyPosition'] == self.state['targetPosition']: 
      self.lose +=1
      reward = -50
      done = True
    

    return self.state, reward, done, info
  
  def isSpyAndAgentInSamePosition(self):
    return self.state['spyPosition'] == self.state['agent1Position'] or self.state['spyPosition'] == self.state['agent2Position']

 #currentPoistion is Tuple (row,col)
  def getPossibleFlightsFromCurrentPosition(self, currentPosition):
    return self.flights[currentPosition]['destinations']
  

  #Move spy
  def moveOpponentSpy(self):
    #get action from the Spy model
    action = self.spyModel.predict(self.state)
    action = action[0].item()
    #check if action is legal (based on the spy location)
    legal_actions = self.getPossibleFlightsFromCurrentPosition(self.state['spyPosition'])
    if(action not in legal_actions):
    #if model predicted ilegal action, spy will move to the traget by shortest path   
      action = self.get_spy_next_airPort_by_shortest_path(self.state['spyPosition'])
    #update spy to new position
    self.state["spyPosition"] = action


  #self.col represent the number of columns in the grid
  def getAirPortIndex(self, currentPosition):
    return currentPosition[0] * self.col + currentPosition[1]
  
  def get_spy_next_airPort_by_shortest_path(self, spy_airport_index):
    #calculate shortest path between spy to target
    path = self.shortest_path(spy_airport_index, self.state['targetPosition'])
    return path[1]
  
  def shortest_path(self, node1, node2):
    rnd = False
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]
        
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = self.flights[last_node]['destinations']
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
           
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []

  def render(self):
    return
  
  def reset(self):
    self.state["spyPosition"] = SPY_POSITION
    self.state["agent1Position"] = AGENT1_POSITION
    self.state["agent2Position"] = AGENT2_POSITION

    return self.state

  def stats(self):
    return self.win, self.lose, self.ilegal_step

  def reset_stats(self):
    self.win = 0
    self.lose = 0
    self.ilegal_step = 0


# env = AgentsEnv_v0(4,4)


# for i in range(10):
#   print(env.action_space.sample())


# # model = PPO("MultiInputPolicy", env, verbose=1)
# model = PPO.load("ppo_spy", env=env)
# model.learn(total_timesteps=25000)
# win, lose, ilegal_step = env.stats()
# print(f'win {win}, lose {lose}, ilegal {ilegal_step}')
# model.save("ppo_spy")