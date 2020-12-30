"""
Well, it can play and train continuously, but it's really crappy
Done: insert skips when the whole array is -np.inf or 0 (it's equivalent coin toss then)
Done: maybe properly implement an epsilon greedy function (need to read up first)
DONE: implement the save and load models (read https://www.tensorflow.org/tutorials/keras/save_and_load)
DONE: look up why the loss is nan (fixed, was using np.inf) and accuracy 1 (fixed by normalising the data in)
"""

import tensorflow as tf
from selenium import webdriver
import numpy as np
import time as t
import minesweeper_interface as mi
import random as r
from os import path
import pickle as p


def check_unclicked(board, height, width, game):
    predictions = [[], [], []]
    for h in range(2, height - 1):
        for w in range(2, width - 1):
            # putting 1 here, as -np.inf is causing the prediction to go to nan
            if board[h, w] == 1:
                #print("height: {}, {}".format(h-2, h+3))
                #print("width: {}, {}".format(w-2, w+3))
                array = board[h-2:h+3, w-2:w+3]
                # forcing checks only on arrays with at least 5 labelled cells to get useful information
                if ((0.9 == array) | (array == 1)).sum() < 21:
                    subarray = array[1:-1,1:-1]
                    # making sure that there's at least 1 revealed cell beside the cell being evaluated
                    if ((0.9 == subarray) | (subarray == 1)).sum() != 9:
                        # if it's not the first game, add the option to the prediction list, else just click it for data
                        if game != 0:
                            predictions[0].append(array)
                            predictions[1].append(model(np.array([array])).numpy())
                            predictions[2].append((h, w))
                        else:
                            mi.click_cell(h-1, w-1, driver)
                            return array, "nil"
    # epsilon greedy function
    if 0.1 < r.random():
        print("best!")
        # turning part of the prediction list to array, to easily find the max
        probability_list = np.array(predictions[1])
        # getting the index  of the highest probability
        index = np.argmax(probability_list)
        #print(index)
        #print(predictions)
        probability = predictions[1][index]
    else:
        # explore!
        print("explore!")
        index = r.randint(0, len(predictions[2])-1)
        probability = "explore"
    array = predictions[0][index]
    h, w = predictions[2][index]
    mi.click_cell(h - 1, w - 1, driver)
    return array, probability

# Initialise replay memory, 1st array is a list of 5x5 arrays, 2nd array
replay_memory = [[], []]

# start the browser and load the game
chromeOptions = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chromeOptions)
driver.get('http://minesweeperonline.com/#')

# if a previous model exists
if path.isdir("minesweeper_model"):
    model = tf.keras.models.load_model("minesweeper_model")
    full_memory = p.load(open("minesweeper_model/full_memory", "rb"))
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
    modified_adam = tf.keras.optimizers.Adam(learning_rate=0.00001)
    model.compile(optimizer=modified_adam, loss=loss_fn, metrics=['accuracy'])
    full_memory = [[], [], []]
model.summary()

t.sleep(3)
mi.click_cell(5, 5, driver)

# a counter to check how many games were played
game = 0

while game < 1000:
    if not mi.check_death(driver):
        board = mi.get_board_state(driver)
        height, width = board.shape
        array, prediction = check_unclicked(board, height, width, game)
        print(array)
        replay_memory[0].append(array)
        full_memory[0].append(array)
        full_memory[2].append(prediction)
        if not mi.check_death(driver):
            replay_memory[1].append(0.99)
            full_memory[1].append(0.99)
        else:
            replay_memory[1].append(0)
            full_memory[1].append(0)
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
        p.dump(full_memory, open(r"minesweeper_model/full_memory.p", "wb"))
        t.sleep(3)
        mi.click_cell(5, 5, driver)