#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PTT Tone maker
# Author: srs
# Copyright: srs 2021
# Description: NBFM PTT Tone JAmmer
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import iio

from gnuradio import qtgui

class PTT_Tone_Jammer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PTT Tone maker")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PTT Tone maker")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "PTT_Tone_Jammer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.pw = pw = 1
        self.pw_tau = pw_tau = round(pw/(1/samp_rate))
        self.pri = pri = 1
        self.duty_cycle = duty_cycle = 100
        self.pulse_spacing = pulse_spacing = round((pri/pw)*((100-duty_cycle)/100)*(pw_tau))
        self.radio_freq = radio_freq = 136050000
        self.pulse_vector = pulse_vector = [1]*pw_tau+[0]*(pulse_spacing)
        self.pulse_freq = pulse_freq = 410
        self.pri_tau = pri_tau = round(pri/(1/samp_rate))
        self.num_tones = num_tones = 1
        self.freq = freq = 136050000

        ##################################################
        # Blocks
        ##################################################
        self._radio_freq_range = Range(60000000, 6000000000, 1000000, 136050000, 200)
        self._radio_freq_win = RangeWidget(self._radio_freq_range, self.set_radio_freq, 'Radio Freq', "counter_slider", int)
        self.top_grid_layout.addWidget(self._radio_freq_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._pulse_freq_range = Range(10, 20e3, 100, 410, 200)
        self._pulse_freq_win = RangeWidget(self._pulse_freq_range, self.set_pulse_freq, 'Pulse Freq (Hz)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._pulse_freq_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._num_tones_range = Range(1, 100, 1, 1, 100)
        self._num_tones_win = RangeWidget(self._num_tones_range, self.set_num_tones, 'Number of Tones', "counter_slider", int)
        self.top_grid_layout.addWidget(self._num_tones_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            50000, #size
            samp_rate/2, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(False)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0.0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(True)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 2, 0, 1, 3)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            radio_freq, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 3, 0, 1, 3)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._pw_range = Range(1e-6, 1, 0.5e-6, 1, 200)
        self._pw_win = RangeWidget(self._pw_range, self.set_pw, 'PW (sec)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._pw_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._pri_range = Range(2e-6, 1, 0.5e-6, 1, 200)
        self._pri_win = RangeWidget(self._pri_range, self.set_pri, 'PRI (sec)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._pri_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.pluto_source('', int(freq), int(2084000), int(20000000), 32768, True, True, True, 'manual', 35, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('', int(radio_freq), int(samp_rate), int(20000000), 32768, False, 10.0, '', True)
        self._duty_cycle_range = Range(0, 100, 1, 100, 200)
        self._duty_cycle_win = RangeWidget(self._duty_cycle_range, self.set_duty_cycle, 'Duty Cycle (%)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._duty_cycle_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( num_tones, ((1,2)), ((),), ((),), ((),), "packet_len", True)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(pulse_vector, True, 1, [])
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_SAW_WAVE, pulse_freq, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_time_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PTT_Tone_Jammer")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_pri_tau(round(self.pri/(1/self.samp_rate)))
        self.set_pw_tau(round(self.pw/(1/self.samp_rate)))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_params(int(self.radio_freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.radio_freq, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/2)

    def get_pw(self):
        return self.pw

    def set_pw(self, pw):
        self.pw = pw
        self.set_pulse_spacing(round((self.pri/self.pw)*((100-self.duty_cycle)/100)*(self.pw_tau)))
        self.set_pw_tau(round(self.pw/(1/self.samp_rate)))

    def get_pw_tau(self):
        return self.pw_tau

    def set_pw_tau(self, pw_tau):
        self.pw_tau = pw_tau
        self.set_pulse_spacing(round((self.pri/self.pw)*((100-self.duty_cycle)/100)*(self.pw_tau)))
        self.set_pulse_vector([1]*self.pw_tau+[0]*(self.pulse_spacing))

    def get_pri(self):
        return self.pri

    def set_pri(self, pri):
        self.pri = pri
        self.set_pri_tau(round(self.pri/(1/self.samp_rate)))
        self.set_pulse_spacing(round((self.pri/self.pw)*((100-self.duty_cycle)/100)*(self.pw_tau)))

    def get_duty_cycle(self):
        return self.duty_cycle

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.set_pulse_spacing(round((self.pri/self.pw)*((100-self.duty_cycle)/100)*(self.pw_tau)))

    def get_pulse_spacing(self):
        return self.pulse_spacing

    def set_pulse_spacing(self, pulse_spacing):
        self.pulse_spacing = pulse_spacing
        self.set_pulse_vector([1]*self.pw_tau+[0]*(self.pulse_spacing))

    def get_radio_freq(self):
        return self.radio_freq

    def set_radio_freq(self, radio_freq):
        self.radio_freq = radio_freq
        self.iio_pluto_sink_0.set_params(int(self.radio_freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.radio_freq, self.samp_rate)

    def get_pulse_vector(self):
        return self.pulse_vector

    def set_pulse_vector(self, pulse_vector):
        self.pulse_vector = pulse_vector
        self.blocks_vector_source_x_0.set_data(self.pulse_vector, [])

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.analog_sig_source_x_0_0.set_frequency(self.pulse_freq)

    def get_pri_tau(self):
        return self.pri_tau

    def set_pri_tau(self, pri_tau):
        self.pri_tau = pri_tau

    def get_num_tones(self):
        return self.num_tones

    def set_num_tones(self, num_tones):
        self.num_tones = num_tones

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_pluto_source_0.set_params(int(self.freq), int(2084000), int(20000000), True, True, True, 'manual', 35, '', True)





def main(top_block_cls=PTT_Tone_Jammer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
