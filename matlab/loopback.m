% Setup Receiver
samplesPerFrame = 2^15;
rx=sdrrx('Pluto','OutputDataType','double','SamplesPerFrame',samplesPerFrame,...
    'GainSource','AGC Slow Attack','Gain',0);
% Setup Transmitter
tx = sdrtx('Pluto','Gain',-30);
% Transmit sinewave
pulse = dsp.SignalSource('SamplesPerFrame', samplesPerFrame,...
    'SignalEndAction','Cyclic repetition');
    pri = 1e-3; %sec, pulse repetition interval
    pw = 50e-6; %sec, pulse width
    sbw = 200e3; %Hz, sweep bandwidth
    fs = rx.BasebandSampleRate;
    t = [0:1/fs:pri];
    dc = pw/pri; %duty cycle
    sig = phased.LinearFMWaveform('PRF',1/pri,'SweepBandwidth',sbw,...
    'PulseWidth',pw,'NumPulses',5);
    pulse.Signal = sig();
% sinew = dsp.SineWave('Frequency',300,...
%                     'SampleRate',rx.BasebandSampleRate,...
%                     'SamplesPerFrame', 2^15,...
%                     'ComplexOutput', true);
tx.transmitRepeat(pulse()); % Transmit continuously
% Setup Scope
samplesPerStep = rx.SamplesPerFrame/rx.BasebandSampleRate;
steps = 1;
ts = dsp.TimeScope('SampleRate', rx.BasebandSampleRate,...
                   'TimeSpan', samplesPerStep*steps,...
                   'BufferLength', rx.SamplesPerFrame*steps);
% Receive and view sine
for k=1:steps
  ts(rx());
end
