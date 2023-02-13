import numpy as np
from gym import Env
from gym.spaces import Discrete, Box, Dict

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

SPY_POSITION = 24
AGENT1_POSITION = 19
AGENT2_POSITION = 14
TARGET_POSITION = 15


class SpyEnv_v2(Env):

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
      reward = 50
      done = True
    #
    else:
      # move agents
      self.moveOpponentAgent('agent1Position')
      self.moveOpponentAgent('agent2Position')

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
    return self.flights[currentPosition]['destinations']
  
  def getRowAndColumn(self, indexInAirPortArray):
    row = indexInAirPortArray // self.row
    col = indexInAirPortArray % self.col
    return row, col

  #self.col represent the number of columns in the grid
  def getAirPortIndex(self, currentPosition):
    return currentPosition[0] * self.col + currentPosition[1]
  

  def moveOpponentAgent(self, agentNum):
    agentAirportIndex = self.state[agentNum]

    # actionType = np.random.choice([1, 2], 1, p = [0.9, 0.1])
    
    # if actionType == 1:
    #   airPortIndex = self.getAgentNextAirPortByShortestPath(agentAirportIndex)
    # else:
    #   airPortIndex = self.getAgentNextAirportByRandom(agentAirportIndex)

    airPortIndex = self.getAgentNextAirPortByShortestPath(agentAirportIndex)
  
    
    #set agent new state position
    self.state[agentNum] = airPortIndex
    
  
  def getAgentNextAirPortByShortestPath(self, agentAirportIndex):
    #calculate shortest path between agent to spy
    spyAirportIndex = self.state['spyPosition']
    path = self.shortest_path(agentAirportIndex, spyAirportIndex)
    if(len(path) == 0):
      return self.getAgentNextAirportByRandom(agentAirportIndex)
    return path[1]

  #get random action based on current position
  def getAgentNextAirportByRandom(self, agentAirportIndex):
    return np.random.choice(self.flights[agentAirportIndex]['destinations']) 



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

