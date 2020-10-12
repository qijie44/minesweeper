"""
Well, it can play and train continuously, but it's really crappy
Done: insert skips when the whole array is -np.inf or 0 (it's equivalent coin toss then)
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
from os import path


def check_unclicked(board, height, width, game):
    for h in range(2, height - 1):
        for w in range(2, width - 1):
            # putting 1 here, as -np.inf is causing the prediction to go to nan
            if board[h, w] == 1:
                #print("height: {}, {}".format(h-2, h+3))
                #print("width: {}, {}".format(w-2, w+3))
                array = board[h-2:h+3, w-2:w+3]
                # forcing checks only on arrays with at least 5 labelled cells to get useful information
                if ((0.9 == array) | (array == 1)).sum() < 21:
                    if game != 0:
                        prediction = model(np.array([array]))
                        probability = prediction.numpy()
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
driver = webdriver.Chrome(options=chromeOptions)
driver.get('http://minesweeperonline.com/#')

# if a previous model exists
if path.isdir("minesweeper_model"):
    model = tf.keras.models.load_model("minesweeper_model")
else:
    # Initialise the nn. It should take a 5x5 matrix and output a reward (inverse of probability)
    model = tf.keras.models.Sequential(())
    model.add(tf.keras.layers.Flatten(input_shape=(5, 5)))
    # 2 dense layers with 25 units and ReLU activation
    model.add(tf.keras.layers.Dense(25, activation="relu"))
    model.add(tf.keras.layers.Dense(25, activation="relu"))
    # 1 dense layer with 25 units and sigmoid activation
    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))
    # using cross entropy as the loss function
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer="adam", loss=loss_fn, metrics=['accuracy'])
model.summary()

t.sleep(3)
mi.click_cell(1, 1, driver)

# a counter to check how many games were played
game = 0

while game < 1000:
    if not mi.check_death(driver):
        board = mi.get_board_state(driver)
        height, width = board.shape
        array = check_unclicked(board, height, width, game)
        replay_memory[0].append(array)
        if not mi.check_death(driver):
            replay_memory[1].append(0.99)
        else:
            replay_memory[1].append(0)
    else:
        # pulling the data from replay_memory
        (x_train, y_train) = replay_memory
        # training the nn
        print("x: {}".format(x_train))
        print("y: {}".format(y_train))
        model.fit(np.array(x_train), np.array(y_train), epochs=len(x_train))
        # clean out the replay memory, reset the game, add to the game counter and save the model
        replay_memory = [[], []]
        mi.reset(driver)
        game += 1
        model.save("minesweeper_model")
        t.sleep(3)
        mi.click_cell(1, 1, driver)
