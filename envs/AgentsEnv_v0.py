import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
from envs.model import Model
from envs.SpyEnv_v2 import SpyEnv_v2
from stable_baselines3 import PPO


AIRPORTS = np.array([
  'BANGKOK', #0
  'SAN-FRANSISCO',#1 
  'ZURICH', #2
  'MANILA', #3
  'LONDON', #4
  'AMSTERDAM', #5
  'PARIS', #6
  'DALLAS', #7
  'DENVER', #8
  'NEW-YORK', #9
  'PHILADELPHIA', #10
  'OSLO', #11
  'MANCHESTER', #12
  'SHENZHEN', #13
  'SHANGHAI', #14
  'XAIMEN' #15
])

FLIGHTS = dict({
  'BANGKOK': [2, 3, 5, 13], 
  'SAN-FRANSISCO': [3, 7, 10, 8, 6, 2], 
  'ZURICH': [10, 1, 0, 5, 12, 11, 4], 
  'MANILA': [1, 0, 15], 
  'LONDON': [6, 2, 5, 11], 
  'AMSTERDAM': [4, 2, 0, 12, 11],
  'PARIS': [1, 4],
  'DALLAS': [9, 8, 1 ,10],
  'DENVER':[9, 7, 1 ,10],
  'NEW-YORK': [7, 8],
  'PHILADELPHIA': [7, 8, 1, 2, 5],
  'OSLO': [4, 2, 5, 12],
  'MANCHESTER': [11, 5, 2],
  'SHENZHEN': [0, 14],
  'SHANGHAI': [13, 15],
  'XAIMEN': [3, 4]
})

FLIGHTS_GRAPH = [
  [2, 3, 5, 13], 
  [3, 7, 10, 8, 6, 2], 
  [10, 1, 0, 5, 12, 11, 4], 
  [1, 0, 15], 
  [6, 2, 5, 11], 
  [4, 2, 0, 12, 11],
  [1, 4],
  [9, 8, 1 ,10],
  [9, 7, 1 ,10],
  [7, 8],
  [7, 8, 1, 2, 5],
  [4, 2, 5, 12],
  [11, 5, 2],
  [0, 14],
  [13, 15],
  [3, 4]
]

SPY_POSITION = [0,0]
AGENT1_POSITION = [3,1]
AGENT2_POSITION = [1,2]
TARGET_POSITION = [2,1]


class AgentsEnv_v0(Env):

  def __init__(self, col, row):
    self.row = row
    self.col = col

    self.airPortGrid = AIRPORTS.reshape(col,row)

    self.state = dict({
      "spyPosition": SPY_POSITION, 
      "agent1Position": AGENT1_POSITION, 
      "agent2Position": AGENT2_POSITION,
      "targetPosition": TARGET_POSITION
      })

    self.observation_space = Dict({
      "spyPosition":Box(low=0, high=3, shape=(2,), dtype=int),
      "agent1Position":Box(low=0, high=3, shape=(2,), dtype=int),
      "agent2Position":Box(low=0, high=3, shape=(2,), dtype=int),
      "targetPosition":Box(low=0, high=3, shape=(2,), dtype=int)
      })

    self.action_space = MultiDiscrete([15, 15]) 


    self.possibleActions = AIRPORTS

    self.win = 0
    self.lose = 0
    self.ilegal_step = 0

    spy_env = SpyEnv_v2(4,4)
    self.spyModel = Model.Model(spy_env, isNew=False)

  

  #action = represent index of airpor in array
  def step(self, actions):
    reward = 0
    done = False
    info = {}

    for i in range(len(actions)):
      #check if actions are legal
      legal_flights = self.getPossibleFlightsFromCurrentPosition(tuple(self.state[f"agent{i+1}Position"]))
      if(actions[i] not in legal_flights):
        self.ilegal_step +=1
        reward = -100
        return self.state, reward, True, info
    
    #The spy moving first
    self.moveOpponentSpy()

    #move agents
    for i in range(len(actions)):
      row, col = self.getRowAndColumn(actions[i])
      self.state[f"agent{i+1}Position"] = [row, col]

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
    currentAirPort = self.airPortGrid[currentPosition]
    return FLIGHTS[currentAirPort]
  
  def getRowAndColumn(self, indexInAirPortArray):
    row = indexInAirPortArray // self.row
    col = indexInAirPortArray % self.col
    return row, col

  #Move spy
  def moveOpponentSpy(self):
    #get action from the Spy model
    actions = self.spyModel.predict(self.state)
    #check if action is legal (based on the spy location)
    legal_actions = self.getPossibleFlightsFromCurrentPosition(tuple(self.state['spyPosition']))
    if(actions[0] in legal_actions):
      row, col = self.getRowAndColumn(actions[0])
    #if model predicted ilegal action, spy will move to the traget by shortest path   
    else: 
      spy_airport_index = self.getAirPortIndex(self.state['spyPosition'])
      action = self.get_spy_next_airPort_by_shortest_path(spy_airport_index)
      row, col = self.getRowAndColumn(action)
    #update spy to new position
    self.state["spyPosition"] = [row, col]


  #self.col represent the number of columns in the grid
  def getAirPortIndex(self, currentPosition):
    return currentPosition[0] * self.col + currentPosition[1]
  
  def get_spy_next_airPort_by_shortest_path(self, spy_airport_index):
    #calculate shortest path between spy to target
    target_airport_index = self.getAirPortIndex(self.state['targetPosition'])
    path = self.shortest_path(spy_airport_index, target_airport_index)
    
    return path[1]
  
  def shortest_path(self, node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]
        
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = FLIGHTS_GRAPH[last_node]
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