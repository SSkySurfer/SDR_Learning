# MATLAB files for use with SDRs
## Files:
* PlutoLoopback. (transmits simple modulated data over the Pluto TX to its RX with a loopback cable)
* Project.m (transmits QAM modulation and receives the data to construct an error estimate, look for phase offset, and monitor for phase noise)
* plutoradioWLANTransmitReceiveExample.m (transmits and receives OFDM modulation with either (BPSK, QPSK, 16QAM, or 64QAM).

## Description
* The Pluto loopbck file is the beginning to working with Pluto. It introduces you to the sdr object for rx/tx. 
![TX_RXmatlab](https://www.mathworks.com/help/supportpkg/plutoradio/ref/object_tx_rx_chain.png)

### Loopback.m
'''matlab

    %sdrrx('Pluto', name, value);
    rx = sdrrx('Pluto', name, value);
    rxPluto = sdrrx('Pluto',...
           'RadioID','usb:0',...
           'CenterFrequency',2.5e9,...
           'BasebandSampleRate',1e6);
    %sdrtx('Pluto', name, value);
    tx = sdrtx('Pluto',...
            'RadioID','usb:0',
            'CenterFrequency',2.4e9, ...
            'BasebandSampleRate',1e6,...
            'ChannelMapping',1);
    rx.ShowAdvancedProperties = true;
    tx.ShowAdvancedProperties = true;
    
    >>tx = 
        comm.SDRTxPluto with properties:

    Main
              DeviceName: 'Pluto'
                 RadioID: 'usb:0'
          CenterFrequency: 2.4000e+09
                    Gain: -10
          ChannelMapping: 1
          BasebandSampleRate: 1000000
         
'''

* After a simple loopback script, we can demonstrate the complex waveforms and receive options. Matlab uses the PlutoSDR to transmit/receive complex(I/Q) signals. Therefore, we can use it to perform complex modulations. 

### plutoradioWLANTransmitReceiveExample.m

'''

      % Options
      ctrFreq = 2.432e9;  % Hz, Center freq for tx/rx
      cbw = 'CBW10';       % Choose either 'CBW20', 'CBW10', 'CBW5' for 20, 10, or 5 MHz

      % Choose modulations Where # is described below
      % 0 = 1/2 BPSK
      % 1 = '3/4 BPSK'
      % 2 = '1/2 QPSK'
      % 3 = '3/4 QPSK'
      % 4 = '1/2 16QAM'
      % 5 = '3/4 16QAM'
      % 6 = '2/3 64QAM'
      % 7 = '3/4 64QAM'

      Modulation = 3;
      txgain =-10;
'''

* This sets up the example and allows the user to see different combinations of modulations, frequencies, and gains to transmit an image.
![Baseband](https://github.com/SSkySurfer/SDR_Learning/matlab/images/Baseband_WLAN_signal.png)
![Constel](https://github.com/SSkySurfer/SDR_Learning/matlab/images/WLAN_constellation.png)
![imagesent](https://github.com/SSkySurfer/SDR_Learning/matlab/images/WLAN_image_sent_received.png)

## Dependencies
* Matla R2019b+
* Commmunications Toolbox https://www.mathworks.com/hardware-support/adalm-pluto-radio.html 
* iio tools and drivers for Analog ADALM Pluto.

## Questions?
