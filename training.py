import pickle as p
import numpy as np

memory = p.load(open(r"training_data", "wb"))
print(memory)

x_train = memory[0]
y_train = memory[1]

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

model.fit(np.array(x_train), np.array(y_train), epochs=len(x_train))

model.save("minesweeper_model")