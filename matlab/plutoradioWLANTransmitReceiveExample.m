close all
clear

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


%% Image Transmission and Reception Using WLAN Toolbox and One PlutoSDR 
% This example shows how to transmit and receive WLAN packets on a single
% PlutoSDR device, using the Communications Toolbox(TM) Support Package for
% ADALM-PLUTO Radio and the WLAN Toolbox(TM).  An image file is encoded and
% packed into WLAN packets for transmission, and subsequently decoded on
% reception.

% Copyright 2017-2018 The MathWorks, Inc.

%% Required Hardware and Software
% To run this example, you need the following software:
%
% * <matlab:web(['https://www.mathworks.com/products/communications/'],'-browser') Communications Toolbox(TM)>
%
% You also need the following SDR device and the corresponding support
% package Add-On:
%
% * ADALM-PLUTO radio and the corresponding software
% <matlab:web(['https://www.mathworks.com/hardware-support/adalm-pluto-radio.html'],'-browser')
% Communications Toolbox Support Package for ADALM-PLUTO Radio>
%
%
% For a full list of Communications Toolbox supported SDR platforms,
% refer to Supported Hardware section of
% <matlab:web(['https://www.mathworks.com/discovery/sdr.html'],'-browser')
% Software Defined Radio (SDR) discovery page>.

