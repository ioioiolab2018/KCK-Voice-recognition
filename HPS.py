import sys

import scipy.io.wavfile as wavfile
import scipy.signal
import scipy.fftpack
import numpy as np


def run(filename):
    fs_rate, signal = wavfile.read(filename)  # fs_rate - częstotliwość próbkowania
    l_audio = len(signal.shape)  # liczba kanałów

    if l_audio == 2:
        signal = signal.sum(axis=1) / 2  # uśrednianie jeżeli stereo

    N = signal.shape[0]  # liczba próbek
    secs = N / float(fs_rate)  # długość nagrania
    Ts = 1.0 / fs_rate  # okres pomiędzy próbkami
    t = scipy.arange(0, secs, Ts)  # czas odpowiadający próbkom

    signal = signal * np.kaiser(N, 10)  # zastosowanie kaisera

    FFT = abs(scipy.fft(signal))  # Transformata FFT
    FFT[0:100] = 0  # obcięcie dolnych wartosci (pierwszy pik)

    FFT2 = FFT  # zastosowanie decimate
    for i in range(1, 6):
        FFT3 = scipy.signal.decimate(FFT, i)
        FFT2 = FFT2[range(len(FFT3))] * FFT3
    FFT_side = FFT2

    freqs = scipy.fftpack.fftfreq(signal.size, t[1] - t[0])  # wartosci czestotliwosci
    fft_freqs = np.array(freqs)

    pitch = fft_freqs[np.argmax(FFT2)]  # znalezenie dominujacej czestotliwosci ########

    if pitch < 190:
        print("M")
    else:
        print("K")


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            run(sys.argv[1])
    except:
        print("error")
