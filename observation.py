import numpy as np
from stable_baselines3 import PPO
import os
from envs.flights import flights



class Observation():
  def __init__(self, spy_position, agent1_position, target_position):
    self.state = self.create_state(spy_position, agent1_position, target_position)
   
  def create_state(self, spy_position, agent1_position, target_position):

    for i in range(len(flights)):
      if flights[i]['id'] == spy_position:
        spy_position = i
      if flights[i]['id'] == agent1_position:
        agent1_position = i
      # if flights[i]['id'] == agent2_position:
      #   agent2_position = i
      if flights[i]['id'] == target_position:
        target_position = i
        

    state = dict({
      'spyPosition': spy_position, 
      'agentPosition': agent1_position, 
      # 'agent2Position': agent2_position,
      'targetPosition': target_position
      })

    return state

  

  def get_air_port_id_by_index(self, airport_index):
    for i in enumerate(flights):
      if i[0] == airport_index:
        return flights[i[0]]['id']




      


