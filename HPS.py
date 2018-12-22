import scipy.io.wavfile as wavfile
import scipy.signal
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt

show = True

fs_rate, signal = wavfile.read("train/029_K.wav")  # fs_rate  cxzestotliwosc probkowania
l_audio = len(signal.shape)  # liczba kanałow
print("Channels", l_audio)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2  # usrednianie jezeli stereo
N = signal.shape[0]  # liczba probek
secs = N / float(fs_rate)  # długosc nagrania
Ts = 1.0 / fs_rate  # okres pomiedzy probkami
t = scipy.arange(0, secs, Ts)  # czas odpowiadający próbkom

signal = signal * np.kaiser(N, 30)  # zastosowanie kaisera

FFT = abs(scipy.fft(signal))  # Transformata FFT
FFT[0:3] = 0  # obcięcie dolnych wartosci (pierwszy pik)

FFT2 = FFT  # zastosowanie decimate
for i in range(1, 6):
    FFT3 = scipy.signal.decimate(FFT, i)
    FFT2 = FFT2[range(len(FFT3))] * FFT3
FFT_side = FFT2

freqs = scipy.fftpack.fftfreq(signal.size, t[1] - t[0])  # wartosci czestotliwosci
fft_freqs = np.array(freqs)

pitch = fft_freqs[np.argmax(FFT2)]  # znalezenie dominujacej czestotliwosci ########

if(pitch < 190):
    print("M")
else:
    print("K")

if show:
    freqs_side = freqs[range(len(FFT_side))]  # Wyciecie czestotliwosci do wylresu
    fft_freqs_side = np.array(freqs_side)
    plt.subplot(211)
    p1 = plt.plot(t, signal, "g")  # plotting the signal
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.subplot(212)
    p3 = plt.plot(freqs_side, abs(FFT_side), "b")  # plotting the positive fft spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')
    plt.show()