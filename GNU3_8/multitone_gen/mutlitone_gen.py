#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: multitone_gen
# Author: srs
# Copyright: srs 2021
# Description: multitone waveform generator
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
from PyQt5.QtCore import QObject, pyqtSlot
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
import epy_block_0
import iio

from gnuradio import qtgui

class mutlitone_gen(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "multitone_gen")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("multitone_gen")
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

        self.settings = Qt.QSettings("GNU Radio", "mutlitone_gen")

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
        self.waveform = waveform = 0
        self.tone_freq = tone_freq = 100
        self.sdr_freq = sdr_freq = 136050000
        self.samp_rate = samp_rate = 30000000
        self.num_tones = num_tones = 3
        self.jam_button = jam_button = 0
        self.freq_spacing = freq_spacing = 1000000

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._waveform_options = (0, 1, 2, )
        # Create the labels list
        self._waveform_labels = ('Square', 'Sawtooth', 'Sine', )
        # Create the combo box
        # Create the radio buttons
        self._waveform_group_box = Qt.QGroupBox('Select Waveform ' + ": ")
        self._waveform_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._waveform_button_group = variable_chooser_button_group()
        self._waveform_group_box.setLayout(self._waveform_box)
        for i, _label in enumerate(self._waveform_labels):
            radio_button = Qt.QRadioButton(_label)
            self._waveform_box.addWidget(radio_button)
            self._waveform_button_group.addButton(radio_button, i)
        self._waveform_callback = lambda i: Qt.QMetaObject.invokeMethod(self._waveform_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._waveform_options.index(i)))
        self._waveform_callback(self.waveform)
        self._waveform_button_group.buttonClicked[int].connect(
            lambda i: self.set_waveform(self._waveform_options[i]))
        self.top_grid_layout.addWidget(self._waveform_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tone_freq_range = Range(100, 10000000, 100, 100, 200)
        self._tone_freq_win = RangeWidget(self._tone_freq_range, self.set_tone_freq, 'Tone Frequency', "counter_slider", int)
        self.top_grid_layout.addWidget(self._tone_freq_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sdr_freq_range = Range(60000000, 6000000000, 10000, 136050000, 200)
        self._sdr_freq_win = RangeWidget(self._sdr_freq_range, self.set_sdr_freq, 'SDR frequency', "counter_slider", int)
        self.top_grid_layout.addWidget(self._sdr_freq_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._num_tones_range = Range(1, 100, 1, 3, 200)
        self._num_tones_win = RangeWidget(self._num_tones_range, self.set_num_tones, 'Number of Tones', "counter_slider", int)
        self.top_grid_layout.addWidget(self._num_tones_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _jam_button_push_button = Qt.QPushButton('JAM')
        _jam_button_push_button = Qt.QPushButton('JAM')
        self._jam_button_choices = {'Pressed': 1, 'Released': 0}
        _jam_button_push_button.pressed.connect(lambda: self.set_jam_button(self._jam_button_choices['Pressed']))
        _jam_button_push_button.released.connect(lambda: self.set_jam_button(self._jam_button_choices['Released']))
        self.top_grid_layout.addWidget(_jam_button_push_button, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_spacing_range = Range(25000, 10000000, 25000, 1000000, 200)
        self._freq_spacing_win = RangeWidget(self._freq_spacing_range, self.set_freq_spacing, 'Spacing of Tones', "counter_slider", int)
        self.top_grid_layout.addWidget(self._freq_spacing_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            tone_freq, #fc
            (num_tones*freq_spacing) , #bw
            "", #name
            2
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['rx_data', 'tx_data', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["yellow", "magenta", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 2, 3)
        for r in range(2, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.pluto_source('', int(sdr_freq), int(samp_rate), int(20000000), 32768, True, True, True, 'manual', 60, '', True)
        self.iio_pluto_sink_0 = iio.pluto_sink('', int(sdr_freq), int(samp_rate), int(20000000), 32768, False, 10.0, '', True)
        self.epy_block_0 = epy_block_0.blk(waveform=waveform, samp_rate=samp_rate, ctr_freq=10000000, num_tones=num_tones, freq_spacing=freq_spacing)
        self.blocks_mute_xx_0 = blocks.mute_cc(bool(not(jam_button)))
        self.analog_sig_source_x_0_0_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, tone_freq, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0_0_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_mute_xx_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_mute_xx_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.epy_block_0, 0), (self.blocks_mute_xx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mutlitone_gen")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_waveform(self):
        return self.waveform

    def set_waveform(self, waveform):
        self.waveform = waveform
        self._waveform_callback(self.waveform)
        self.epy_block_0.waveform = self.waveform

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq
        self.analog_sig_source_x_0_0_0_0_0.set_frequency(self.tone_freq)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.tone_freq, (self.num_tones*self.freq_spacing) )

    def get_sdr_freq(self):
        return self.sdr_freq

    def set_sdr_freq(self, sdr_freq):
        self.sdr_freq = sdr_freq
        self.iio_pluto_sink_0.set_params(int(self.sdr_freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.sdr_freq), int(self.samp_rate), int(20000000), True, True, True, 'manual', 60, '', True)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0_0_0_0.set_sampling_freq(self.samp_rate)
        self.epy_block_0.samp_rate = self.samp_rate
        self.iio_pluto_sink_0.set_params(int(self.sdr_freq), int(self.samp_rate), int({bandwidth}), 10.0, '', True)
        self.iio_pluto_source_0.set_params(int(self.sdr_freq), int(self.samp_rate), int(20000000), True, True, True, 'manual', 60, '', True)

    def get_num_tones(self):
        return self.num_tones

    def set_num_tones(self, num_tones):
        self.num_tones = num_tones
        self.epy_block_0.num_tones = self.num_tones
        self.qtgui_freq_sink_x_0.set_frequency_range(self.tone_freq, (self.num_tones*self.freq_spacing) )

    def get_jam_button(self):
        return self.jam_button

    def set_jam_button(self, jam_button):
        self.jam_button = jam_button
        self.blocks_mute_xx_0.set_mute(bool(not(self.jam_button)))

    def get_freq_spacing(self):
        return self.freq_spacing

    def set_freq_spacing(self, freq_spacing):
        self.freq_spacing = freq_spacing
        self.epy_block_0.freq_spacing = self.freq_spacing
        self.qtgui_freq_sink_x_0.set_frequency_range(self.tone_freq, (self.num_tones*self.freq_spacing) )





def main(top_block_cls=mutlitone_gen, options=None):

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
