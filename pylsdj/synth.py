import json


class SynthSoundParams(object):

    def __init__(self, params):
        self._params = params

    def as_native(self):
        return self._params.as_native()

    def import_lsdinst(self, struct):
        self.volume = struct['volume']
        self.filter_cutoff = struct['filter_cutoff']
        self.phase_amount = struct['phase_amount']
        self.vertical_shift = struct['vertical_shift']

    @property
    def volume(self):
        """the wave's volume"""
        return self._params.volume

    @volume.setter
    def volume(self, value):
        self._params.volume = value

    @property
    def filter_cutoff(self):
        """the filter's cutoff frequency"""
        return self._params.filter_cutoff

    @filter_cutoff.setter
    def filter_cutoff(self, value):
        self._params.filter_cutoff = value

    @property
    def phase_amount(self):
        """the amount of phase shift, ``0`` = no phase,
        ``0x1f`` = maximum phase"""
        return self._params.phase_amount

    @phase_amount.setter
    def phase_amount(self, value):
        self._params.phase_amount = value

    @property
    def vertical_shift(self):
        """the amount to shift the waveform vertically"""
        return self._params.vertical_shift

    @vertical_shift.setter
    def vertical_shift(self, value):
        self._params.vertical_shift = value


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

    @waveform.setter
    def waveform(self, value):
        self._params.waveform = value

    @property
    def filter_type(self):
        '''the type of filter applied to the waveform; one of
        ``"lowpass"``, ``"highpass"``, ``"bandpass"``, ``"allpass"``'''
        return self._params.filter_type

    @filter_type.setter
    def filter_type(self, value):
        self._params.filter_type = value

    @property
    def filter_resonance(self):
        """boosts the signal around the cutoff
        frequency, to change how bright or dull the wave sounds"""
        return self._params.filter_resonance

    @filter_resonance.setter
    def filter_resonance(self, value):
        self._params.filter_resonance = value

    @property
    def distortion(self):
        '''use ``"clip"`` or ``"wrap"`` distortion'''
        return self._params.distortion

    @distortion.setter
    def distortion(self, value):
        self._params.distortion = value

    @property
    def phase_type(self):
        '''compresses the waveform horizontally; one of
        ``"normal"``, ``"resync"``, ``"resync2"``'''
        return self._params.phase_type

    @phase_type.setter
    def phase_type(self, value):
        '''compresses the waveform horizontally; one of
        ``"normal"``, ``"resync"``, ``"resync2"``'''
        self._params.phase_type = value

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

        import_keys = ['start', 'end', 'waveform', 'filter_type',
                       'filter_resonance', 'distortion', 'phase_type']

        for key in import_keys:
            value = synth_data['params'][key]

            if key in ('start', 'end'):
                getattr(self, key).import_lsdinst(value)
            else:
                setattr(self, key, value)

        for i, wave in enumerate(synth_data['waves']):
            for j, frame in enumerate(wave):
                self.waves[i][j] = frame
