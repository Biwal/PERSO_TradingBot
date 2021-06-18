#!/usr/bin/env

from stable_baselines3 import PPO
import crypt_env
from utils.EnvMaker import EnvMaker
from utils.Evaluator import Evaluator
from crypt_env.envs.CryptEnv import CryptEnv

if __name__ == "__main__":

    em = EnvMaker()
    eva = Evaluator()

    # window_look_back=5
    for window_look_back in [2]:
        partial_timesteps = 100000

        env_args = {
            "lookback_window_size": window_look_back,
            "serial":False
        }
        train_env, _ = em.make_dummy_train_test_env(env_args)

        model = PPO(
            "MlpPolicy",
            train_env,
            verbose=1,
            seed=1,
            tensorboard_log=f"./logs/",
            batch_size=256,
            gamma=0.9999,
            learning_rate=7.77e-05,
            ent_coef=0.00429,
            clip_range=0.1,
            n_epochs=10,
            gae_lambda=0.9,
            max_grad_norm=5,
            vf_coef=0.19,
        )

        model.learn(total_timesteps=partial_timesteps)


        env_args = {
            "lookback_window_size": window_look_back,
        }
        _, test_env = em.make_dummy_train_test_env(env_args)
        eva.evaluate_model(model, test_env)
