import tensorflow as tf
from tensorflow.keras import layers

class architecture:
    def __init__(self,max_players,lstm_depth):
        self.max_players = max_players
        self.output_number = 36*self.max_players + 1
        self.lstm_depth = lstm_depth
        self.model_make()

    def model_make(self):
        view_input = tf.keras.Input(shape=(None,self.max_players+5))
        whole_seq_output, final_memory_state, final_carry_state = layers.LSTM(self.lstm_depth,return_sequences=False,return_state=True)(view_input)
        dice_input = tf.keras.Input(shape=(6))
        mixed = layers.Concatenate()([final_carry_state,dice_input])
        mixed = layers.Dense(30,activation=tf.keras.activations.relu)(mixed)
        mixed = layers.Dense(30,activation=tf.keras.activations.relu)(mixed)
        output = layers.Dense(self.output_number)(mixed)
        mid = tf.keras.Model([view_input,dice_input],output)
        self.model = mid