from stable_baselines3.common.vec_env import DummyVecEnv, VecCheckNan, VecNormalize
import gym
from utils.DataLoader import DataLoader
import pandas as pd
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env


class EnvMaker:
    def __init__(self) -> None:
        self.dl = DataLoader()
        self.train, self.test = pd.DataFrame(), pd.DataFrame()

    def make_dummy_env(self, dataset, env_args):
        env = gym.make("crypt-v001", df=dataset, **env_args)
        check_env(env)
        env = DummyVecEnv([lambda: env])
        env = VecCheckNan(env, raise_exception=True)
        env = VecNormalize(
            env, norm_obs=True, norm_reward=False, clip_obs=10.0, gamma=0.95
        )
        return env

    def make_dummy_train_test_env(self, env_args):
        if (self.train.empty) or (self.test.empty) :
            self.train, self.test = self.dl.get_train_test_dataset()

        train_env = self.make_dummy_env(dataset=self.train, env_args=env_args)
        test_env = self.make_dummy_env(dataset=self.test, env_args=env_args)
        return train_env, test_env

    def make_vec_env(self,dataset, env_args):
        env_args["df"]= dataset
        env = make_vec_env('crypt-v001', env_kwargs=env_args)
        env = VecCheckNan(env, raise_exception=True)
        env = VecNormalize(
            env, norm_obs=True, norm_reward=False, clip_obs=10.0, gamma=0.95
        )
        return env

    def make_vec_train_test_env(self,env_args):
        if (self.train.empty) or (self.test.empty) :
            self.train, self.testd = self.dl.get_train_test_dataset()

        train_env = self.make_vec_env(dataset=self.train, env_args=env_args)
        test_env = self.make_vec_env(dataset=self.test, env_args=env_args)
        return train_env, test_env
