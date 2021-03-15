#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulse Radar
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
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import iio

from gnuradio import qtgui

class pulse_radar(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Pulse Radar")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pulse Radar")
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

        self.settings = Qt.QSettings("GNU Radio", "pulse_radar")

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
        self.tgt_pw = tgt_pw = 10e-3
        self.samp_rate = samp_rate = 2000000
        self.tgt_pw_tau = tgt_pw_tau = round(tgt_pw/(1/samp_rate))
        self.tgt_pri = tgt_pri = 10e-2
        self.percent_tracks = percent_tracks = 50
        self.track_spacing = track_spacing = round((tgt_pri/tgt_pw)*((100-percent_tracks)/100)*(tgt_pw_tau))
        self.tgt_pri_tau = tgt_pri_tau = round(tgt_pri/(1/samp_rate))
        self.pulse_vector = pulse_vector = [1]*tgt_pw_tau+[0]*(track_spacing)
        self.pulse_freq = pulse_freq = 200
        self.freq = freq = 136050000

        ##################################################
        # Blocks
        ##################################################
        self._pulse_freq_range = Range(10, 10e3, 100, 200, 200)
        self._pulse_freq_win = RangeWidget(self._pulse_freq_range, self.set_pulse_freq, 'Pulse Freq', "counter_slider", float)
        self.top_grid_layout.addWidget(self._pulse_freq_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tgt_pw_range = Range(1e-6, 1, 0.5e-6, 10e-3, 200)
        self._tgt_pw_win = RangeWidget(self._tgt_pw_range, self.set_tgt_pw, 'target radar PW', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tgt_pw_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tgt_pri_range = Range(2e-6, 1, 0.5e-6, 10e-2, 200)
        self._tgt_pri_win = RangeWidget(self._tgt_pri_range, self.set_tgt_pri, 'target radar PRI', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tgt_pri_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            100000, #size
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
            pulse_freq, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



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
        self._percent_tracks_range = Range(0, 100, 1, 50, 200)
        self._percent_tracks_win = RangeWidget(self._percent_tracks_range, self.set_percent_tracks, 'percent_tracks', "counter_slider", float)
        self.top_grid_layout.addWidget(self._percent_tracks_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.pluto_source('', int(freq), int(2084000), int(20000000), 32768, True, True, True, 'manual', 35, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('', int(freq), int(samp_rate), int(20000000), 32768, False, 10.0, '', True)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(pulse_vector, True, 1, [])
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, pulse_freq, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_time_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pulse_radar")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tgt_pw(self):
        return self.tgt_pw

    def set_tgt_pw(self, tgt_pw):
        self.tgt_pw = tgt_pw
        self.set_tgt_pw_tau(round(self.tgt_pw/(1/self.samp_rate)))
        self.set_track_spacing(round((self.tgt_pri/self.tgt_pw)*((100-self.percent_tracks)/100)*(self.tgt_pw_tau)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_tgt_pri_tau(round(self.tgt_pri/(1/self.samp_rate)))
        self.set_tgt_pw_tau(round(self.tgt_pw/(1/self.samp_rate)))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_params(int(self.freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.pulse_freq, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate/2)

    def get_tgt_pw_tau(self):
        return self.tgt_pw_tau

    def set_tgt_pw_tau(self, tgt_pw_tau):
        self.tgt_pw_tau = tgt_pw_tau
        self.set_pulse_vector([1]*self.tgt_pw_tau+[0]*(self.track_spacing))
        self.set_track_spacing(round((self.tgt_pri/self.tgt_pw)*((100-self.percent_tracks)/100)*(self.tgt_pw_tau)))

    def get_tgt_pri(self):
        return self.tgt_pri

    def set_tgt_pri(self, tgt_pri):
        self.tgt_pri = tgt_pri
        self.set_tgt_pri_tau(round(self.tgt_pri/(1/self.samp_rate)))
        self.set_track_spacing(round((self.tgt_pri/self.tgt_pw)*((100-self.percent_tracks)/100)*(self.tgt_pw_tau)))

    def get_percent_tracks(self):
        return self.percent_tracks

    def set_percent_tracks(self, percent_tracks):
        self.percent_tracks = percent_tracks
        self.set_track_spacing(round((self.tgt_pri/self.tgt_pw)*((100-self.percent_tracks)/100)*(self.tgt_pw_tau)))

    def get_track_spacing(self):
        return self.track_spacing

    def set_track_spacing(self, track_spacing):
        self.track_spacing = track_spacing
        self.set_pulse_vector([1]*self.tgt_pw_tau+[0]*(self.track_spacing))

    def get_tgt_pri_tau(self):
        return self.tgt_pri_tau

    def set_tgt_pri_tau(self, tgt_pri_tau):
        self.tgt_pri_tau = tgt_pri_tau

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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.pulse_freq, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.iio_pluto_sink_0.set_params(int(self.freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.freq), int(2084000), int(20000000), True, True, True, 'manual', 35, '', True)





def main(top_block_cls=pulse_radar, options=None):

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
