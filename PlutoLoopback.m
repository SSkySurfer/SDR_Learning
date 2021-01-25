%%configure radio
release(tx);
release(rx);
configurePlutoRadio('AD9364'); % Setup ADALM-PLUTO transmitter(tx)

%% Run program
% User tunable (samplesPerSymbol>=decimation)
M= 4;  % Modulation order and Samples per symbol
% Create binary data
data = randi([0 1],2^16,1);
samplesPerSymbol = 2^7; decimation = 4;
samplesPerFrame = 4e6;
% Set up radio
f_c = 3000e6; % Adjust to select open frequency
tx = sdrtx('Pluto','Gain',-40,'CenterFrequency',f_c);
rx=sdrrx('Pluto','OutputDataType','double','SamplesPerFrame',samplesPerFrame,'CenterFrequency',f_c);
% Or use an RTL-SDR Rx
%sdrsetup  %Setup RTLSDR receiver (rx)

% rx = comm.SDRRTLReceiver('RadioAddress','0', ...
%     'CenterFrequency',f_c,'SamplesPerFrame',SamplesPerFrame,...
%     'FrequencyCorrection',-14,'OutputDataType','double',...
%     'EnableBurstMode',true,'NumFramesInBurst',30);

% Create a QAM modulator System object and modulate data

modData = qammod(data,M,'bin');
% Set up filters
rctFilt = comm.RaisedCosineTransmitFilter( ...
    'OutputSamplesPerSymbol', samplesPerSymbol);
rcrFilt = comm.RaisedCosineReceiveFilter( ...
    'InputSamplesPerSymbol', samplesPerSymbol, ...
    'DecimationFactor', decimation);
% Pass data through radio
tx.transmitRepeat(rctFilt(modData)); data = rcrFilt(rx());
% Set up visualization and delay objects
VFD = dsp.VariableFractionalDelay('Bandwidth',1); 
cd = comm.ConstellationDiagram;
% Process received data for timing offset
remainingSPS = samplesPerSymbol/decimation;
% Grab end of data where AGC has converged
l=length(data);
data = data(end-remainingSPS*900+1:end);
for index = 0:100
% Delay signal
tau_hat = index/50;
delayedsig = VFD(data, tau_hat);
% Linear interpolation
o = sum(reshape(delayedsig,remainingSPS,...
    length(delayedsig)/remainingSPS).',2)./remainingSPS;
% Visualize constellation
cd(o); pause(0.01);
end