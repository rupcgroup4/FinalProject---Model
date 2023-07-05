import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
from envs.model import Model
from stable_baselines3 import PPO




class AgentsEnv(Env):

  def __init__(self, state, flights, train_against_model=False):

    self.flights = flights
    self.initial_state = state.copy()

    self.state = list(self.initial_state.values())

    self.observation_space = MultiDiscrete([
      len(flights),
      len(flights),
      len(flights),
      len(flights)
      ])

    self.action_space = MultiDiscrete([len(flights), len(flights)]) 

    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    self.tie = 0
    self.episode_steps = 0
    self.last_actions = [self.state[1], self.state[2]]

    if train_against_model:
      from envs.SpyEnv import SpyEnv
      spy_env = SpyEnv(state, flights)
      self.spyModel = Model.Model(spy_env, name='SpyEnv', isNew=False)
    
    self.train_against_model = train_against_model


  def heuristicFunction(self, actions):
      reward = 0

      spy_to_agent1 = len(self.shortest_path(self.state[0], self.state[1]))-1
      spy_to_agent2 = len(self.shortest_path(self.state[0], self.state[2]))-1

      if spy_to_agent1 == 1 and actions[0] != self.state[0]:
        reward -= 0.1

      if spy_to_agent2 == 1 and actions[1] != self.state[0]:
        reward -= 0.1

      if actions[0] == actions[1]:
        reward -= 0.1

      return reward



  #action = represent index of airpor in array
  def step(self, actions):
    self.episode_steps+=1
    reward = 0
    reward = self.heuristicFunction(actions)
    done = False
    info = {}

    self.last_actions = [self.state[1], self.state[2]]

    if(self.episode_steps > 30):
      self.tie +=1
      return self.state, -2, True, info


    for i in range(len(actions)):
      #check if actions are legal
      legal_flights = self.getPossibleFlightsFromCurrentPosition(self.state[i+1])
      if(actions[i] not in legal_flights):
        self.ilegal_step +=1
        reward = -3
        return self.state, reward, True, info
      
    #Check if spy lose
    if self.isSpyAndAgentInSamePosition(): 
      self.win +=1
      reward = 1
      done = True
    # Check if Spy wins
    elif self.state[0] == self.state[3] and not self.isSpyAndAgentInSamePosition(): 
        self.lose +=1
        reward = -1
        done = True    
    else:
      #move agents
      for i in range(len(actions)):
        self.state[i+1] = actions[i]

      #Calculate reward
      if self.isSpyAndAgentInSamePosition(): 
        self.win +=1
        reward = 1
        done = True
    
    if not done:
      #Spy move
      self.moveOpponentSpy()
     

    return self.state, reward, done, info
  
  def isSpyAndAgentInSamePosition(self):
    return self.state[0] == self.state[1] or self.state[0] == self.state[2]

 #currentPoistion is Tuple (row,col)
  def getPossibleFlightsFromCurrentPosition(self, currentPosition):
    return self.flights[currentPosition]['destinations']
  
  def mask_actions(self):
    mask_actions = []
    for i in range(2):
      agent_mask = []
      valid_actions = self.getPossibleFlightsFromCurrentPosition(self.state[i+1])
      for j in range(len(self.flights)):
        if j in valid_actions and j != self.last_actions[i]: # 
          agent_mask.append(True)
          continue
        agent_mask.append(False)
      mask_actions.append(agent_mask)
    mask_actions = np.array(mask_actions)
    return mask_actions


  #Move spy
  def moveOpponentSpy(self):
    if self.train_against_model:
      #get action from the Spy model
      action = self.spyModel.predict(self.state)
      action = action.item()
    else:
      #spy will move to the traget by shortest path   
      action = self.get_spy_next_airPort_by_shortest_path(self.state[0])
    #update spy to new position
    self.state[0] = action


  #self.col represent the number of columns in the grid
  def getAirPortIndex(self, currentPosition):
    return currentPosition[0] * self.col + currentPosition[1]
  
  def get_spy_next_airPort_by_shortest_path(self, spy_airport_index):
    #calculate shortest path between spy to target
    path = self.shortest_path(spy_airport_index, self.state[3])
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
    self.state = list(self.initial_state.values())
    self.moveOpponentSpy()

    self.episode_steps = 0
    self.last_actions = [self.state[1], self.state[2]]
    return self.state

  def stats(self):
    return self.win, self.lose, self.ilegal_step, self.tie

  def reset_stats(self):
    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    self.tie = 0


