from selenium import webdriver
import numpy as np
import time as t
import minesweeper_interface as mi

np.set_printoptions(precision=3, threshold=np.inf)

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chromeOptions)

driver.get('http://minesweeperonline.com/#')

#print(get_board_state(driver))
#print(mines_left(driver))
#print(get_time(driver))
mi.click_cell(4,4,driver)
mi.reset(driver)

#driver.close()