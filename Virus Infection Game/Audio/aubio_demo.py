#modified from https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
#modifed by Tara Stentz (tstentz)
import aubio

def detect(filename):
        downsample = 8
        samplerate = 44100 // downsample
        win_s = 4096 // downsample # fft size
        hop_s = 512  // downsample # hop size
        s = aubio.source(filename, samplerate, hop_s)
        samplerate = s.samplerate
        tolerance = 0.8
        pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
        pitch_o.set_unit("freq")
        pitch_o.set_tolerance(tolerance)
        pitches = []
        confidences = []
        # total number of frames read
        total_frames = 0
        counter = 0
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            confidence = pitch_o.get_confidence()
            print("timestamp = %0.2f, pitch = %0.1f, confidence = %0.3f" 
                % (total_frames / float(samplerate), pitch, confidence))
            pitches += [pitch]
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break
        return pitches