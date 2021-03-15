"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from random import seed
from random import random
from gnuradio import gr
from scipy import signal
from scipy.signal import find_peaks, peak_prominences
import logging, sys

#waveform = np.uint32
#samp_rate = np.uint32
#ctr_freq = np.uint32
#num_tones = np.uint32
#freq_spacing = np.uint32

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, waveform=0, samp_rate=10000000, ctr_freq=0, num_tones=3, freq_spacing=1000000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.waveform = waveform
        self.samp_rate = samp_rate
        self.ctr_freq=ctr_freq
        self.num_tones=num_tones
        self.freq_spacing = freq_spacing
        

    	    
    def work(self, input_items, output_items):

        def signaltonoise(s, axis=0, ddof=0): 
         a=np.asanyarray(s)
         m=a.mean(axis)
         sd=a.std(axis=axis, ddof=ddof)
         
        # implement random seed for phase offset
        seed(1)
        num_samples=np.uint32
        num_samples= input_items[0].size
        #logging.debug(print(num_samples))
	
	#Create start and stop frequency
        if self.num_tones > 1:
        	spread     =  self.freq_spacing*self.num_tones
        	start_freq =  0 - spread/2
        	end_freq   =  0 + spread/2
        	ctr_freqs  =  np.linspace(start_freq, end_freq,self.num_tones)
        else:
        	ctr_freqs  = (self.ctr_freq, self.ctr_freq)
       
        # Create empty vectors	
        temp_data = np.zeros((1,num_samples),dtype=np.complex64)
        data_new = np.zeros((1,num_samples),dtype=np.complex64)
        mt = np.zeros((1,num_samples),dtype=np.complex64)
   	# Create time vector
        t = np.linspace(0,num_samples/self.samp_rate,num_samples)
        
        # Add the waveforms at spaced frequencies to make a multitone
        for n in range(len(ctr_freqs)):
        	if   self.waveform == 0:
        		data_new = signal.square(2*np.pi*(ctr_freqs[n]+self.ctr_freq)*t*random()) 
        	elif self.waveform == 1:
        		data_new = signal.sawtooth(2 * np.pi * ctr_freqs[n] * t )
        	else:
        		data_new = np.sin(2 * np.pi * ctr_freqs[n] * t )
        	 
        	temp_data = temp_data + data_new
        	#signal.chirp(t, start_freq, num_samples/self.samp_rate, end_freq, method='linear')
        	
        	
        mt = np.divide(temp_data[0:2],np.ndarray.max(abs(temp_data[0:2])))	
        output_items[0][:] = temp_data[0:2]
        #print (mt[0:2][0])
        return len(output_items[0])
