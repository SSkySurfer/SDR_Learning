# SDR_Learning
## TABLE OF CONTENTS
- [1. Steps to Install GNUradio] (#1-steps-to-install-gnuradio)
  * [1.1 Get started with GNU radio here](#11-get-started-with-gnu-radio-here)

  * [1.2. Learn about GNUradio and AD Pluto SDR drivers](#12-learn-about-gnuradio-and-ad-pluto-sdr-drivers)

  * [1.3. Install specific libraries for Pluto](#13-install-specific-libraries-for-pluto)

- [2. Use the GNUradio NBFM transceiver flowgraph on this page](#2-use-the-gnuradio-nbfm-transceiver-flowgraph-on-this-page)
  * [2.1. Download the grc flowgraph named](#21-download-the-grc-flowgraph)
  * [2.2. Link the wav file to the flowgraph. Modify the file source to the wav file.](#22-link-the-wav-file-to-the-flowgraph-modify-the-file-source-to-the-wav-file)
  * [2.3. If using the voice transmit feature of the flowgraph](#23-if-using-the-voice-transmit-feature-of-the-flowgraph)
  * [2.4. Modify the Audio Sink](#24-modify-the-audio-sink)
  * [2.5. Plugin your PlutoSDR](#25-plugin-your-plutosdr)
  * [2.6. Start the flowgraph and talk](#26-start-the-flowgraph-and-talk)
  * [2.7. Change the GUI's TX/RX selector to TX](#27-change-the-gui-s-tx-rx-selector-to-tx)
  * [2.8. Try the wav file](#28-try-the-wav-file)

  * [2.9. Try the computer microphone](#29-try-the-computer-microphone)
  * [2.10. Modify the slider bars as required for other transmitters.](#210-modify-the-slider-bars-as-required-for-other-transmitters)
- [3. Resources for Pluto SDRs](#3-resources-for-pluto-sdrs)

## 1. Steps to Install GNUradio 
* Steps to Install GNUradio (v3.7) with PlutoSDR (Windows)
## Table of Contents

### 1.1 Get started with GNU radio here 
* - https://wiki.gnuradio.org/index.php/PlutoSDR_FMRadio

### 1.2. Learn about GNUradio and AD Pluto SDR drivers 
* - https://wiki.gnuradio.org/index.php/PlutoSDR_Source 

### 1.3. Install specific libraries for Pluto 
* https://wiki.analog.com/resources/tools-software/linux-software/gnuradio_windows:
#### 1.3.1. Install lib-iio here: https://github.com/analogdevicesinc/libiio 
#### 1.3.2 Install libad9361-iio here: https://github.com/analogdevicesinc/libad9361-iio
  
*  *Note, process may not be stable with GNUradio v3.8
## 2. Use the GNUradio NBFM transceiver flowgraph on this page
![GNUradio flowgraph for a NBFM transceiver](https://github.com/SSkySurfer/SDR_Learning/blob/main/NBFM_transceiver_Pluto_grc.png)
<em align="center"> GNUradio flowgraph for a NBFM transceive </em>
![GUI to modify parameters in the transceiver flowgraph](https://github.com/SSkySurfer/SDR_Learning/blob/main/NBFM_gui.png)
<em align="center">GUI to modify parameters in the transceiver flowgraph</em>

### 2.1. Download the grc flowgraph 
#### 2.1.1. Download file named "NBFM_transceiver_Pluto.grc"
### 2.2. Link the wav file to the flowgraph. Modify the file source to the wav file.
#### 2.2.1. Download a test *.wav file on this repo.
#### 2.2.2. Alternatively, use your own *wav. 
### 2.3. If using the voice transmit feature of the flowgraph
#### 2.3.1. Link your computer's microphone to the flowgraph, by modifying the "Audio Source" block, and changing the "Device_Name". First, find to your computer's microphone name (e.g. Internal Microphone (Realtek Device)).
#### 2.3.2. Replace the Device "Internal Microphone (Conexant SmartAudio HD)" with your Computer's Device_Name with "quotes" (e.g. "Internal Microphone (Realtek Device)")
### 2.4. Modify the Audio Sink
#### 2.4.1. Replace the Device "Speakers (Conexant SmartAudio HD)" with your Speakers' Device_Name
### 2.5. Plugin your PlutoSDR
 * Assuming not already plugged in (If ever encountnering errors, replugin the device)
### 2.6. Start the flowgraph and talk
#### 2.6.1. Start flowgraph and talk into a radio on 141.050MHz (default receive frequency).
#### 2.6.2. Listen to the playback on your computer audio. 
#### 2.6.3. Or stop, enable the wave file sink, modify the file storage location, start the flowgraph again
### 2.7. Change the GUI's TX/RX selector to TX 
#### 2.7.1. This amplifies the TX gain, and lowers the RX gain
### 2.8. Try the wav file
#### 2.8.1 Tune your handheld radio to 136.050MHz
#### 2.8.2. Playback the wav file on your pc. Listen to the audio in your radio.
### 2.9. Try the computer microphone
#### 2.9.1. Stop, enable the "Audio Source" (i.e. microphone), disable the "Wav File Source" start
#### 2.9.2. Start the flowgraph and talk into the mic. Listen to the voice on your handheld radio (or another SDR)
### 2.10. Modify the slider bars as required for other transmitters.

### 3. Resources for Pluto SDRs
* Paper on Pluto Architechture and GNUradio examples: https://peer.asee.org/incorporating-plutosdr-in-the-communication-laboratory-and-classroom-potential-or-pitfall.pdf 
* Official Analog Devices PLUTO SDR links here: https://wiki.analog.com/university/tools/pluto/users 

## 4. Lessons and tutorials for SDR lessons
* Get started with Python here: https://jupyter.org/

* Learn about IQ data: < https://www.ni.com/en-us/innovations/videos/07/i-q-data--plain-and-simple.html#:~:text=I%2FQ%20signals%2C%20or%20I,signals%20in%20the%20time-domain.&text=You%20want%20to%20understand%20more,QAM)%2C%20or%20RF%20upconverters > 
