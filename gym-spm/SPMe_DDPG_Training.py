import gym
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3 import PPO, TD3, DDPG
from stable_baselines3.common.vec_env.vec_check_nan import VecCheckNan
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.cmd_util import make_vec_env
# from stable_baselines3.common.utils import set_random_seed
# from stable_baselines3.common.vec_env import DummyVecEnv

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.td3.policies import MlpPolicy

from stable_baselines3.common.noise import NormalActionNoise

if __name__ == '__main__':
    env_id = 'gym_spm:spm-v0'
    num_cpu = 4  # Number of processes to use

    train = True

    env = gym.make('gym_spm:spm-v0')

    # The noise objects for DDPG
    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=25.67 * np.ones(n_actions))
    model = DDPG(MlpPolicy, env, action_noise=action_noise, verbose=1, tensorboard_log="./DDPG_spm_v2_SOC_point5_two_state/")
    # model = TD3(MlpPolicy, env, action_noise=action_noise, verbose=1, tensorboard_log="./TD3_spm_v2_SOC_point5_two_state/")

    if train:
        model.learn(total_timesteps=2500000, tb_log_name='test_run_3_SOCpoint5_two_state')
        model.save('TD3_test_3_SOC_point5_two_states')
    else:
        model.load('TD3_test_2_SOC_point5_two_states')

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
    
    print("Mean Reward = ", mean_reward)
    
    epsi_sp_list = []
    action_list = []
    soc_list = []
    Concentration_list = []
    Concentration_list1 = []
    
    obs = env.reset()
    for _ in range(3600):
    
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, done, info = env.step(action)
    
        epsi_sp_list.append(env.epsi_sp.item(0))
        # Concentration_list.append(env.state_output['yp'].item())
        # Concentration_list.append(env.state_output['yn'].item())
        soc_list.append(env.state_of_charge.item())
    
        action_list.append(action)
    
        if done:
            break
            # obs = env.reset()
 
    plt.figure()
    plt.plot(soc_list)
    plt.show()
    
    
    plt.figure()
    plt.plot(epsi_sp_list)
    plt.title("Sensitivity Values")
    
    plt.figure()
    plt.plot(action_list)
    plt.title("Input Currents")
    plt.show()
