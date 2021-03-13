# SDR_Learning
## TABLE OF CONTENTS
- [1. Steps to Install GNUradio](#1-steps-to-install-GNUradio)
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
- These are the basic Steps to Install GNUradio (v3.7) with PlutoSDR (Windows). More details are in the links.

### 1.1 Get started with GNU radio here 
- Instructions here: https://wiki.gnuradio.org/index.php/PlutoSDR_FMRadio

### 1.2. Learn about GNUradio and AD Pluto SDR drivers 
- Instructions here: https://wiki.gnuradio.org/index.php/PlutoSDR_Source 

### 1.3. Install specific libraries for Pluto 
* Instructions here: https://wiki.analog.com/resources/tools-software/linux-software/gnuradio_windows
#### 1.3.1. Install lib-iio here: https://github.com/analogdevicesinc/libiio 
#### 1.3.2 Install libad9361-iio here: https://github.com/analogdevicesinc/libad9361-iio
  
## GNUradio v3.8  
### NOTE: GNUradio v3.8 requires a new toolbox (gr-iio) and works best in Ubuntu. 
- 1. In order to use the GNUradio 3.8 software, utilize the virtual machine here: : https://github.com/bastibl/instant-gnuradio
- 2. Install PlutoSDR dependencies for GNUradio (gr-iio toolbox https://github.com/analogdevicesinc/gr-iio/tree/upgrade-3.8)

## 2. Use the GNUradio NBFM transceiver flowgraphs
* Download the NBFM_transceiver_Pluto.grc under /GNU3_7/ or /GNU3_8/ depending on your version.
![GNUradio flowgraph for a NBFM transceiver](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/PTT_rev1_grc.png)
- <em align="center"> GNUradio flowgraph for a NBFM transceiver </em>
![GUI to modify parameters in the transceiver flowgraph](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/PTT_rev1.png)
- <em align="center">GUI to modify parameters in the transceiver flowgraph</em>

### 2.1. Download the grc flowgraph 
#### 2.1.1. Download file named "NBFM_transceiver_Pluto.grc"
### 2.2. Link the wav file to the flowgraph. Modify the file source to the wav file.
#### 2.2.1. Download a test *.wav file on this repo under /exampleAudio
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


## 3. Use the GNUradio Pulse Radar flowgraphs
* Download the pulse_radar.grc under /GNU3_8/ (can be easily modified for GNU 3.7)
![GNUradio flowgraph for a Pulsed Radar](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/pulse_radar_grc.png)
- <em align="center"> GNUradio flowgraph for a Pulse Radar tx/rx </em>
![GUI to modify parameters in the radar tx/rx flowgraph](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/pulse_radar_lowPRF.png)
- <em align="center">GUI to modify parameters in the transceiver flowgraph, using a low duty cycle(PRF) </em>
![GUI to modify parameters in the radar tx/rx flowgraph](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/pulse_radar_highPRF.png)
- <em align="center">GUI to modify parameters in the transceiver flowgraph, using a high duty cycle(PRF)</em>


## 4. Use the GNUradio PTT Tone Generator flowgraphs
* Download the PTT_Tone_gen.grc under /GNU3_8/ (can be easily modified for GNU 3.7)
![GNUradio flowgraph for a PTT Tone Generator](https://github.com/SSkySurfer/SDR_Learning/blob/main/images/PTT_tone_gen.png)
* Play a tune/tone on a PTT using the slider bar to change the modulation frequency.

## 5. Resources for Pluto SDRs
* Paper on Pluto Architechture and GNUradio examples: https://peer.asee.org/incorporating-plutosdr-in-the-communication-laboratory-and-classroom-potential-or-pitfall.pdf 
* Official Analog Devices PLUTO SDR links here: https://wiki.analog.com/university/tools/pluto/users 
* 
## 6. Lessons and tutorials for SDR lessons
* Get started with Python here: https://jupyter.org/

* Learn about IQ data: < https://www.ni.com/en-us/innovations/videos/07/i-q-data--plain-and-simple.html#:~:text=I%2FQ%20signals%2C%20or%20I,signals%20in%20the%20time-domain.&text=You%20want%20to%20understand%20more,QAM)%2C%20or%20RF%20upconverters > 
