from copy import deepcopy

import numpy as np
import pywt
from scipy.signal import hilbert
from scipy.integrate import cumtrapz

from kswutils_signal.frequency_analysis import FrequencyAnalysis as FA


def removedc_minus_mean(data):
    return data - np.mean(data)


def removedc_fft_ifft(data):

    freq_signal = np.fft.fft(data)

    freq_signal[0] = 0  # remove dc component

    removed_dc = np.fft.ifft(freq_signal)

    modified_signal = np.real(removed_dc)

    return modified_signal


def denoise_signal_wavelet_transform(signal):
    # Perform wavelet transform
    coeffs = pywt.wavedec(signal, "db1", level=4)

    # Apply thresholding to the detail coefficients
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    threshold = sigma * np.sqrt(2 * np.log(len(signal)))

    denoised_coeffs = coeffs[:]
    denoised_coeffs[1:] = (
        pywt.threshold(c, value=threshold, mode="soft") for c in denoised_coeffs[1:]
    )

    # Reconstruct the signal
    denoised_signal = pywt.waverec(denoised_coeffs, "db1")
    return denoised_signal


def integrate_to_velocity(acceleration, sampling_rate):

    data = deepcopy(acceleration)

    # == De-noising == #

    data_denoised = denoise_signal_wavelet_transform(data)

    # == Filtering == #

    data_filtered = FA.bandpass_filter(data_denoised, 10, 600, sampling_rate, order=3)

    # data0 = data_filtered - np.mean(data_filtered)
    # data0 = remove_dc(data)

    n = len(data_filtered)
    d = n / sampling_rate

    time = np.linspace(0, d, num=n)

    # velocity = np.cumsum(acceleration) * (time[1] - time[0])
    velocity = cumtrapz(data_filtered, time, initial=0)

    # velocity0 = velocity - np.mean(velocity)

    velocity *= 9.81e3

    return velocity

    # velocity0 = fft_ifft(velocity)
    # return velocity0


def calculate_envelope_hilbert_transform(signal):

    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)

    return amplitude_envelope
