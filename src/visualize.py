import sys
from aubio import source, pitch, pvoc, filterbank
from audio_util import *
from plot import *
from numpy import vstack, zeros
import numpy as np

#Arguments
if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

#Constants
filename = sys.argv[1]
downsample = 16
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])
hop_s = 512  // downsample # hop size
length = get_length_sec(filename,samplerate,hop_s);
win_s = 4096 // downsample # fft size
tolerance = 0.7

#Get the audio object
s = source(filename, samplerate, hop_s)

#Initalize pitch tracking
pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

#Setup energy tracking
pv = pvoc(win_s, hop_s)
f = filterbank(40, win_s)
f.set_mel_coeffs_slaney(samplerate)


#Set up arrays to store processed data
energies = []
pitches = []
times = []
confidences = []

# total number of frames read
total_frames = 0
while True:
    #Sample and determine pitch with confidences
    samples, read = s()
    pitch = pitch_o(samples)[0]
    confidence = pitch_o.get_confidence()

    #save resulting data
    pitches += [pitch]
    times += [total_frames]
    confidences += [confidence]
    total_frames += read

    fftgrain = pv(samples)
    new_energies = f(fftgrain)
    energies+=[np.sum(new_energies)]

    if read < hop_s: break


#Process data
skip = 1
pitches = np.array(pitches[skip:])
energies = np.array(energies[skip:])
confidences = np.array(confidences[skip:])
times = [t * hop_s for t in range(len(pitches))]


# Filter the data
dta = filter_array(pitches, confidences, tolerance)
x = filter_array_on_other(times, pitches, confidences, tolerance)
s = filter_array_on_other(energies, pitches, confidences, tolerance)

#Print the result
visualize(x, dta, s, filename)
