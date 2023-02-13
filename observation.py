import numpy as np
from stable_baselines3 import PPO
from envs.SpyEnv_v2 import SpyEnv_v2
import os

INIT_SPY_LOCATION = [0,0]
INIT_AGENT_LOCATION = [2,0]
INIT_TARGET_LOCATION = [2,1]

AIRPORTS = np.array([
  'BKK', #0
  'SFO',#1 
  'ZRH', #2
  'MNL', #3
  'LGW', #4
  'AMS', #5
  'ORY', #6
  'DFW', #7
  'DEN', #8
  'LGA', #9
  'PHL', #10
  'OSL', #11
  'MAN', #12
  'SZX', #13
  'SHA', #14
  'XMN' #15
])

class Observation():
  def __init__(self, spy_position, agent1_position, agent2_position, target_position):
    self.state = self.create_state(spy_position, agent1_position, agent2_position, target_position)
   
  def create_state(self, spy_position, agent1_position, agent2_position, target_position):

    spy_position, agent1_position, agent2_position, target_position = self.getIndexesFromAirPortIds(spy_position, agent1_position, agent2_position, target_position)

    state = dict({
      'spyPosition': spy_position, 
      'agent1Position': agent1_position, 
      'agent2Position': agent2_position,
      'targetPosition': target_position
      })

    return state

  def getIndexesFromAirPortIds(self, spy_position, agent1_position, agent2_position, target_position):
    spy_position = self.getAgentRowAndColumn(np.where(AIRPORTS== spy_position))
    agent1_position = self.getAgentRowAndColumn(np.where(AIRPORTS== agent1_position))
    agent2_position = self.getAgentRowAndColumn(np.where(AIRPORTS== agent2_position))
    target_position = self.getAgentRowAndColumn(np.where(AIRPORTS== target_position))

    return spy_position, agent1_position, agent2_position, target_position

  
  def getAgentRowAndColumn(self, indexInAirPortArray):
      row = indexInAirPortArray[0] // 4
      col = indexInAirPortArray[0] % 4
      return [int(row), int(col)]
    
  def get_air_port_id_by_index(self, airport_index):
    return AIRPORTS[airport_index]

# BKK ='BKK'
# SHA = 'SHA'
# LGA = 'LGA'
# obs = Observation('BKK','SHA','LGA')

# # res = obs.predict()

# # res = res[0]
# # print(res)
# res = obs.getIndexesFromAirPortIds(BKK, SHA, LGA)

# print(res)


      


