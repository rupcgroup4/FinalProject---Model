import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.model import Model


SPY_POSITION = 32
AGENT1_POSITION = 13
AGENT2_POSITION = 22
TARGET_POSITION = 14


class SpyEnv_v3(Env):

  def __init__(self, flights):
 
    self.flights = flights

    self.state = dict({
      "spyPosition": SPY_POSITION, 
      "agent1Position": AGENT1_POSITION, 
      "agent2Position": AGENT2_POSITION,
      "targetPosition": TARGET_POSITION
      })

    self.observation_space = Dict({
      "spyPosition": Discrete(len(flights)),
      "agent1Position": Discrete(len(flights)),
      "agent2Position": Discrete(len(flights)),
      "targetPosition": Discrete(len(flights))
      })

    self.action_space = Discrete(len(flights))


    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    agents_env = AgentsEnv_v0(flights)
    self.agents_model = Model.Model(agents_env, isNew=False)

    

  #action = represent index of airpor in array
  def step(self, action):
    reward = 0
    done = False
    info = {}

    #check if action is legal
    legal_flights = self.getPossibleFlightsFromCurrentPosition(self.state["spyPosition"])
    if(action not in legal_flights):
      self.ilegal_step +=1
      reward = -50
      return self.state, reward, True, info

    #Move spy
    self.state["spyPosition"] = action

    #Calculate reward
    if self.isSpyAndAgentInSamePosition(): 
      self.lose +=1
      reward = -50
      done = True
    elif self.state['spyPosition'] == self.state['targetPosition']: 
      self.win +=1
      reward = 100
      done = True
    #
    else:
      # move agents
      self.moveOpponentAgents()

      # check if spy lose after agents moved
      if self.isSpyAndAgentInSamePosition(): 
        self.lose +=1
        reward = -50
        done = True

    return self.state, reward, done, info
  
  def isSpyAndAgentInSamePosition(self):
    return self.state['spyPosition'] == self.state['agent1Position'] or self.state['spyPosition'] == self.state['agent2Position']

  #currentPoistion is index in flights array
  def getPossibleFlightsFromCurrentPosition(self, currentPosition):
    return self.flights[currentPosition]['destinations']
  


  def moveOpponentAgents(self):
    #get actions from the Agents model
    actions = self.agents_model.predict(self.state)[0]
    for i in range(len(actions)):
      #for each agent check if actions is legal
      legal_flights = self.getPossibleFlightsFromCurrentPosition(self.state[f"agent{i+1}Position"])
      if(actions[i] in legal_flights):
        action = actions[i] 
      else:
        action = self.getAgentNextAirPortByShortestPath(self.state[f"agent{i+1}Position"])
      #update agent to new position
      self.state[f"agent{i+1}Position"] = action

    
  def getAgentNextAirPortByShortestPath(self, agentAirportIndex):
    #calculate shortest path between agent to spy
    path = self.shortest_path(agentAirportIndex, self.state['spyPosition'])
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