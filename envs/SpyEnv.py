import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict, MultiDiscrete
from envs.model import Model


SPY_POSITION = 32
AGENT1_POSITION = 13
AGENT2_POSITION = 22
TARGET_POSITION = 14


class SpyEnv(Env):

  def __init__(self, state, flights, train_against_model=False, train_against_new_model=False):
    
    self.flights = flights
    self.initial_state = state.copy()
    self.state = list(self.initial_state.values())
    
    self.observation_space = MultiDiscrete([
      len(flights),
      len(flights),
      len(flights),
      len(flights),
      ])
    
    # for i in range(len(flights)):
    #   self.state[str(i)] = flights[i]['destinations']
    #   self.observation_space[str(i)] = Box(low=0, high=len(flights), shape=(len(flights[i]['destinations']),))
    #   self.initial_state[str(i)] = flights[i]['destinations']

    

    self.action_space = Discrete(len(flights))


    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    self.tie = 0
    self.episode_steps = 0

    self.last_action = None

    if train_against_model:
      from envs.AgentsEnv import AgentsEnv
      agents_env = AgentsEnv(state, flights)
      self.agents_model = Model.Model(agents_env, name='AgentsEnv', isNew=train_against_new_model)
      

    self.train_against_model = train_against_model

    self.sp_ST = len(self.shortest_path(self.initial_state['spyPosition'], self.state[3]))-1
    self.sp_SA1 = len(self.shortest_path(self.initial_state['spyPosition'], self.state[1]))-1
    self.sp_SA2 = len(self.shortest_path(self.initial_state['spyPosition'], self.state[2]))-1
    

  def historicFunction(self):
    reward = 0

    sp_ST = len(self.shortest_path(self.state[0], self.state[3]))-1
    sp_SA1 = len(self.shortest_path(self.state[0], self.state[1]))-1
    sp_SA2 = len(self.shortest_path(self.state[0], self.state[2]))-1

    if sp_ST < self.sp_ST: 
      reward += 0.1

    if sp_ST > self.sp_ST: 
      reward -= 0.1

    if sp_ST == 1: 
      reward += 0.2
    
    if sp_SA1 < self.sp_SA1 and sp_SA2 < self.sp_SA2: 
      reward += 0.2
    
    if sp_SA1 < self.sp_SA1 or sp_SA2 < self.sp_SA2: 
      reward += 0.1

    if sp_SA1 == 1: 
      reward -= 0.1
    
    if sp_SA2 == 1: 
      reward -= 0.1

    return reward


  #action = represent index of airpor in array
  def step(self, action):
    self.episode_steps+=1
    reward = 0
    done = False
    info = {}

    self.last_action = self.state[0]

    if(self.episode_steps > 30):
      reward = -2
      return self.state, reward, True, info

    #check if action is legal
    legal_flights = self.getPossibleFlightsFromCurrentPosition(self.state[0])
    if(action not in legal_flights):
      self.ilegal_step +=1
      reward = -3
      return self.state, reward, True, info

    #Move spy
    self.state[0] = action

    # if reward == 0:
    #   reward = self.historicFunction()

    #Calculate reward
    if self.isSpyAndAgentInSamePosition(): 
      self.lose +=1
      reward = -1
      done = True
    elif self.state[0] == self.state[3]: 
      self.win +=1

      # shortest_path = len(self.shortest_path(self.initial_state['spyPosition'], self.initial_state['targetPosition'])) - 1
      # steps_played_over_shorthest_path = self.episode_steps - shortest_path
      # reward = 1 - (steps_played_over_shorthest_path / 30)
      reward = 1
      done = True
    else:
      # move agents
      self.moveOpponentAgents()

      # check if spy lose after agents moved
      if self.isSpyAndAgentInSamePosition(): 
        self.lose +=1
        reward = -1
        done = True

    return self.state, reward, done, info
  
  def isSpyAndAgentInSamePosition(self):
    return self.state[0] == self.state[1] or self.state[0] == self.state[2]


  #currentPoistion is index in flights array
  def getPossibleFlightsFromCurrentPosition(self, currentPosition):
    return self.flights[currentPosition]['destinations']
  
  def mask_actions(self):
    mask_actions = []
    valid_actions = self.getPossibleFlightsFromCurrentPosition(self.state[0])
    for i in range(len(self.flights)):
      if i in valid_actions and i != self.last_action:
        mask_actions.append(True)
        continue
      mask_actions.append(False)

    mask_actions = np.array(mask_actions)
    return mask_actions


  def moveOpponentAgents(self):

    if self.train_against_model:
      #get actions from the Agents model
      actions = self.agents_model.predict(self.state)
    for i in range(2):
      #for each agent check if actions is legal
      if self.train_against_model:
        action = actions[i] 
      else:
        action = self.getAgentNextAirPortByShortestPath(self.state[i+1])
      #update agent to new position
      self.state[i+1] = action

    
  def getAgentNextAirPortByShortestPath(self, agentAirportIndex):
    #calculate shortest path between agent to spy
    path = self.shortest_path(agentAirportIndex, self.state[0])
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
    self.episode_steps = 0
    self.last_action = None
    return self.state

  def stats(self):
    return self.win, self.lose, self.ilegal_step, self.tie

  def reset_stats(self):
    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    self.tie = 0
