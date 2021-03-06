#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 02:10:33 2017

@author: levimcclenny
"""


import numpy as np
import matplotlib.pyplot as plt



time = 10000
runs = 2000

def k_bandit_testbed(arms, time, runs, eps, stationary = True, 
                      constant_step = False, step_size = .1, 
                      optimistic = False, opt_mean = 5):
    
    final_reward = [[] for i in range(0,len(eps))]
    optimal_action = [[] for i in range(0,len(eps))]
    for k in range(len(eps)):
        Rewards = np.zeros(time)
        OptimalAction = np.zeros(time)
        for i in range(runs):
            q_star = np.random.normal(0,1,arms)
            bestAction = np.argmax(q_star)
            q_est = np.zeros(arms)
            if optimistic:
                q_est = np.repeat(float(opt_mean), arms)
            counts = np.zeros(arms)
            rew = []
            #optimal_count = 0
            optimalAction = []
            for j in range(0,time):
                optimal_count = 0
                if eps[k] > np.random.random(): 
                    action = np.random.randint(arms)
                else:
                    action = np.argmax(q_est)
                if action == bestAction:
                    optimal_count = 1
                reward = q_star[action] + np.random.normal(0,1)
                counts[action] +=1
                if constant_step:
                    q_est[action] += step_size*(reward - q_est[action])
                else:
                    q_est[action] += (1/counts[action])*(reward - q_est[action])
                if not stationary:
                    q_star += np.random.normal(0,.01,arms)
                    bestAction = np.argmax(q_star)
                rew.append(reward)
                optimalAction.append(optimal_count)
            Rewards += rew
            OptimalAction += optimalAction
        
        final_reward[k] = Rewards/runs
        optimal_action[k] = OptimalAction/runs
    return final_reward, optimal_action

rewardOpt, actionOpt = k_bandit_testbed(10, 1000, 2000, [0], constant_step = True, optimistic = True)
rewardReal, actionReal = k_bandit_testbed(10, 1000, 2000, [0.1], constant_step = True)


#plt.subplot(212)
plt.plot(actionOpt[0], label = "Optimistic/Greedy, $Q_{1} = 5, \epsilon = 0$")
plt.plot(actionReal[0], label = "Realistic/$\epsilon$-Greedy, $Q_{1} = 0, \epsilon =0.1$")
plt.legend()
plt.xlabel('Steps')
plt.ylabel('% optimal action')
plt.legend()


