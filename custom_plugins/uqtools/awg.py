import logging
import os
from . import Measurement

class ProgramAWG(Measurement):
    '''
    Program AWG sequences, storing the generated sequences 
    in the data directory of the measurement.
    '''
    def __init__(self, sequence, awgs, **kwargs):
        '''
        Input:
            sequence - populated sequence object
            awgs - list of AWG instruments the sequence is distributed to
        '''
        super(ProgramAWG, self).__init__(data_directory='patterns', **kwargs)
        self._sequence = sequence
        self._awgs = awgs
    
    def _measure(self, wait=True):
        '''
        upload sequence to the AWGs
        '''
        host_dir = self.get_data_directory()
        host_file = self._name
        
        self._sequence.sample()
        self._sequence.export(host_dir, host_file)
        for idx, awg in enumerate(self._awgs):
            #awg.clear_waveforms()
            host_fullpath = os.path.join(host_dir, 'AWG_{0:0=2d}'.format(idx), host_file+'.seq')
            if os.path.exists(host_fullpath):
                awg.load_host_sequence(host_fullpath)
            else:
                logging.warning(__name__ + ': no sequence file found for AWG #{0}.'.format(idx))
        if wait:
            # wait for all AWGs to finish loading
            for idx, awg in enumerate(self._awgs):
                awg.wait()
                if awg.get_seq_length() != len(self._sequence):
                    logging.error(__name__ + ': sequence length reported by AWG #{0} differs from the expected value {1}.'.format(idx, len(self._sequence)))

    def plot(self):
        self._sequence.sample()
        from custom_lib.pulsegen import ptplot_gui
        ptplot_gui.plot(self._seqence, [0,1,2,3], [0,1], 0)