# This is a coding sample from my CS181 Practical: Classifying Sounds, Spring 2021.
# I create two data transformation functions for data augmentation through 1) Creating more data by adding noise and 2) Creating more data by shifting time.

# add noise
import numpy as np
np.random.seed(0) # reset the seed
def add_noise(data, noise_factor):
    noise = np.random.randn(data.shape[1])
    augmented_data = np.empty((data.shape[0], data.shape[1]))
    for i in range(data.shape[0]):
        augmented_data[i] = data[i] + noise_factor * noise
    # Cast back to same data type
    # augmented_data = augmented_data.astype(type(data[0]))
    return augmented_data

# time shift code
def time_shift(data, sampling_rate, shift_max, shift_direction):
    augmented_data = np.empty((data.shape[0], data.shape[1]))
    for i in range(data.shape[0]):
        shift = np.random.randint(sampling_rate * shift_max)
        if shift_direction == 'right':
            shift = -shift
        elif shift_direction == 'both':
            direction = np.random.randint(0, 2)
            if direction == 1:
                shift = -shift
        augmented_data[i] = np.roll(data[i], shift)
    return augmented_data

def main():
    class_dict = {0 : "air_conditioner", 
              1 : "car_horn",
              2 : "children_playing",
              3 : "dog_bark",
              4 : "drilling",
              5 : "engine_idling",
              6 : "gun_shot",
              7 : "jackhammer",
              8 : "siren",
              9 : "street_music"}

    X_amp_train_noise = add_noise(X_amp_train, 0.05)

    # view the difference between raw and noise data
    num = 30
    print(class_dict[y_amp_train[num]])
    plot_amp(X_amp_train[num])
    plot_amp(X_amp_train_noise[num])

    # add noise data to raw data
    X_amp_train_noise_comb = np.append(X_amp_train, X_amp_train_noise, axis=0)
    y_amp_train_noise = np.append(y_amp_train, y_amp_train, axis=0)

    X_amp_train_time = time_shift(X_amp_train, 0.5, X_amp_train.shape[1], 'both')

    # view the difference between raw and noise data
    num = 29
    print(class_dict[y_amp_train[num]])
    plot_amp(X_amp_train[num])
    plot_amp(X_amp_train_time[num])

    # combine both raw, noise, and time data
    X_amp_train_time_comb = np.append(X_amp_train, X_amp_train_time, axis=0)
    X_amp_train_comb = np.append(X_amp_train_noise, X_amp_train_time_comb, axis=0)
    y_amp_train_comb = np.append(y_amp_train_noise, y_amp_train, axis=0)
    print(X_amp_train_comb.shape)