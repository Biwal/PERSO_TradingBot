from abc import ABC, abstractmethod
from collections import deque
import pandas as pd
from .Wallet import Wallet

class RewarderScheme(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.reset()

    @property
    def history(self):
        return pd.DataFrame({
            "Récompense": self._hist_reward,
            "Récompense cumulé": self._hist_reward_sum,
            "Récompense moyenne": self._hist_reward_mean,
        })

    def reset(self):
        self._total_reward = 0

        self._hist_reward = deque()
        self._hist_reward_sum = deque()
        self._hist_reward_mean = deque()

    @abstractmethod
    def compute_reward(self, df_row):
        raise NotImplementedError()

    def _save_reward(self, reward):
        self._total_reward += reward

        self._hist_reward.append(reward)
        self._hist_reward_sum.append(self._total_reward)
        self._hist_reward_mean.append(self._total_reward / (len(self._hist_reward) + 1))

class MaximizeForex(RewarderScheme):
    def __init__(self) -> None:
        super().__init__()

    def compute_reward(self, wallet:Wallet):

        reward = wallet.current_value - wallet.previous_value
        self._save_reward(reward=reward)
        return reward