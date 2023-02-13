import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import Env
from gym.spaces import Discrete, Box


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
  'XAIMEN': [3, 14]
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
  [3, 14]
]

class SpyEnv_v0(Env):

  def __init__(self, col, row):
    self.row = row
    self.col = col

    self.airPortGrid = AIRPORTS.reshape(col,row)
    self.positionsGrid = np.zeros((col,row))
    # self.positionsGrid[0,0] = 1 #1 represent Spy
    self.positionsGrid[2,1] = 3 #3 represent target
    self.positionsGrid[3,1] = 2 #2 represent Agent
    self.positionsGrid[0,3] = 2 #2 represent Agent

    self.position = [0,0]
    
    self.action_space = Discrete(len(AIRPORTS))
    self.observation_space = Box(low=0, high=1, shape=(2,))

    self.possibleActions = AIRPORTS

  #action = represent index of airpor in array
  def step(self, action):
    reward = -1
    done = False

    #Move agent
    row, col = self.getAgentRowAndColumn(action)
    self.position = [row, col]
    #Calculate reward
    if self.positionsGrid[row, col] == 2: #2 represent agent
      reward = -50
      done = True
    elif self.positionsGrid[row, col] == 3: #3 represent target
      done = True
    
    return self.position, reward, done
    
  #get random action based on current position
  def getSampleAction(self):
    currentAirPort = self.airPortGrid[self.position[0], self.position[1]]
    return np.random.choice(FLIGHTS[currentAirPort]) 

  def getPossibleFlightsFromCurrentPosition(self, row, col):
    currentAirPort = self.airPortGrid[row, col]
    return FLIGHTS[currentAirPort]
  
  def getAgentRowAndColumn(self, indexInAirPortArray):
      row = indexInAirPortArray // self.row
      col = indexInAirPortArray % self.col
      return row, col

  def redner(self):
    return
  
  def reset(self):
    self.position = [0,0]
    return self.position



def maxAction(Q, state, actions):
  values = np.array([Q[(state[0],state[1]), a] for a in actions])
  action = np.argmax(values)
  return actions[action]


if __name__ == '__main__':
  # Agnet move as a Spy accroding to flights
  env = SpyEnv_v0(4, 4)
  # model hyperparameters
  ALPHA = 0.1
  GAMMA = 1.0
  EPS = 1.0
  Q = {}
  for row in range(env.row):
    for col in range(env.col):
      for action in env.getPossibleFlightsFromCurrentPosition(row, col):
          Q[(row,col), action] = 0
  numGames = 500
  totalRewards = np.zeros(numGames)
  for i in range(numGames):
     
      if i % 5000 == 0:
        print('starting game ', i)
      
      done = False
      epRewards = 0
      observation = env.reset()
      while not done:
          rand = np.random.random()
          action = maxAction(Q, observation, env.getPossibleFlightsFromCurrentPosition(env.position[0], env.position[1])) if rand < (1-EPS) \
              else env.getSampleAction()
          observation_, reward, done = env.step(action)
          epRewards += reward
          action_ = maxAction(Q, observation_, env.getPossibleFlightsFromCurrentPosition(env.position[0], env.position[1]))
          Q[(observation[0], observation[1]), action] = Q[(observation[0], observation[1]), action] + ALPHA*(reward +
                        GAMMA*Q[(observation_[0], observation_[1]), action_] - Q[(observation[0], observation[1]), action])
          observation = observation_
      if EPS - 2 / numGames > 0:
          EPS -= 2 / numGames
      else:
          EPS = 0
      totalRewards[i] = epRewards
  plt.plot(totalRewards)
  plt.show()


  






