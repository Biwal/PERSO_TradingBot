#!/usr/bin/env
import gym
import json
import datetime as dt

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from TradingBotGymEnv import TradingBotGymEnv

import pandas as pd

df = pd.read_csv('AAPL.csv')
df = df.sort_values('Timestamp')

# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: TradingBotGymEnv(df)])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10)

obs = env.reset()
for i in range(10):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
   