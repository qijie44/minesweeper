import random as r
import numpy as np
import pickle as p

memory = [[],[]]

for i in range(100000):
    bomb_num = int(r.gauss(10.10, 10.10))
    uncovered_squares = r.randint(9,15)

    minefield = np.ones((7,7))

    pad_rand = r.randint(0, 8)

    if pad_rand != 0:
        top = int(pad_rand/3)+1
        side = pad_rand%3+1
        minefield[:top, :] = 0.9
        minefield[:, :side] = 0.9

    for bomb in range(bomb_num):
        h = r.randint(0, 6)
        w = r.randint(0, 6)
        if minefield[h][w] != 0.9:
            minefield[h][w] = 10

    temp_minefield = np.pad(minefield, 1)
    for squares in range(uncovered_squares):
        h = r.randint(1, 5)
        w = r.randint(1, 5)
        if (h != 3) and (w != 3):
            if minefield[h][w] == 1:
                subarray = minefield[h - 1:h + 2,w - 1:w + 2]
                minefield[h][w] = int(subarray.sum()/10)/10

    np.rot90(minefield, r.randint(0,3))

    minefield = minefield[1:-1,1:-1]
    if minefield[2][2] == 10:
        death = True
    else:
        death = False

    minefield = np.where(minefield==10, 1, minefield)

    if death:
        memory[0].append(minefield)
        memory[1].append(0)
    else:
        memory[0].append(minefield)
        memory[1].append(0.99)

with open(r"training_data.p", "wb") as f:
    p.dump(memory, f)
    f.close()