%% Introduction
% You can use WLAN Toolbox to generate standard-compliant MAC frames and
% waveforms. These baseband waveforms can be upconverted for RF
% transmission using SDR hardware such as PlutoSDR. The PlutoSDR
% <matlab:plutoradiodoc('sdrpluto_repeatedwaveformtx') Repeated Waveform
% Transmitter> functionality allows a waveform to be transmitted over the
% air and is received using the same SDR hardware. The received waveform is
% captured and downsampled to baseband using a PlutoSDR and is decoded to
% recover the transmitted information as shown in the following figure.
%
% <<SDRWLAN80211aTransceiver_published.png>>
%
% This example imports and segments an image file into multiple MAC service
% data units (MSDUs). Each MSDU is passed to the
% <matlab:doc('wlanMACFrame') wlanMACFrame> function to create a MAC
% protocol data unit (MPDU). This function also consumes
% <matlab:doc('wlanMACFrameConfig') wlanMACFrameConfig> object as an input,
% which can be used to sequentially number the MPDUs through the
% |SequenceNumber| property. The MPDUs are passed to the PHY layer as PHY
% Layer Service Data Units (PSDUs). Each PSDU data is packed into a single
% NonHT, 802.11a(TM) [ <#24 1> ] WLAN packet using WLAN Toolbox. This
% example creates a WLAN baseband waveform using the
% <matlab:doc('wlanWaveformGenerator') wlanWaveformGenerator> function.
% This function consumes multiple PSDUs and processes each to form a series
% of PLCP Protocol Data Units (PPDUs). The multiple PPDUs are upconverted
% and the RF waveform is sent over the air using PlutoSDR as shown in the
% following figure.
%
% <<plutoradioWLANTransmitReceiveExampleTransmit.png>>
%
% This example then captures the transmitted waveform using the same
% PlutoSDR.  The RF transmission is demodulated to baseband and the
% received MPDUs are decoded using the <matlab:doc('wlanMPDUDecode')
% wlanMPDUDecode> function. The extracted MSDUs are ordered using the
% |SequenceNumber| property in the recovered MAC frame configuration
% object. The information bits in the multiple received MSDUs are combined
% to recover the transmitted image. The receiver processing is illustrated
% in the following diagram.
%
% <<plutoradioWLANTransmitReceiveExampleReceive.png>>

%% Example Setup
% Before you run this example, perform the following steps:
%
% # Configure your host computer to work with the Support Package for
% ADALM-PLUTO Radio. See <matlab:plutoradiodoc('sdrpluto_spsetup') Getting
% Started> for help.
% # Make sure that WLAN Toolbox is installed. You must have a WLAN
% Toolbox license to run this example.
%
% When you run this example, the first thing the script does is to check
% for WLAN Toolbox.

% Check that WLAN Toolbox is installed, and that there is a valid
% license
if isempty(ver('wlan')) % Check for WLAN Toolbox install
    error('Please install WLAN Toolbox to run this example.');
elseif ~license('test', 'WLAN_System_Toolbox') % Check that a valid license is present
    error( ...
        'A valid license for WLAN Toolbox is required to run this example.');
end
 
%%
% The script then configures all the scopes and figures that will be
% displayed throughout the example.

% Setup handle for image plot
if ~exist('imFig', 'var') || ~ishandle(imFig)
    imFig = figure;
    imFig.NumberTitle = 'off';
    imFig.Name = 'Image Plot';
    imFig.Visible = 'off';
else   
    clf(imFig); % Clear figure
    imFig.Visible = 'off';
end

% Setup Spectrum viewer
spectrumScope = dsp.SpectrumAnalyzer( ...
    'SpectrumType', 'Power density', ...
    'SpectralAverages', 10, ...
    'YLimits', [-130 -50], ...
    'Title', 'Received Baseband WLAN Signal Spectrum', ...
    'YLabel', 'Power spectral density', ...
    'Position', [69 376 800 450]);

% Setup the constellation diagram viewer for equalized WLAN symbols
constellation = comm.ConstellationDiagram(...
    'Title', 'Equalized WLAN Symbols', ...
    'ShowReferenceConstellation', false, ...
    'Position', [878 376 460 460]);
                            
%%
% An <matlab:plutoradiodoc('commsdrtxpluto') SDR Transmitter> System object
% is used with the PlutoSDR to transmit baseband data to the SDR hardware.
%

%  Initialize SDR device
deviceNameSDR = 'Pluto'; % Set SDR Device
rx = sdrdev(deviceNameSDR);           % Create SDR device object 

%%
% The following sections explain the design and architecture of this
% example, and what you can expect to see as the code is executed.

%% Transmitter Design
% The general structure of the WLAN transmitter can be described as follows:
%
% # Import an image file and convert it to a stream of decimal bytes.
% # Generate a baseband WLAN signal using WLAN Toolbox, pack the data
% stream into multiple 802.11a packets.
% # Prepare the baseband signal for transmission using the SDR hardware.
% # Send the baseband data to the SDR hardware for upsampling and
% continuous transmission at the desired center frequency.

%%
% The transmitter gain parameter is used to impair the quality of the
% received waveform, you can change this parameter to reduce transmission
% quality, and impair the signal. These are suggested values, depending on
% your antenna configuration, you may have to tweak these values. The
% suggested values are:
%
% # Set to 0 for increased gain (0dB)
% # Set to -10 for default gain (-10dB)
% # Set to -20 for reduced gain (-20dB)

txGain = 0;

%%
% *Prepare Image File*
% 
% The example reads data from the image file, scales it for transmission,
% and converts it to a stream of decimal bytes. The scaling of the image
% reduces the quality of the image by decreasing the size of the binary
% data stream.
%
% The size of the transmitted image directly impacts the number of WLAN
% packets which are required for the transmission of the image data. A
% scaling factor is used to scale the original size of the image. The
% number of WLAN packets that are generated for transmission is dependent
% on the following:
%
% # The image scaling that you set when importing the image file.
% # The length of the data carried in a packet. This is specified by the
% |msduLength| variable. 
% # The MCS value of the transmitted packet.
%
% The combination of scaling factor |scale| of 0.2, and MSDU length
% |msduLength| of 2304 as shown below, requires the transmission of 11 WLAN
% radio packets. Increasing the scaling factor or decreasing the MSDU
% length will result in the transmission of more packets.

% Input an image file and convert to binary stream
fileTx = 'peppers.png';            % Image file name
fData = imread(fileTx);            % Read image data from file
scale = 0.2;                       % Image scaling factor
origSize = size(fData);            % Original input image size
scaledSize = max(floor(scale.*origSize(1:2)),1); % Calculate new image size
heightIx = min(round(((1:scaledSize(1))-0.5)./scale+0.5),origSize(1));
widthIx = min(round(((1:scaledSize(2))-0.5)./scale+0.5),origSize(2));
fData = fData(heightIx,widthIx,:); % Resize image
imsize = size(fData);              % Store new image size
txImage = fData(:);

%%
% The example displays the image file that is to be transmitted. When the
% image file is successfully received and decoded, the example displays the
% image.

% Plot transmit image
figure(imFig);
imFig.Visible = 'on';
subplot(211); 
    imshow(fData);
    title('Transmitted Image');
subplot(212);
    title('Received image will appear here...');
    set(gca,'Visible','off');
    set(findall(gca, 'type', 'text'), 'visible', 'on');

pause(0); % Pause to plot Tx image

%%
% *Fragment transmit data*
%
% The example uses the data stream that is created from the input image
% file |txImage|. The data stream is split into smaller transmit units
% (MSDUs) of size |msduLength|. An MPDU is created for each transmit unit
% using the <matlab:doc('wlanMACFrame') wlanMACFrame> function. Each call
% to this function creates an MPDU corresponding to the given MSDU and the
% frame configuration object. The frame configuration object can be created
% using <matlab:doc('wlanMACFrameConfig') wlanMACFrameConfig> which can be
% used to configure the sequence number of the MPDU. All the MPDUs are then
% sequentially passed to the physical layer for transmission.
%
% In this example the |msduLength| field is set to 2304 bytes. This is to
% ensure that the maximum MSDU size specified in the standard [ <#24 1> ]
% is not exceeded. The data in the last MPDU is appended with zeros, this
% is to make all MPDUs the same size.


% List parameters for different OFDM MCS schemes
MCS = 0:7;
Modulation_char = ['1/2 BPSK','3/4 BPSK', '1/2 QPSK', '3/4 QPSK', '1/2 16QAM',...
    '3/4 16QAM', '2/3 64QAM', '3/4 64QAM'];
codedBitsPerOFDMSymbol= [48, 48, 96, 96, 192, 192, 288, 288];
codedBitsPerSubcarrier = [1, 1, 2, 2, 4, 4, 6, 6];

%Choose OFDM MCS modulation. Experiment with this and observe BER
OFDM_MCS = Modulation; 

bitsPerOctet = 8; %codedBitsPerSubcarrier(OFDM_MCS+1) + 2 ;
msduLength = (bitsPerOctet)*codedBitsPerOFDMSymbol(OFDM_MCS+1); % MSDU length in bytes
numMSDUs = ceil(length(txImage)/msduLength);
padZeros = msduLength-mod(length(txImage),msduLength);
txData = [txImage; zeros(padZeros,1)];
txDataBits = double(reshape(de2bi(txData, bitsPerOctet)', [], 1));

% Divide input data stream into fragments

data = zeros(0, 1);

for ind=0:numMSDUs-1
    
    % Extract image data (in octets) for each MPDU
    frameBody = txData(ind*msduLength+1:msduLength*(ind+1),:);
    
    % Create MAC frame configuration object and configure sequence number
    cfgMAC = wlanMACFrameConfig('FrameType', 'Data', 'SequenceNumber', ind);
    
    % Generate MPDU
    [mpdu, lengthMPDU]= wlanMACFrame(frameBody, cfgMAC);
    
    % Convert MPDU bytes to a bit stream
    psdu = reshape(de2bi(hex2dec(mpdu), bitsPerOctet)', [], 1);
    
    % Concatenate PSDUs for waveform generation
    data = [data; psdu]; %#ok<AGROW>
    
end

%% 
% *Generate IEEE 802.11a Baseband WLAN Signal*
%
% The non-HT waveform is synthesized using
% <matlab:doc('wlanWaveformGenerator') wlanWaveformGenerator> with a non-HT
% format configuration object. The object is created using the
% <matlab:doc('wlanNonHTConfig') wlanNonHTConfig> function. The properties
% of the object contain the configuration. In this example an object is
% configured for a 20 MHz bandwidth, 1 transmit antenna and 64QAM rate 2/3
% (MCS 6).

nonHTcfg = wlanNonHTConfig;         % Create packet configuration
nonHTcfg.MCS = OFDM_MCS;            % Modulation: ['1/2 BPSK','3/4 BPSK', '1/2 QPSK', '3/4 QPSK', '1/2 16QAM', '3/4 16QAM', '2/3 64QAM', '3/4 64QAM'];
nonHTcfg.Modulation = 'OFDM';       % Default is 'OFDM'
nonHTcfg.NumTransmitAntennas = 1;   % Number of transmit antenna
chanBW = cbw; %nonHTcfg.ChannelBandwidth;
nonHTcfg.PSDULength = lengthMPDU;   % Set the PSDU length

% The sdrTransmitter uses the |transmitRepeat| functionality to transmit
% the baseband WLAN waveform in a loop from the DDR memory on the PlutoSDR.
% The transmitted RF signal is oversampled and transmitted at 30 MHz.  The
% 802.11a signal is transmitted on channel 5, which corresponds to a center
% frequency of 2.432 GHz as defined in section 17.4.6.3 of [1].

sdrTransmitter = sdrtx(deviceNameSDR, 'RadioID','ip:192.168.3.1'); % Transmitter properties

% Resample the transmit waveform at 30 MHz
fs = wlanSampleRate(nonHTcfg); % Transmit sample rate in MHz
osf = 1.5;                     % Oversampling factor

sdrTransmitter.BasebandSampleRate = fs*osf; 
sdrTransmitter.CenterFrequency = ctrFreq;  % Channel 5
sdrTransmitter.ShowAdvancedProperties = true;
sdrTransmitter.Gain = txGain;

% Initialize the scrambler with a random integer for each packet
scramblerInitialization = randi([1 127],numMSDUs,1);

% Generate baseband NonHT packets separated by idle time 
txWaveform = wlanWaveformGenerator(data,nonHTcfg, ...
    'NumPackets',numMSDUs,'IdleTime',20e-6, ...
    'ScramblerInitialization',scramblerInitialization);

% Resample transmit waveform 
txWaveform  = resample(txWaveform,fs*osf,fs);

fprintf('\nGenerating WLAN transmit waveform:\n')

% Scale the normalized signal to avoid saturation of RF stages
powerScaleFactor = 0.8;
txWaveform = txWaveform.*(1/max(abs(txWaveform))*powerScaleFactor);

% Transmit RF waveform
sdrTransmitter.transmitRepeat(txWaveform);

%%
% *Repeated transmission using SDR Hardware*
%
% The |transmitRepeat| function transfers the baseband WLAN packets with
% idle time to the PlutoSDR, and stores the signal samples in hardware
% memory. The example then transmits the waveform continuously over the air
% until the release method of the transmit object is called. Messages are
% displayed in the command window to confirm that transmission has started
% successfully.

%% Receiver Design
%
% The general structure of the WLAN receiver can be described as follows:
%
% # Capture multiple packets of the transmitted WLAN signal using
% SDR hardware.
% # Detect a packet
% # Coarse carrier frequency offset is estimated and corrected
% # Fine timing synchronization is established. The L-STF, L-LTF and L-SIG
% samples are provided for fine timing to allow to adjust the packet
% detection at the start or end of the L-STF 
% # Fine carrier frequency offset is estimated and corrected
% # Perform a channel estimation for the received signal using the L-LTF
% # Detect the format of the packet
% # Decode the L-SIG field to recover the MCS value and the length of the
% data portion
% # Decode the data field to obtain the transmitted data within each
% packet
% # Decode the received PSDU and check if the frame check sequence (FCS)
% passed for the PSDU.
% # Order the decoded MSDUs based on the |SequenceNumber| property in the
% recovered MAC frame configuration object.
% # Combine the decoded MSDUs from all the transmitted packets to form the
% received image
%
% This example plots the power spectral density (PSD) of the captured
% waveform, and shows visualizations of the equalized data symbols, and
% the received image.
% 
%%
% *Receiver Setup*
% 
% The sdrReceiver is controlled using the properties defined in the
% |sdrReceiver| object. The sample rate of the receiver is 30 MHz, which is
% 1.5 times the baseband sample rate of 20 MHz.

%%
% An <matlab:plutoradiodoc('commsdrrxpluto') SDR Receiver> System object is
% used with the PlutoSDR to receive baseband data from the SDR hardware.

sdrReceiver = sdrrx(deviceNameSDR,'RadioID','ip:192.168.2.1');
sdrReceiver.BasebandSampleRate = sdrTransmitter.BasebandSampleRate;
sdrReceiver.CenterFrequency = sdrTransmitter.CenterFrequency;
sdrReceiver.GainSource = 'Manual';
sdrReceiver.Gain = 30;
sdrReceiver.OutputDataType = 'double';

% Configure the capture length equivalent to twice the length of the
% transmitted signal, this is to ensure that PSDUs are received in order.
% On reception the duplicate MAC fragments are removed.
captureLength = 2*length(txWaveform);
spectrumScope.SampleRate = sdrReceiver.BasebandSampleRate;

% Get the required field indices within a PSDU 
indLSTF = wlanFieldIndices(nonHTcfg,'L-STF'); 
indLLTF = wlanFieldIndices(nonHTcfg,'L-LTF'); 
indLSIG = wlanFieldIndices(nonHTcfg,'L-SIG');
Ns = indLSIG(2)-indLSIG(1)+1; % Number of samples in an OFDM symbol

%%
% *Capture Receive Packets* 
%%
% The transmitted waveform is captured using the PlutoSDR.
fprintf('\nStarting a new RF capture.\n')
    
burstCaptures = capture(sdrReceiver, captureLength, 'Samples');

%%
% *Receiver Processing* 
%%
% The example uses a while loop to capture and decode packets. The WLAN
% waveform is continually transmitted over the air in a loop, the first
% packet that is captured by the sdrReceiver is not guaranteed to be the
% first packet that was transmitted. This means that the packets may be
% decoded out of sequence. To enable the received packets to be recombined
% in the correct order, their sequence number must be determined. The
% decoded PSDU bits for each packet are passed to the
% <matlab:doc('wlanMPDUDecode') wlanMPDUDecode> function. This function
% decodes the MPDU and outputs the MSDU as well as the recovered MAC frame
% configuration object <matlab:doc('wlanMACFrameConfig')
% wlanMACFrameConfig>. The |SequenceNumber| property in the recovered MAC
% frame configuration object can be used for ordering the MSDUs in the
% transmitted sequence. The while loop finishes receive processing when a
% duplicate frame is detected, which is finally removed during receiver
% processing. In case of a missing frame the quality of the image is
% degraded.
%
% When the WLAN packet has successfully decoded, the detected sequence
% number is displayed in the command window for each received packet. The
% equalized data symbol constellation is shown for each received packet.

% Show power spectral density of the received waveform
spectrumScope(burstCaptures);

% Downsample the received signal
rxWaveform = resample(burstCaptures,fs,fs*osf);
rxWaveformLen = size(rxWaveform,1);
searchOffset = 0; % Offset from start of the waveform in samples

% Minimum packet length is 10 OFDM symbols
lstfLen = double(indLSTF(2)); % Number of samples in L-STF
minPktLen = lstfLen*5;
pktInd = 1;
sr = wlanSampleRate(nonHTcfg); % Sampling rate
fineTimingOffset = [];
packetSeq = [];
displayFlag = 0; % Flag to display the decoded information

% Perform EVM calculation
evmCalculator = comm.EVM('AveragingDimensions',[1 2 3]);
evmCalculator.MaximumEVMOutputPort = true;

% Receiver processing
while (searchOffset + minPktLen) <= rxWaveformLen    
    % Packet detect
    pktOffset = wlanPacketDetect(rxWaveform, chanBW, searchOffset, 0.8);
 
    % Adjust packet offset
    pktOffset = searchOffset+pktOffset;
    if isempty(pktOffset) || (pktOffset+double(indLSIG(2))>rxWaveformLen)
        if pktInd==1
            disp('** No packet detected **');
        end
        break;
    end

    % Extract non-HT fields and perform coarse frequency offset correction
    % to allow for reliable symbol timing
    nonHT = rxWaveform(pktOffset+(indLSTF(1):indLSIG(2)),:);
    coarseFreqOffset = wlanCoarseCFOEstimate(nonHT,chanBW); 
    nonHT = helperFrequencyOffset(nonHT,fs,-coarseFreqOffset);

    % Symbol timing synchronization
    fineTimingOffset = wlanSymbolTimingEstimate(nonHT,chanBW);
    
    % Adjust packet offset
    pktOffset = pktOffset+fineTimingOffset;

    % Timing synchronization complete: Packet detected and synchronized
    % Extract the non-HT preamble field after synchronization and
    % perform frequency correction
    if (pktOffset<0) || ((pktOffset+minPktLen)>rxWaveformLen) 
        searchOffset = pktOffset+1.5*lstfLen; 
        continue; 
    end
    fprintf('\nPacket-%d detected at index %d\n',pktInd,pktOffset+1);
  
    % Extract first 7 OFDM symbols worth of data for format detection and
    % L-SIG decoding
    nonHT = rxWaveform(pktOffset+(1:7*Ns),:);
    nonHT = helperFrequencyOffset(nonHT,fs,-coarseFreqOffset);

    % Perform fine frequency offset correction on the synchronized and
    % coarse corrected preamble fields
    lltf = nonHT(indLLTF(1):indLLTF(2),:);           % Extract L-LTF
    fineFreqOffset = wlanFineCFOEstimate(lltf,chanBW);
    nonHT = helperFrequencyOffset(nonHT,fs,-fineFreqOffset);
    cfoCorrection = coarseFreqOffset+fineFreqOffset; % Total CFO

    % Channel estimation using L-LTF
    lltf = nonHT(indLLTF(1):indLLTF(2),:);
    demodLLTF = wlanLLTFDemodulate(lltf,chanBW);
    chanEstLLTF = wlanLLTFChannelEstimate(demodLLTF,chanBW);

    % Noise estimation
    noiseVarNonHT = helperNoiseEstimate(demodLLTF);

    % Packet format detection using the 3 OFDM symbols immediately
    % following the L-LTF
    format = wlanFormatDetect(nonHT(indLLTF(2)+(1:3*Ns),:), ...
        chanEstLLTF,noiseVarNonHT,chanBW);
    disp(['  ' format ' format detected']);
    if ~strcmp(format,'Non-HT')
        fprintf('  A format other than Non-HT has been detected\n');
        searchOffset = pktOffset+1.5*lstfLen;
        continue;
    end
    
    % Recover L-SIG field bits
    [recLSIGBits,failCheck] = wlanLSIGRecover( ...
           nonHT(indLSIG(1):indLSIG(2),:), ...
           chanEstLLTF,noiseVarNonHT,chanBW);

    if failCheck
        fprintf('  L-SIG check fail \n');
        searchOffset = pktOffset+1.5*lstfLen;
        continue; 
    else
        fprintf('  L-SIG check pass \n');
    end

    % Retrieve packet parameters based on decoded L-SIG
    [lsigMCS,lsigLen,rxSamples] = helperInterpretLSIG(recLSIGBits,sr);

    if (rxSamples+pktOffset)>length(rxWaveform)
        disp('** Not enough samples to decode packet **');
        break;
    end
    
    % Apply CFO correction to the entire packet
    rxWaveform(pktOffset+(1:rxSamples),:) = helperFrequencyOffset(...
        rxWaveform(pktOffset+(1:rxSamples),:),fs,-cfoCorrection);

    % Create a receive Non-HT config object
    rxNonHTcfg = wlanNonHTConfig;
    rxNonHTcfg.MCS = lsigMCS;
    rxNonHTcfg.PSDULength = lsigLen;

    % Get the data field indices within a PPDU 
    indNonHTData = wlanFieldIndices(rxNonHTcfg,'NonHT-Data');

    % Recover PSDU bits using transmitted packet parameters and channel
    % estimates from L-LTF
    [rxPSDU,eqSym] = wlanNonHTDataRecover(rxWaveform(pktOffset+...
           (indNonHTData(1):indNonHTData(2)),:), ...
           chanEstLLTF,noiseVarNonHT,rxNonHTcfg);

    constellation(reshape(eqSym,[],1)); % Current constellation
    pause(0); % Allow constellation to repaint
    release(constellation); % Release previous constellation plot

    refSym = wlanClosestReferenceSymbol(eqSym,rxNonHTcfg);
    [evm.RMS,evm.Peak] = evmCalculator(refSym,eqSym);

    % Decode the MPDU and extract MSDU
    [cfgMACRx, msduList{pktInd}, status] = wlanMPDUDecode(rxPSDU, rxNonHTcfg); %#ok<*SAGROW>

    if strcmp(status, 'Success')
        disp('  MAC FCS check pass');
        
        % Store sequencing information
        packetSeq(pktInd) = cfgMACRx.SequenceNumber;
        
        % Convert MSDU to a binary data stream
        rxBit{pktInd} = reshape(de2bi(hex2dec(cell2mat(msduList{pktInd})), 8)', [], 1);
        
    else % Decoding failed
        if strcmp(status, 'FCSFailed')
            % FCS failed
            disp('  MAC FCS check fail');
        else
            % FCS passed but encountered other decoding failures
            disp('  MAC FCS check pass');
        end
        
        % Since there are no retransmissions modeled in this example, we'll
        % extract the image data (MSDU) and sequence number from the MPDU,
        % even though FCS check fails.
        
        % Remove header and FCS. Extract the MSDU.
        macHeaderBitsLength = 24*bitsPerOctet;
        fcsBitsLength = 4*bitsPerOctet;
        msduList{pktInd} = rxPSDU(macHeaderBitsLength+1 : end-fcsBitsLength);
        
        % Extract and store sequence number
        sequenceNumStartIndex = 23*bitsPerOctet+1;
        sequenceNumEndIndex = 25*bitsPerOctet - 4;
        packetSeq(pktInd) = bi2de(rxPSDU(sequenceNumStartIndex:sequenceNumEndIndex)');
        
        % MSDU binary data stream
        rxBit{pktInd} = double(msduList{pktInd});
    end
    
    % Display decoded information
    if displayFlag
        fprintf('  Estimated CFO: %5.1f Hz\n\n',cfoCorrection); %#ok<UNRCH>

        disp('  Decoded L-SIG contents: ');
        fprintf('                            MCS: %d\n',lsigMCS);
        fprintf('                         Length: %d\n',lsigLen);
        fprintf('    Number of samples in packet: %d\n\n',rxSamples);

        fprintf('  EVM:\n');
        fprintf('    EVM peak: %0.3f%%  EVM RMS: %0.3f%%\n\n', ...
        evm.Peak,evm.RMS);

        fprintf('  Decoded MAC Sequence Control field contents:\n');
        fprintf('    Sequence number:%d\n',packetSeq(pktInd));
    end

    % Update search index
    searchOffset = pktOffset+double(indNonHTData(2));

    
    pktInd = pktInd+1;
    % Finish processing when a duplicate packet is detected. The
    % recovered data includes bits from duplicate frame
    if length(unique(packetSeq))<length(packetSeq)
        break
    end  
end

% Release the state of sdrTransmitter and sdrReceiver object
release(sdrTransmitter); 
release(sdrReceiver);

%%
% *Reconstruct Image*
%%
% The image is reconstructed from the received MAC frames.
if ~(isempty(fineTimingOffset)||isempty(pktOffset))&& ...
        (numMSDUs==(numel(packetSeq)-1))
    % Remove the duplicate captured MAC fragment
    rxBitMatrix = cell2mat(rxBit); 
    rxData = rxBitMatrix(1:end,1:numel(packetSeq)-1);

    startSeq = find(packetSeq==0);
    rxData = circshift(rxData,[0 -(startSeq(1)-1)]);% Order MAC fragments

    % Perform bit error rate (BER) calculation
    bitErrorRate = comm.ErrorRate;
    err = bitErrorRate(double(rxData(:)), ...
                    txDataBits(1:length(reshape(rxData,[],1))));
    fprintf('  \nBit Error Rate (BER):\n');
    fprintf('          Bit Error Rate (BER) = %0.5f.\n',err(1));
    fprintf('          Number of bit errors = %d.\n', err(2));
    fprintf('    Number of transmitted bits = %d.\n\n',length(txDataBits));

    % Recreate image from received data
    fprintf('\nConstructing image from received data.\n');
    
    decdata = bi2de(reshape(rxData(1:length(txImage)*bitsPerOctet), 8, [])');   
  
    receivedImage = uint8(reshape(decdata,imsize));
    % Plot received image
    if exist('imFig', 'var') && ishandle(imFig) % If Tx figure is open
        figure(imFig); subplot(212); 
    else
        figure; subplot(212);
    end
    imshow(receivedImage);
    title(sprintf('Received Image'));
end

%% Things to Try
% You can modify the sdrTransmitter |txGain| gain to observe the difference in
% the EVM and BER after signal reception and processing. You should also be
% able to see any errors in the displayed, received image. Try changing the
% scaling factor |scale| to 0.5. This should improve the quality of the
% received image by generating more transmit bits. This should also
% increase the number of transmitted PPDUs.

%% Troubleshooting
%
% General tips for troubleshooting SDR hardware and the Communications
% Toolbox Support Package for ADALM-PLUTO Radio can be found in
% <matlab:plutoradiodoc('sdrpluto_troubleshoot') Common Problems and Fixes>.

%% Selected Bibliography
% # IEEE Std 802.11(TM)-2012 IEEE Standard for Information technology -
% Telecommunications and information exchange between systems - Local and
% metropolitan area networks - Specific requirements - Part 11: Wireless
% LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications.

displayEndOfDemoMessage(mfilename)
