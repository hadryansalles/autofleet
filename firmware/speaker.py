import sounddevice as sd
import numpy as np

def play(duration):
    frequency = 880
    # Generate the time axis for the beep sound
    t = np.linspace(0, duration, int(duration * 44100), False)

    # Generate the beep sound waveform
    beep_waveform = np.sin(frequency * 2 * np.pi * t)

    # Play the beep sound
    sd.play(beep_waveform, 44100, blocksize=2048)
    sd.wait()