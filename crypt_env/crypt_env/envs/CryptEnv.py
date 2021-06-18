import gym
import pandas as pd
import numpy as np
from gym import spaces
from .Clock import Clock
from .Observer import ObserverScheme 
from .Portfolio import Porfolio



class CryptEnv(gym.Env):
    """A Bitcoin trading environment for OpenAI gym"""

    metadata = {"render.modes": ["live", "file", "none"]}
    viewer = None

    def __init__(
        self,
        df,
        lookback_window_size=50,
        commission=0.001,
        initial_balance=10000,
        serial=False,
    ):
        super(CryptEnv, self).__init__()
        self.df = df.reset_index()

        self.lookback_window_size = lookback_window_size
        self.commission = commission
        self.serial = serial

        self.clock = Clock(dataset_length=df.shape[0], window_look_back=self.lookback_window_size, episode=self.serial )
        self.os = ObserverScheme(dataset=df, clock=self.clock)
        self.pf = Porfolio()
        self.action_space = spaces.Discrete(2)
        self.observation_space = self.os.observation_space

        
        self.initial_balance = initial_balance
     


    def step(self, action):
        df_row = self.os.dataset_active_row
        # print('feeeee')
        self.pf.process(action, df_row['Close'])

        reward = self.pf.last_move

        done = True if self.clock.steps_left == 0 else False

        self.clock.increment()

        if not done:
            self.os.update_observations()

        obs = self.os.observations

        return obs, reward, done, {} 

    def reset(self):
        self.clock.reset()
        self.os.reset()
        self.pf.reset()

        return self.os.observations

    def render(self, mode='human', **kwargs):
        # print('self.net_worth')
        pass