import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
import numpy as np

# Generate dummy data
data = np.random.rand(1000, 20)

# Define the autoencoder model
input_dim = data.shape[1]
encoding_dim = 10

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)

autoencoder = Model(input_layer, decoded)

# Compile the model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the model
autoencoder.fit(data, data, epochs=50, batch_size=256, shuffle=True, validation_split=0.2)

# Encode and decode some data
encoded_data = autoencoder.predict(data)
decoded_data = autoencoder.predict(encoded_data)

print("Original Data: ", data[0])
print("Reconstructed Data: ", decoded_data[0])
import matplotlib.pyplot as plt

# Plot original and reconstructed data
n = 10  # Number of samples to plot
plt.figure(figsize=(20, 4))
for i in range(n):
    # Original data
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(data[i].reshape(1, -1), cmap='gray')
    plt.title("Original")
    plt.axis('off')

    # Reconstructed data
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_data[i].reshape(1, -1), cmap='gray')
    plt.title("Reconstructed")
    plt.axis('off')

plt.show()