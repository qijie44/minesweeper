"""
Well, it can play and train continuously, but it's really crappy
TODO: insert skips when the whole array is -np.inf or 0 (it's equivalent coin toss then)
TODO: maybe properly implement an epsilon greedy function (need to read up first)
TODO: implement the save and load models (read https://www.tensorflow.org/tutorials/keras/save_and_load)
TODO: look up why the loss is nan (fixed, was using np.inf) and accuracy 1 (def something wrong with the model here)
"""

import tensorflow as tf
from selenium import webdriver
import numpy as np
import time as t
import minesweeper_interface as mi
import random as r


def check_unclicked(board, height, width, game):
    for h in range(2, height - 1):
        for w in range(2, width - 1):
            # putting 100 here, as -np.inf is causing the prediction to go to nan
            if board[h, w] == 100:
                #print("height: {}, {}".format(h-2, h+3))
                #print("width: {}, {}".format(w-2, w+3))
                array = board[h-2:h+3, w-2:w+3]
                if game != 0:
                    prediction = model(np.array([array]))
                    probability = tf.nn.softmax(prediction).numpy()
                    print("array:")
                    print(array)
                    print("probability: {}".format(probability))
                    # fake epsilon greedy function
                    if np.log10(game) > r.random():

                        if probability == 1:
                            mi.click_cell(h-1, w-1, driver)
                            return array
                    else:
                        # explore!
                        mi.click_cell(h - 1, w - 1, driver)
                        return array
                else:
                    mi.click_cell(h-1, w-1, driver)
                    return array


# Initialise replay memory, 1st array is a list of 5x5 arrays, 2nd array
replay_memory = [[], []]

# start the browser and load the game
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chromeOptions)
driver.get('http://minesweeperonline.com/#')

# Initialise the nn. It should take a 5x5 matrix and output a reward (inverse of probability)
model = tf.keras.models.Sequential(())
model.add(tf.keras.layers.Flatten(input_shape=(5, 5)))
# 1 dense layers with 25 units and ReLU activation
model.add(tf.keras.layers.Dense(25, activation="relu"))
# q dense layer with 25 units and linear activation
model.add(tf.keras.layers.Dense(1, activation="linear"))
# using cross entropy as the loss function
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer="adam", loss=loss_fn, metrics=['accuracy'])
model.summary()

t.sleep(3)
mi.click_cell(1, 1, driver)

# a counter to check how many games were played
game = 0

while game < 10:
    if not mi.check_death(driver):
        board = mi.get_board_state(driver)
        height, width = board.shape
        array = check_unclicked(board, height, width, game)
        replay_memory[0].append(array)
        if not mi.check_death(driver):
            replay_memory[1].append(1)
        else:
            replay_memory[1].append(0)
    else:
        # pulling the data from replay_memory
        (x_train, y_train) = replay_memory
        # training the nn
        print("x: {}".format(x_train))
        print("y: {}".format(y_train))
        model.fit(np.array(x_train), np.array(y_train), epochs=len(x_train))
        # clean out the replay memory, reset the game and add to the game counter
        replay_memory = [[], []]
        mi.reset(driver)
        game += 1
        t.sleep(3)
        mi.click_cell(1, 1, driver)
