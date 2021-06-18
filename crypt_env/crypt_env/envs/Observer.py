import numpy as np
import pandas as pd
from gym import spaces
from collections import deque
import pandas_ta as ta
from .Clock import Clock

class ObserverScheme:
    def __init__(self, dataset: pd.DataFrame, clock: Clock) -> None:
        self._dataset = dataset
        self._clock = clock

        self._observations = deque(maxlen=self._clock.window_look_back + 1)
        ###
        self._observation_columns = ["fwma", 'obv']
        self.reset()

    @property
    def observations(self) -> pd.DataFrame:
        state = pd.DataFrame(
            np.array(self._observations), columns=self._observation_columns
        )
        return state.values.flatten()

    @property
    def dataset_active_row(self) -> pd.Series:
        return self._dataset.iloc[self._clock.current_index, :]

    @property
    def observation_space(self) -> spaces.Box:
        return spaces.Box(low=-10, high=10, shape=self.observations.shape)

    def reset(self) -> None:
        self._set_initial_obs()

    def update_observations(self) -> None:
        obs_values = self._compute_obs(index=self._clock.current_index)
        # print('PBBBBBB')
        self._observations.append(obs_values)

    def _set_initial_obs(self) -> None:

        for i in range(
            self._clock.current_index - self._clock.window_look_back,
            self._clock.current_index + 1,
        ):
            obs_values = self._compute_obs(index=i)
            self._observations.append(obs_values)

    def _compute_obs(self, index: int) -> list:

        sub_df = self._dataset.iloc[
            self._clock.current_index
            - self._clock.window_look_back : self._clock.current_index
        ]
        # print('XX')
        # print(self._dataset)
        # print(sub_df)
        fwma = ta.fwma(sub_df['Close'], length=(self._clock.window_look_back-1)).mean()
        obv = ta.obv(sub_df['Close'], sub_df['Close']).mean()
        ###
        obs = [fwma, obv]
        return obs

