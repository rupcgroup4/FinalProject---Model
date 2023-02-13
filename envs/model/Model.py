from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
import os


class Model():

  def __init__(self, env, isNew=False):
    self.log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs', 'PPO', env.__class__.__name__)
    self.save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'SavedModels', 'PPO', env.__class__.__name__)

    self.env = env

    #if isNew == True create new model otherwise load existing model
    if isNew:
        self.model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=self.log_path)
    else:
        self.model = PPO.load(self.save_path, env=env)

    
    
  def learn(self, total_timesteps=1000):
    self.model.learn(total_timesteps=total_timesteps)
    self.model.save(self.save_path)


  def evaluate_model(self, episodes=10):
    print(evaluate_policy(self.model, self.env, n_eval_episodes=episodes)) #Output (score, std(standard deviation)) 

  def test_model(self, episodes):
    steps = 0
    for episode in range(1, episodes+1):
        #Reseting the environment to start new game(Episode)
        obs = self.env.reset() 
        done = False
        score = 0
        
        while not done:
            #Using Model predict nad not a random action
            action, _states = self.model.predict(obs) 
            obs, reward, done, info = self.env.step(action.item()) #Take step based on model prediction
            print(obs)
            score += reward
            steps +=1
    win, lose, ilegal_step = self.env.stats()
    print(f'win {win}, lose {lose}, steps {steps}, ilegal {ilegal_step}')
  
  def predict(self, obs):
    return self.model.predict(obs)
    

