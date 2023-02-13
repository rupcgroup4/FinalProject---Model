import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict
from envs.AgentsEnv_v0 import AgentsEnv_v0
from envs.model import Model



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


class SpyEnv_v3(Env):

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
      "spyPosition":Box(low=0, high=3, shape=(2,),),
      "agent1Position":Box(low=0, high=3, shape=(2,),),
      "agent2Position":Box(low=0, high=3, shape=(2,),),
      "targetPosition":Box(low=0, high=3, shape=(2,),)
      })

    self.action_space = Discrete(16) 

    self.possibleActions = AIRPORTS

    self.win = 0
    self.lose = 0
    self.ilegal_step = 0
    agents_env = AgentsEnv_v0(4,4)
    self.agents_model = Model.Model(agents_env, isNew=False)

    

  

  #action = represent index of airpor in array
  def step(self, action):
    reward = 0
    done = False
    info = {}

    #check if action is legal
    legal_flights = self.getPossibleFlightsFromCurrentPosition(tuple(self.state["spyPosition"]))
    if(action not in legal_flights):
      self.ilegal_step +=1
      reward = -100
      return self.state, reward, True, info

    #Move spy
    row, col = self.getRowAndColumn(action)
    self.state["spyPosition"] = [row, col]

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

  #currentPoistion is Tuple (row,col)
  def getPossibleFlightsFromCurrentPosition(self, currentPosition):
    currentAirPort = self.airPortGrid[currentPosition]
    return FLIGHTS[currentAirPort]
  
  def getRowAndColumn(self, indexInAirPortArray):
    row = indexInAirPortArray // self.row
    col = indexInAirPortArray % self.col
    return row, col

  #self.col represent the number of columns in the grid
  def getAirPortIndex(self, currentPosition):
    return currentPosition[0] * self.col + currentPosition[1]
  

  def moveOpponentAgents(self):
    #get actions from the Agents model
    actions = self.agents_model.predict(self.state)[0]
    for i in range(len(actions)):
      #for each agent check if actions is legal
      legal_flights = self.getPossibleFlightsFromCurrentPosition(tuple(self.state[f"agent{i+1}Position"]))
      if(actions[i] in legal_flights):
        row, col = self.getRowAndColumn(actions[0])
      #if model predicted ilegal action, agent will move to the spy by shortest path   
      else:
        agent_airport_index = self.getAirPortIndex(self.state[f"agent{i+1}Position"])
        action = self.getAgentNextAirPortByShortestPath(agent_airport_index)
        row, col = self.getRowAndColumn(action)
      #update agent to new position
      self.state[f"agent{i+1}Position"] = [row, col]

    
  def getAgentNextAirPortByShortestPath(self, agentAirportIndex):
    #calculate shortest path between agent to spy
    spyAirportIndex = self.getAirPortIndex(self.state['spyPosition'])
    path = self.shortest_path(agentAirportIndex, spyAirportIndex)
    
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