import numpy as np


def remove_dc(data):

    freq_signal = np.fft.fft(data)

    freq_signal[0] = 0  # remove dc component

    removed_dc = np.fft.ifft(freq_signal)

    modified_signal = np.real(removed_dc)

    return modified_signal