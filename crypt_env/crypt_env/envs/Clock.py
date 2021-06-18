import random
class Clock:
    def __init__(
        self, dataset_length: int, window_look_back: int = 0, init_index: int = 0, episode_length:int=250, episode:bool=False
    ) -> None:
        self._dataset_length = dataset_length
        self._window_look_back = window_look_back
        self._init_index = init_index
        self._episode_length = episode_length
        self._episode = episode
        self.reset()

    @property
    def current_step(self):
        return self._current_step

    @property
    def steps_left(self):
        return self._steps_left

    @property
    def current_index(self):
        return self._current_index

    @property
    def window_look_back(self):
        return self._window_look_back

    def increment(self):
        self._current_step += 1
        self._current_index += 1
        self._steps_left -= 1

    def reset(self):
        self._current_step = 0
        if self._episode:
            self._steps_left = self._episode_length
            min_begin_index = 0 + self._window_look_back + self._init_index
            max_begin_index = self._dataset_length - 1 - self._episode_length
            self._current_index = random.randint(min_begin_index, max_begin_index)
        else:    
            self._steps_left = (
                self._dataset_length - 1 - self._window_look_back - self._init_index
            )   
            self._current_index = 0 + self._window_look_back + self._init_index

        # print(' FIN '*10)
