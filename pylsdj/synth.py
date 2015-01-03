import json

class SynthSoundParams(object):
    def __init__(self, params):
        self._params = params

    @property
    def volume(self):
        """the wave's volume"""
        return self._params.volume

    @property
    def filter_cutoff(self):
        """the filter's cutoff frequency"""
        return self._params.filter_cutoff

    @property
    def phase_amount(self):
        """the amount of phase shift, ``0`` = no phase,
        ``0x1f`` = maximum phase"""
        return self._params.phase_amount

    @property
    def vertical_shift(self):
        """the amount to shift the waveform vertically"""
        return self._params.vertical_shift


class Synth(object):
    def __init__(self, song, index):
        self._song = song
        self._index = index

        self._params = self._song.song_data.softsynth_params[index]

        self._start = SynthSoundParams(
            self._song.song_data.softsynth_params[index].start)
        self._end = SynthSoundParams(
            self._song.song_data.softsynth_params[index].end)

    @property
    def song(self):
        """the synth's parent Song"""
        return self._song

    @property
    def index(self):
        """the synth's index within its parent song's synth table"""
        return self._index

    @property
    def start(self):
        """parameters for the start of the sound, represented as a
        SynthSoundParams object"""
        return self._start

    @property
    def end(self):
        """parameters for the end of the sound, represented as a
        SynthSoundParams object"""
        return self._end

    @property
    def waveform(self):
        '''the synth\'s waveform type; one of ``"sawtooth"``,
        ``"square"``, ``"sine"``'''
        return self._params.waveform

    @property
    def filter_type(self):
        '''the type of filter applied to the waveform; one of
        ``"lowpass"``, ``"highpass"``, ``"bandpass"``, ``"allpass"``'''
        return self._params.filter_type

    @property
    def filter_resonance(self):
        """boosts the signal around the cutoff
        frequency, to change how bright or dull the wave sounds"""
        return self._params.filter_resonance

    @property
    def distortion(self):
        '''use ``"clip"`` or ``"wrap"`` distortion'''
        return self._params.distortion

    @property
    def phase_type(self):
        '''compresses the waveform horizontally; one of
        ``"normal"``, ``"resync"``, ``"resync2"``'''
        return self._params.phase_type

    @property
    def waves(self):
        """a list of the synth's waveforms, each of which is a list of bytes"""
        return self.song.song_data.wave_frames[self.index]

    def export(self):
        export_struct = {}

        export_struct["params"] = json.loads(self._params.as_json())
        export_struct["waves"] = []

        for wave in self.waves:
            export_struct["waves"].append(list(wave))

        return export_struct

    def import_lsdinst(self, synth_data):
        params_native = self._params.as_native()

        for key in params_native:
            if key[0] == '_':
                continue

            if key in ('start', 'end'):
                self._import_sound_params(
                    synth_data['params'][key], getattr(self, key))
            else:
                setattr(self._params, key, synth_data['params'][key])

        for i, wave in enumerate(synth_data['waves']):
            for j, frame in enumerate(wave):
                self.waves[i][j] = frame

    def _import_sound_params(self, params, dest):
        native_repr = dest.as_native()

        for key in native_repr:
            if key[0] == '_':
                continue

            setattr(dest, key, params[key])
