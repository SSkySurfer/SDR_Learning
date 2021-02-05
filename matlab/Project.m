clearvars, clc

%%
% Final project 
% ECE535 - SU2020
% Stephen Sweetnich

% Configure Radio
sdrsetup  %Setup RTLSDR receiver (rx)
configurePlutoRadio('AD9364'); % Setup ADALM-PLUTO transmitter(tx)
%% Set Transmit and receive ranges
f_s = 16e5;
f_c = 290e6; % Adjust to select open frequency
samplesPerFrame = 2^15;
samplesPerSymbol = 12;
decimation = 4;
% Create an SDR receiver System object with the specified properties. 
rx_name = 'RTL-SDR';
rx = comm.SDRRTLReceiver('RadioAddress','0','SampleRate',f_s, ...
    'CenterFrequency',f_c,'SamplesPerFrame',samplesPerFrame,...
    'FrequencyCorrection',-14,'OutputDataType','double',...
    'EnableBurstMode',true,'NumFramesInBurst',15);

% Create transmitter
tx_name='Pluto';
gain = -30; %dB
tx = sdrtx(tx_name,'RadioID', 'usb:0','BasebandSampleRate',f_s, ...
    'CenterFrequency',f_c,'OutputDataType','double','Gain',-50);

%% Create LTE transmission model
% Setup LTE waveform
% Configure Model for LTE
cfg = lteTestModel('1.1','10MHz');
dims = lteDLResourceGridSize(cfg); % binary format dimensions

