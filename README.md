# SDR_Learning

## 1. Steps to Install GNUradio (v3.7) with PlutoSDR (Windows):
### 1.1 Get started with GNU radio here: https://wiki.gnuradio.org/index.php/PlutoSDR_FMRadio

### 1.2. Learn about GNUradio and AD Pluto SDR drivers. https://wiki.gnuradio.org/index.php/PlutoSDR_Source 

### 1.3. Install specific libraries for Pluto (https://wiki.analog.com/resources/tools-software/linux-software/gnuradio_windows):
 1.3.1. Install lib-iio here: https://github.com/analogdevicesinc/libiio 
 1.3.2 Install libad9361-iio here: https://github.com/analogdevicesinc/libad9361-iio
  
  *Note, process may not be stable with GNUradio v3.8
## 2. Use the GNUradio NBFM transceiver flowgraph on this page
![plot](https://github.com/SSkySurfer/SDR_Learning/blob/main/NBFM_gui.png)
### 2.1. Download the grc flowgraph named "NBFM_transceiver_Pluto.grc"
### 2.2. Link the wav file to the flowgraph. Modify the file source to the wav file.
 2.2.1. Download a test *.wav file on this repo.
 2.2.2. Alternatively, use your own *wav. 
### 2.3. If using the voice transmit feature of the flowgraph, link your computer's microphone to the flowgraph, by modifying the "Audio Source" block, and changing the "Device_Name" to your computer's microphone name with "quotes" (e.g. "Internal Microphone (Realtek Device)")
### 2.4. Modify the "Audio Sink" with your Speakers' Device_Name.
### 2.5. Plugin your PlutoSDR, if not already plugged in.
### 2.6. Start the flowgraph and talk into a radio on 141.050MHz (default receive frequency). Listen to the playback on your computer audio. Or stop, enable the wave file sink, modify the file storage location, start the flowgraph again.
### 2.7. Change the GUI's TX/RX selector to TX. (This amplifies the TX gain, and lowers the RX gain)
### 2.8. Try the wav file
 2.8.1 Tune your handheld radio to 136.050MHz
 2.8.2. Playback the wav file on your pc. Listen to the audio in your radio.
### 2.9. Try the computer microphone
 2.9.1. Stop, enable the "Audio Source" (i.e. microphone), disable the "Wav File Source" start
 2.9.2. Start the flowgraph and talk into the mic. Listen to the voice on your handheld radio (or another SDR)
### 2.10. Modify the slider bars as required for other transmitters.

### Resources for Pluto SDRs
 - Paper on Pluto Architechture and GNUradio examples: https://peer.asee.org/incorporating-plutosdr-in-the-communication-laboratory-and-classroom-potential-or-pitfall.pdf 
 - Official Analog Devices PLUTO SDR links here: https://wiki.analog.com/university/tools/pluto/users 

## Lessons and tutorials for SDR lessons
 - Get started with Python here: https://jupyter.org/

 - Learn about IQ data: < https://www.ni.com/en-us/innovations/videos/07/i-q-data--plain-and-simple.html#:~:text=I%2FQ%20signals%2C%20or%20I,signals%20in%20the%20time-domain.&text=You%20want%20to%20understand%20more,QAM)%2C%20or%20RF%20upconverters > 
