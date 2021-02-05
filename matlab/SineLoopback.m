% Setup Receiver
sdrsetup  %Setup RTLSDR receiver (rx)
f_c = 120e6; %MHz
f_s = 1e6; % baseband Sample Rate'
s_f = 2^12; % Samples per frame
rx=sdrrx('Pluto','OutputDataType','double','BasebandSampleRate',f_s);
% rx = comm.SDRRTLReceiver('RadioAddress','0', ...
%     'CenterFrequency',f_c,'SamplesPerFrame',2^15,...
%     'FrequencyCorrection',-14,'OutputDataType','double',...
%     'EnableBurstMode',true,'NumFramesInBurst',15);
% Setup Transmitter
tx = sdrtx('Pluto','Gain',-30,'CenterFrequency',f_c);
% Transmit sinewave
sine = dsp.SineWave('Frequency',300,...
    'SampleRate',f_s,...
    'SamplesPerFrame', s_f,...
    'ComplexOutput', true);
tx.transmitRepeat(sine()); % Transmit continuously
% Setup Scope
samplesPerStep = s_f/s_f;
steps = 3;
ts = dsp.TimeScope(2, 'SampleRate', f_s,...
    'TimeSpan', samplesPerStep*steps,...
    'BufferLength', rx.SamplesPerFrame*steps);
% Receive and view sine
for k=1:steps
ts(rx(),sine()./50);
end