%% Make Transmit Data
preamble = [1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]'; 
str = 'Hello there!I am gre8';
d = reshape(dec2bin(str,8).'-'0',1,[])';
d_size = prod(dims)*2/size(d,1);
d_long = repmat(d,d_size,1);
data =  [preamble;d];

str_read_test = char(bin2dec(reshape(char(data+'0'), 8,[]).'))';
str_read_test_one = str_read_test(10:length(str_read_test));

%regrid = reshape(lteSymbolModulate(data,'QPSK'),dims);
%wf= lteOFDMModulate(cfg,regrid);
%wf_demod = lteOFDMDemodulate(cfg,data);
% Setup M-QAM waveform
M=4;
wf = qammod(d,M,'bin','PlotConstellation',true);
wf_demod = qamdemod(wf,M,'bin','UnitAveragePower',true); %test demod

% Setup PSK waveform
%wf = pskmod(data,M,0,'bin');
%wf_demod = pskdemod(wf,M,0,'bin'); % Test demod
% Test demod on tx signal
str_read_wf = char(bin2dec(reshape(char(wf_demod+'0'), 8, []).'))';
str_read_wf_one = str_read_test(5:25);
%% Create Transmit filters
rctFilt = comm.RaisedCosineTransmitFilter('OutputSamplesPerSymbol', samplesPerSymbol);
rcrFilt = comm.RaisedCosineReceiveFilter('InputSamplesPerSymbol', samplesPerSymbol, ...
    'DecimationFactor', decimation);
%% Execute TX/RX
% Cature settings for lost frames and latency
frameTime = rx.SamplesPerFrame/rx.SampleRate;
% Transmit
tx.transmitRepeat(rctFilt(wf));
% Receive
rx_data = rcrFilt(rx());
% Create a delay
VFD = dsp.VariableFractionalDelay;
constDiagram= comm.ConstellationDiagram('XLimits',[-5, 5], 'YLimits', [-5,5]);
% Process received data for timing offset
remainingSPS = samplesPerSymbol/decimation;
% Take end of data after AGC converged
rx_data = rx_data(end-remainingSPS*1000+1:end);
    
%Delay signal
tau_hat = .5; 
delayedsig = VFD(rx_data, tau_hat);
% Interpolation (Linear)
data_pts = sum(reshape(delayedsig,remainingSPS,...
    length(delayedsig)/remainingSPS).',2)./remainingSPS;
constDiagram(rx_data);

release(tx);
release(rx);
%% Estimation of error
fftOrder = 2^10; k = 2;
modulationOrder= M;
frequencyRange = linspace(-f_s/2,f_s/2,fftOrder);
% Precalculate constants
offsetEstimates = zeros(floor(length(rx_data)/fftOrder),1);
indexToHz = f_s/(modulationOrder*fftOrder);
for est=1:length(offsetEstimates)
    % Increment indexes
    timeIndex = (k:k+fftOrder-1).';
    k = k + fftOrder;
    % Remove modulation effects
    sigNoMod = rx_data(timeIndex).^modulationOrder;
    % Take FFT and ABS
    freqHist = abs(fft(sigNoMod));
    % Determine most likely offset
    [~,maxInd] = max(freqHist);
    offsetInd = maxInd - 1;
    if maxInd>=fftOrder/2 % Compensate for spectrum shift
    offsetInd = offsetInd - fftOrder;
end
% Convert to Hz from normalized frequency index
offsetEstimates(est) = offsetInd * indexToHz;
end
%% Apply Corrections
frameSize = 2^15;
numFrames = 1; 
nSamples = numFrames*frameSize;
% Configure LF and PI
LoopFilter = dsp.IIRFilter('Structure', 'Direct form II transposed', ...
    'Numerator', [1 0], 'Denominator', [1 -1]);
Integrator = dsp.IIRFilter('Structure', 'Direct form II transposed', ...
    'Numerator', [0 1], 'Denominator', [1 -1]);
DampingFactors = [0.05];
NormalizedLoopBandwidth = 0.09;
for DampingFactor = DampingFactors
    % Calculate range estimates
    NormalizedPullInRange = min(1, 2*pi*sqrt(2)*DampingFactor*NormalizedLoopBandwidth);
    MaxFrequencyLockDelay = (4*NormalizedPullInRange^2)/...
    (NormalizedLoopBandwidth)^3;
    MaxPhaseLockDelay = 0.5/(NormalizedLoopBandwidth);
    % Calculate coefficients for FFC
    PhaseRecoveryLoopBandwidth = NormalizedLoopBandwidth*samplesPerSymbol;
    PhaseRecoveryGain = samplesPerSymbol;
    PhaseErrorDetectorGain = log2(M); DigitalSynthesizerGain = -1;
    theta = PhaseRecoveryLoopBandwidth/...
        ((DampingFactor + 0.25/DampingFactor)*samplesPerSymbol);
    delta = 1 + 2*DampingFactor*theta + theta*theta;
    % G1
    ProportionalGain = (4*DampingFactor*theta/delta)/...
        (PhaseErrorDetectorGain*PhaseRecoveryGain);
    % G3
    IntegratorGain = (4/samplesPerSymbol*theta*theta/delta)/...
    (PhaseErrorDetectorGain*PhaseRecoveryGain);
    % Correct carrier offset
    output = zeros(size(rx_data));
    Phase = 0; previousSample = complex(0);
    LoopFilter.release();Integrator.release();
    for k = 1:length(rx_data)-1
        % Complex phase shift   
        output(k) = rx_data(k+1)*exp(1i*Phase);
        % PED
        phErr = sign(real(previousSample)).*imag(previousSample)...
            - sign(imag(previousSample)).*real(previousSample); 
        % Loop Filter   
        loopFiltOut = step(LoopFilter,phErr*IntegratorGain);
        % Direct Digital Synthesizer
        DDSOut = step(Integrator,phErr*ProportionalGain + loopFiltOut);
        Phase = DigitalSynthesizerGain * DDSOut;
        previousSample = output(k);
    end
    scatterplot(output(end-1024:end-10));title('Dampened signal');
    xlabel('In-Phase'); ylabel('Quadrature')
end

%% Demodulate and plot
% Demodulate
%rx_data_demod = lteOFDMDemodulate(cfg,rx_data);
%rx_data_demod = qamdemod(rx_data,M,'bin','OutputType','bit');
pskDemodulator = comm.PSKDemodulator(M,'BitOutput',true);
rx_data_demod = pskDemodulator(output);
%%
str_read_final = char(bin2dec(reshape(char(rx_data_demod+'0'), 8,[]).'))';
str_read_final_one = str_read_test(1:21);
%%
% Plot TX and receive
figure(2)
scatterplot(wf); hold on
scatterplot(rx_data)




