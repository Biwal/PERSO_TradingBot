from abc import ABC, abstractmethod
from collections import deque
import pandas as pd
import gymnasium as gym

class ActionScheme(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self._action_space = gym.spaces.Discrete(3, start=0)

    @property
    def action_space(self):
        return self._action_space
    
    @property
    def history(self):
        return pd.DataFrame({
            "action" : self._hist_action
        })
    
    def reset(self):
        self._hist_action = deque()

    def _save_action(self, action):
        self._hist_action.append(action)

    @abstractmethod
    def compute_action(self, action):
        raise NotImplementedError()
    
class AgentAction(ActionScheme):
    def compute_action(self, action):
        self._save_action(action)
        return action

class BaselineAction(ActionScheme):
    def compute_action(self, action = None):
        baseline_action = 0
        self._save_action(baseline_action)
        return baseline_action

class RandomAction(ActionScheme ):
    def compute_action(self, action = None):
        random_action = self.action_space.sample()
        self._save_action(random_action)
        return random_action
    