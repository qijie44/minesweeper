import numpy as np


def get_board_state(driver):
    board = np.empty([16, 30])
    for x in range(1, 17):
        for y in range(1, 31):
            cell = driver.find_element_by_id("{}_{}".format(x, y))
            cell_content = cell.get_attribute("class")
            if "blank" in cell_content:
                # putting 100 here, as -np.inf is causing the prediction to go to nan
                board[x - 1][y - 1] = 100
            for i in range(0, 9):
                if str(i) in cell_content:
                    board[x - 1][y - 1] = i
    board = np.pad(board, 2, mode="constant", constant_values=0)
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