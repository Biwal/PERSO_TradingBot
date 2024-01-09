import numpy as np 
import pandas as pd 
import gymnasium as gym 
from .ActionScheme import AgentAction, BaselineAction, RandomAction
from .Clock import Clock
from .RewardScheme import MaximizeForex
from .ObserverScheme import ObserverScheme
from .Wallet import Wallet

import matplotlib.pyplot as plt
import seaborn as sns

class ForexEnv(gym.Env):
    metadata = {"render.modes" : ["human"]}

    def __init__(
            self,
            dataset,
            action_scheme = AgentAction(),
            rewarder_scheme = MaximizeForex(),
            window_look_back = 0,
            episodic = True,
            run_name = 'default'
            ) -> None:
        super().__init__()
        
        self._dataset = dataset
        self._window_look_back = window_look_back
        self._action_scheme = action_scheme
        self._rewarder_scheme = rewarder_scheme

        self._clock = Clock( 
            dataset_length = dataset.shape[0],
            window_look_back = self._window_look_back,
            episode = episodic   
        )

        self._wallet = Wallet()
        
        self._obs_scheme = ObserverScheme(
            dataset = dataset,
            clock = self._clock,
            wallet = self._wallet
        )

        self.action_space = self._action_scheme.action_space
        self.observation_space = self._obs_scheme.observation_space

    def step(self, action):
        dataset_active_row = self._obs_scheme.dataset_active_row
        action_def = self._action_scheme.compute_action(action)

        self._wallet.step(action = action_def, obs = dataset_active_row)

        reward = self._rewarder_scheme.compute_reward(self._wallet)

        terminated = True if self._clock.steps_left == 0 else False
        truncated = False

        self._clock.increment()

        if not terminated:
            self._obs_scheme.update_observations()

        obs = self._obs_scheme.observations

        return obs, reward, terminated, truncated, {}
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self._clock.reset()
        self._wallet.reset()
        self._action_scheme.reset()
        self._rewarder_scheme.reset()
        self._obs_scheme.reset()

        obs = self._obs_scheme.observations
        return obs,  {}

    def render(self, mode="human"):

        cumsum = self._rewarder_scheme.history["Récompense cumulé"].tail(1).values[0]
        mean = self._rewarder_scheme.history["Récompense cumulé"].tail(1).values[0] / self._rewarder_scheme.history.shape[0]
        description = f""" - Suivi de la récompense  :
        Nombre de récompenses enregistrées : {self._rewarder_scheme.history.shape[0]} 
        Récompense cumulé : {cumsum:.3e}
        Récompense moyenne : {mean:.3f} 
        """
        print(description)

        # sns.set_theme(
        #     style="darkgrid",
        #     rc={
        #         "axes.linewidth": 1,
        #         "axes.edgecolor": "black",
        #         "xtick.bottom": True,
        #         "ytick.left": True,
        #     },
        # )
        # sns.despine()
        # sns.set_palette("icefire")

    def _save_plot(self, figure):
        path = f"logs/recompense1.png"
        self._manage_dirs(path)
        figure.savefig(path)

    def _manage_dirs(self, path: str):
        import os, os.path
        import errno
        # https://stackoverflow.com/a/600612/119527
        try:
            os.makedirs(os.path.dirname(path), mode=0o777)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(os.path.dirname(path)):
                pass
            else:
                raise
        