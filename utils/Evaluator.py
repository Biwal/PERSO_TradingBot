class Evaluator:
    def evaluate_model(self, model, env, n_eval_episodes: int = None):
        # len_eval = n_eval_episodes if n_eval_episodes is not None else env.clock.limit
        self.manual_evaluation(model, env)
        # self.sb_evaluation(env, model, len_eval)

    def sb_evaluation(self, env, model, n_eval_episodes):
        pass

    def manual_evaluation(self, model, env):
        obs = env.reset()
        suma = 0
        for i in range(200):
            action, _states = model.predict(obs, deterministic=True)
            obs, rewards, done, info = env.step(action)

            suma+=rewards
            # env.env_method('live_render')
        print(f"Récompense finale : {suma}")
        print('*'*50)
        env.render()
