import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    y = filtfilt(b, a, data)
    return y

 def highpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high')
    y = filtfilt(b, a, data)
    return y

# Example usage:
if __name__ == "__main__":
    # Generate a sample signal: 1 second, 1000 Hz sample rate
    fs = 1000.0
    t = np.linspace(0, 1.0, int(fs), endpoint=False)
    # Signal with 50 Hz and 200 Hz components
    data = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*200*t)

    # Apply bandpass filter: keep 40-100 Hz
    filtered_band = bandpass_filter(data, lowcut=40, highcut=100, fs=fs, order=4)

    # Apply lowpass filter: keep below 100 Hz
    filtered_low = lowpass_filter(data, cutoff=100, fs=fs, order=4)

    # Apply highpass filter: keep above 100 Hz
    filtered_high = highpass_filter(data, cutoff=100, fs=fs, order=4)

    # Plot original and filtered signals
    plt.figure(figsize=(12, 10))
    plt.subplot(4, 1, 1)
    plt.plot(t, data, label='Original Signal')
    plt.legend()
    plt.subplot(4, 1, 2)
    plt.plot(t, filtered_band, label='Band-pass (40-100 Hz)', color='orange')
    plt.legend()
    plt.subplot(4, 1, 3)
    plt.plot(t, filtered_low, label='Low-pass (<100 Hz)', color='green')
    plt.legend()
    plt.subplot(4, 1, 4)
    plt.plot(t, filtered_high, label='High-pass (>100 Hz)', color='red')
    plt.legend()
    plt.xlabel('Time [s]')
    plt.tight_layout()
    plt.show()