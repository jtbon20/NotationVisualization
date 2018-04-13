import sys
from aubio import source, pitch
from audio_util import *
from plot import *
import numpy as np

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 16
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

hop_s = 512  // downsample # hop size
length = get_length_sec(filename,samplerate,hop_s);
win_s = 4096 // downsample # fft size

#instantiate the aubio object
s = source(filename, samplerate, hop_s)

tolerance = 0.7
pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

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
    if read < hop_s: break


skip = 1
pitches = np.array(pitches[skip:])
confidences = np.array(confidences[skip:])
times = [t * hop_s for t in range(len(pitches))]

dta = filter_array(pitches, confidences, tolerance)
x = filter_array_on_other(times, pitches, confidences, tolerance)

visualize(x, dta, None, filename)
