import numpy as np
from selenium import common


def get_board_state(driver):
    try:
        driver.find_element_by_id("100_1")
    except common.exceptions.NoSuchElementException:
        print("itworsk")
    for x in range(1, 100):
        try:
            cell = driver.find_element_by_id("{}_1".format(x))
            if cell.get_attribute("style") == "display: none;":
                col = x-1
                break
        except common.exceptions.NoSuchElementException:
            col = x-1
            break
    for y in range(1, 100):
        try:
            cell = driver.find_element_by_id("1_{}".format(y))
            if cell.get_attribute("style") == "display: none;":
                row = x-1
                break
        except common.exceptions.NoSuchElementException:
            row = y-1
            break
    print("col:{}, row:{}".format(col, row))
    board = np.empty([col, row])
    for x in range(1, col+1):
        for y in range(1, row+1):
            cell = driver.find_element_by_id("{}_{}".format(x, y))
            cell_content = cell.get_attribute("class")
            if "blank" in cell_content:
                # putting 1 here, as -np.inf is causing the prediction to go to nan
                board[x - 1][y - 1] = 1
            # the 0-8 here is for the number of mines
            for i in range(0, 8):
                if str(i) in cell_content:
                    board[x - 1][y - 1] = i/10
    return board

def get_padded_board_state(driver):
    board = np.pad(board, 2, mode="constant", constant_values=0.9)
    return board

def mines_left(driver):
    hundreds = driver.find_element_by_id("mines_hundreds")
    tens = driver.find_element_by_id("mines_tens")
    ones = driver.find_element_by_id("mines_ones")
    return int(hundreds.get_attribute("class").strip("time") + tens.get_attribute("class").strip("time") + ones.get_attribute("class").strip("time"))

def get_time(driver):
    hundreds = driver.find_element_by_id("seconds_hundreds")
    tens = driver.find_element_by_id("seconds_tens")
    ones = driver.find_element_by_id("seconds_ones")
    return int(hundreds.get_attribute("class").strip("time") + tens.get_attribute("class").strip("time") + ones.get_attribute("class").strip("time"))

def click_cell(x, y, driver):
    cell = driver.find_element_by_id("{}_{}".format(x, y))
    print("clicked: {},{}".format(x,y))
    cell.click()

def reset(driver):
    driver.find_element_by_id("face").click()

def check_death(driver):
    if driver.find_element_by_id("face").get_attribute("class") == "facesmile":
        return False
    else:
        return True