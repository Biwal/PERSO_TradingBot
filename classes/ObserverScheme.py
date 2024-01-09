import numpy as np 
import pandas as pd 
import gymnasium as gym 
from collections import deque 
from .Clock import Clock 
from .Wallet import Wallet

class ObserverScheme:
    def __init__(self, dataset : pd.DataFrame, clock : Clock, wallet: Wallet ) -> None:
        self._dataset = dataset
        self._clock = clock
        self._wallet = wallet

        self._obs = deque(maxlen = self._clock.window_look_back + 1)
        self._obs_cols = [
            'bid',
            'ask',
            'eur'
            ]
        self.reset()

    @property
    def observations(self):
        state = pd.DataFrame(
            np.array(self._obs), columns=self._obs_cols
        )
        return state.values.flatten()
    
    @property
    def dataset_active_row(self):
        return self._dataset.iloc[self._clock.current_index, :]
    
    @property
    def observation_space(self):
        return gym.spaces.Box(low=-10, high=10, shape=self.observations.shape)
    
    @property
    def history(self):
        return self._hist_obs
    
    def reset(self):
        self._init_histo()
        self._init_obs()

    def update_observations(self):
        obs_tmp = self._compute_obs(self._clock.current_index)
        self._obs.append(obs_tmp)
        self._save_obs(obs_tmp)

    
    def _init_obs(self):
        for i in range(
            self._clock.current_index - self._clock.window_look_back,
            self._clock.current_index + 1
        ):
            obs_tmp = self._compute_obs(i)
            self._obs.append(obs_tmp)
    
    def _compute_obs(self, row_index):
        current_row = self._dataset.iloc[row_index, :]
        obs = [
            current_row['BO'],
            current_row['AO'],
            self._wallet.current_euros
        ]
        return obs
    

    def _init_histo(self):
        ...

    def _save_obs(self, obs):
        ...

    
    