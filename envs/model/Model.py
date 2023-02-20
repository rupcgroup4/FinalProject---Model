from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy

from sb3_contrib.ppo_mask import MaskablePPO
import os


class Model():

  def __init__(self, env, name, isNew=False):
    self.log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs', 'PPO', name)
    self.save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'SavedModels', 'PPO',name)

    self.env = env

    #if isNew == True create new model otherwise load existing model
    if isNew:
        # self.model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=self.log_path)
        self.model = MaskablePPO(MaskableActorCriticPolicy, self.env, verbose=1)
    else:
        # self.model = PPO.load(self.save_path+'/best_model', env=env)
        self.model = MaskablePPO.load(self.save_path+'/best_model', env=self.env)

    self.eval_call_back()

    
  def eval_call_back(self):
     #Specify on after which average reward to stop the training
    stop_callback = StopTrainingOnRewardThreshold(reward_threshold=1, verbose=1)
    #Callback that going to get triggered after each training round
    self.eval_callback = EvalCallback(self.env,
                                #call the callback on each new best score
                                callback_on_new_best=stop_callback,
                                #call the callback each 5000 rounds
                                eval_freq=5000,
                                #save the best model as file
                                best_model_save_path=self.save_path,
                                verbose=1,
                                log_path=self.log_path
                                )

  def learn(self, total_timesteps=1000):
    self.model.learn(total_timesteps=total_timesteps)
    # self.model.save(self.save_path)


  def evaluate_model(self, episodes=10):
    print(evaluate_policy(self.model, self.env, n_eval_episodes=episodes)) #Output (score, std(standard deviation)) 


  def predict(self, obs):
    action, _states = self.model.predict(obs, action_masks=self.env.mask_actions()) 
    return action

  def test_model(self, episodes):
    steps = 0
    for episode in range(1, episodes+1):
        #Reseting the environment to start new game(Episode)
        obs = self.env.reset() 
        done = False
        score = 0
        
        while not done:
            #Using Model predict nad not a random action
            action = self.predict(obs)
            obs, reward, done, info = self.env.step(action) #Take step based on model prediction
            score += reward
            steps +=1
    win, lose, ilegal_step = self.env.stats()
    # if(win > 0):
    # return {
    #   'state':  self.env.initial_state,
    #   'win': win,
    #   'lose': lose,
    #   'ilegal': ilegal_step
    # }
    print(f'win {win}, lose {lose}, steps {steps}, ilegal {ilegal_step}')
  
    

