"""
Attempt at trying to see if my construction of the model is flawed or the way i structured the problem was wrong.

TODO:
"""

#import tensorflow as tf
from selenium import webdriver
import numpy as np
import time as t
import minesweeper_interface as mi
import random as r

# start the browser and load the game
chromeOptions = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chromeOptions)
driver.get('http://minesweeperonline.com/#')
t.sleep(3)
# selecting the beginner game (smaller size, easier to build q learning matrix)
game_options = driver.find_element_by_id("options-link")
game_options.click()
option = driver.find_element_by_id("beginner")
option.click()
new_game = driver.find_element_by_class_name("dialogText")
new_game.click()

board = mi.get_board_state(driver)
height, width = board.shape

print(board)
print("height:{}".format(height))
print("width:{}".format(width))