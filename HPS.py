import scipy.io.wavfile as wavfile
import scipy.signal
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import sys
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

show = False

filename = "a.wav"
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("No file argument")

fs_rate, signal = wavfile.read(filename)  # fs_rate  cxestotliwosc probkowania
l_audio = len(signal.shape)  # liczba kanałow
if l_audio == 2:
    signal = signal.sum(axis=1) / 2  # usrednianie jezeli stereo

signal = signal[int(len(signal) / 20):-int(len(signal) / 20)]  # obciecie poczatku i konca

N = signal.shape[0]  # liczba probek

Ts = 1.0 / fs_rate  # okres pomiedzy probkami

signal = signal * np.kaiser(N, 12)  # zastosowanie kaisera

FFT = abs(scipy.fft(signal))  # Transformata FFT

freqs = scipy.fftpack.fftfreq(signal.size, Ts)  # wartosci czestotliwosci
fft_freqs = np.array(freqs)

min = 0
siec = 0

for i, freq in enumerate(freqs):
    if freq > 35:
        min = i
        break

for i, freq in enumerate(freqs):
    if freq > 50:
        siec = i
        break

FFT[0:min] = 0  # obcięcie dolnych wartosci ponizej 30Hz
for i in range(0, 5):
    FFT[i * siec - 5:i * siec + 5] = 0  # usuniecie 50hz, przydzwiek sieci

FFT2 = FFT  # zastosowanie decimate
for i in range(1, 6):
    FFT3 = scipy.signal.decimate(FFT, i)
    FFT2 = FFT2[range(len(FFT3))] * FFT3
FFT_side = FFT2

pitch = fft_freqs[np.argmax(FFT2)]  # znalezenie dominujacej czestotliwosci

if pitch < 170:
    print("M")
else:
    print("K")

if show:
    secs = N / float(fs_rate)  # długosc nagrania
    t = scipy.arange(0, secs, Ts)  # czas odpowiadający próbkom
    freqs_side = freqs[range(min * 10)]  # Wyciecie czestotliwosci do wylresu
    fft_freqs_side = np.array(freqs_side)
    # p1 = plt.plot(t, signal, "g")  # plotting the signal
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.subplot(212)
    plt.plot(freqs_side, abs(FFT_side[range(min * 10)]), "b")
    plt.xlabel(filename)
    plt.ylabel('Count single-sided')
    plt.show()
