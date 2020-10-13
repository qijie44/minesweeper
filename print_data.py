import pickle as p


full_memory = p.load(open("minesweeper_model/full_memory", "rb"))

for i in range(len(full_memory[0])):
    print(full_memory[0][i])
    print("live?: {}".format(str(full_memory[1][i])))
    print("prediction: {}".format(str(full_memory[2][i])))