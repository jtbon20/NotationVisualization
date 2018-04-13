import sys
from aubio import source, pitch
from audio_util import get_length_sec
from plot import *

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 64
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

hop_s = 512  // downsample # hop size
length = get_length_sec(filename,samplerate,hop_s);
win_s = 4096 // downsample # fft size

#instantiate the aubio object
s = source(filename, samplerate, hop_s)

tolerance = 0.8
pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
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

import os.path
from numpy import array, ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from demo_waveform_plot import get_waveform_plot, set_xlabels_sample2time

skip = 1
pitches = array(pitches[skip:])
confidences = array(confidences[skip:])
times = [t * hop_s for t in range(len(pitches))]

fig = plt.figure(figsize=(160, 20), dpi=400)
plt.plot(times, confidences, '-')
plt.axis('off')

#ax1 = fig.add_subplot(311)
#ax1 = get_waveform_plot(filename, samplerate = samplerate, block_size = hop_s, ax = ax1)
#plt.setp(ax1.get_xticklabels(), visible = False)
#ax1.set_xlabel('')

#plt.savefig(os.path.basename(filename) + '.svg')
plt.savefig(os.path.basename(filename) + '.svg')
plt.close();
