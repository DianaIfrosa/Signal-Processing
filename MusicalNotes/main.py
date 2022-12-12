# Ifrosă Diana-Maria - 351
# Ionescu Ioan - 351

import numpy as np
import sounddevice as sd

LENGTH_NOTE = 2  # seconds
BASE_FREQ = 440  # A4 frequency
AMPLITUDE = 10000
PHASE = 0

SAMPLING_RATE = 44100
SAMPLING_PERIOD = 1. / SAMPLING_RATE  # seconds

sd.default.samplerate = SAMPLING_RATE

PITCHES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def sine(amplitude, frequency, time, phase):
    return amplitude * np.sin(2 * np.pi * frequency * time + phase)


def note_to_frequency(name):
    if name == 'R':  # rest
        return 0

    octave = int(name[-1])
    pitch = PITCHES.index(name[:-1])

    # In order to find the frequency of a specific note, we take the frequency of note A4 (which is considered base)
    # and we multiply it with 2 at the power of the 'distance' between the given note and A4 (pitch 9, octave 4)
    # divided by 12:
    return BASE_FREQ * 2 ** ((octave - 4) + (pitch - 9) / 12.)


def get_wave(note, duration=2):
    if duration < 0:  # dotted note
        duration = LENGTH_NOTE * (1 / -duration + 1 / (2 * -duration))
    else:
        duration = LENGTH_NOTE * (1 / duration)
    n_samples = duration / SAMPLING_PERIOD
    freq = note_to_frequency(note)
    time = np.linspace(0, duration, int(n_samples + 1))
    wave = sine(AMPLITUDE, freq, time, PHASE)
    return wave


def create_song(notes):
    return np.concatenate([get_wave(name, int(duration)) for (name, duration) in notes])


def play_song(song):
    wav_wave = np.array(song, dtype=np.int16)
    sd.play(wav_wave, blocking=True)
    sd.stop()


def read_song(file_path):
    data = np.genfromtxt(file_path, dtype=[('note', 'S8'), ('duration', int)], delimiter=", ", comments='//')
    notes = []
    for (note, duration) in data:
        note = note.decode()
        if note == 'REST':  # transform 'REST' to 'R'
            note = note[:1]
        else:  # ignore the 'NOTE_' part
            note = note[5:]

        notes.append((note, duration))

    return create_song(np.array(notes))


def ex1():
    octave = [('C4', 2), ('D4', 2), ('E4', 2),  ('F4', 2), ('G4', 2),  ('A4', 2), ('B4', 2), ('C5', 2)]

    song = create_song(octave)
    play_song(song)


def ex2():
    # Wiegenlied (Brahms' Lullaby), inspired by
    # https://github.com/robsoncouto/arduino-songs/blob/master/brahmslullaby/brahmslullaby.ino

    tones = [('G4', 4), ('G4', 4), ('A#4', -4), ('G4', 8), ('G4', 4),
             ('A#4', 4), ('R', 4), ('G4', 8), ('A#4', 8), ('D#5', 4),
             ('D5', -4), ('C5', 8), ('C5', 4), ('A#4', 4), ('F4', 8),
             ('G4', 8), ('G#4', 4), ('F4', 4), ('F4', 8), ('G4', 8,),
             ('G#4', 4), ('R', 4), ('F4', 8), ('G#4', 8,), ('D5', 8,),
             ('C5', 8), ('A#4', 4), ('D5', 4,), ('D#5', 4), ('R', 4),
             ('D#4', 8), ('D#4', 8), ('D#5', 2), ('C5', 8), ('G#4', 8),
             ('A#4', 2), ('G4', 8), ('D#4', 8), ('G#4', 4), ('A#4', 4),
             ('C5', 4), ('A#4', 2), ('D#4', 8), ('D#4', 8), ('D#5', 2),
             ('C5', 8), ('G#4', 8), ('A#4', 2), ('G4', 8), ('D#4', 8),
             ('A#4', 4), ('G4', 4), ('D#4', 4), ('D#4', 2)]

    song = create_song(tones)
    play_song(song)


def ex3():
    # Fur Elise, inspired by
    # https://github.com/robsoncouto/arduino-songs/blob/master/furelise/furelise.ino

    song = read_song("musicScore.txt")
    play_song(song)


if __name__ == '__main__':
    ex1()
    ex2()
    ex3()