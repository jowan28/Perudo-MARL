from q_net import architecture
import numpy as np
import random
import tensorflow as tf
import csv

class script:
    def __init__(self,file_location):
        self.csv_log = file_location

    def write_to_log(self,row):
        with open(self.csv_log, 'a') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(row)

# Define the Q-learning agent with a Q-network
class QLearningAgent:
    def __init__(self, players, epsilon=0.1, learning_rate=0.1, discount_factor=0.9):
        self.n_actions = 6*players + 1
        self.epsilon = epsilon
        self.name = []
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_network = architecture(players,8)
        self.optimizer = tf.keras.optimizers.Adam(learning_rate)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            q_values = self.q_network.model.predict(state)
            return np.argmax(q_values) 

    def update_q_network(self, state, action, reward, next_state):
        print(state)
        with tf.GradientTape() as tape:
            q_values = self.q_network.model(state)
            next_q_values = self.q_network.model(next_state)
            target_q = q_values.numpy()
            target_q[0,int(action)] = reward + self.discount_factor * np.max(next_q_values)
            loss = tf.reduce_mean(tf.square(target_q - q_values))
        grads = tape.gradient(loss, self.q_network.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.q_network.model.trainable_variables))


# Define the training loop
def train_perudo_agents(env, agents, episodes, agent_number, script_location):
    scribe = script(script_location)
    for episode in range(episodes):
        #state_store = np.zeros((len(agents)))
        state_store = 0
        action_store = 0
        reward_store = 0
        env.reset()
        done = False
        failed = False
        while (not done) or (failed):
            #current state = next state
            cur_ID = env.current_player.name
            if cur_ID == 0:
                #pick the correct agent
                if failed:
                    #we still need to train the model
                    print('correcting bad bid')
                    agents.update_q_network(state_store, action_store, reward_store, failed_state)
                    failed = False
                else:
                    state = [tf.convert_to_tensor(np.expand_dims(env.bet_history,axis=0)), tf.convert_to_tensor(np.expand_dims(env.current_player.Dice_numbers(),axis=0))]
                    if state_store != 0:
                        agents.update_q_network(state_store, action_store, reward_store, state)
                    action = agents.choose_action(state)
                    reward, done, failed = env.step(action)
                    if failed:
                        failed_state = state
                    row = [episode,cur_ID,reward]
                    scribe.write_to_log(row)
                    #store state, action, reward
                    state_store = state
                    action_store = action
                    reward_store = reward
            else:
                #computer player
                action = 0
                #the computer doesnt care
                reward, done, failed = env.step(action)
