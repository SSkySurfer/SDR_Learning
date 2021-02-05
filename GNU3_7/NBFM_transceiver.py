#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NBFM_transceiver
# Author: SRS, 2020
# Description: Pluto SDR FM transceiver
# Generated: Tue Feb  2 13:06:19 2021
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class NBFM_transceiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NBFM_transceiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NBFM_transceiver")
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

        self.settings = Qt.QSettings("GNU Radio", "NBFM_transceiver")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.rx_freq = rx_freq = 141050000
        self.offset = offset = 5000000
        self.tx_gain = tx_gain = 15
        self.tx_freq = tx_freq = rx_freq-offset
        self.sqch = sqch = -60
        self.sdr_samp_rate = sdr_samp_rate = samp_rate*12
        self.rx_tx = rx_tx = 0
        self.rx_gain = rx_gain = 10
        self.rx_freq_fine = rx_freq_fine = 0
        self.rx_aud = rx_aud = 0.300

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 90, 1, 15, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'tx_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sqch_range = Range(-110, -50, 1, -60, 200)
        self._sqch_win = RangeWidget(self._sqch_range, self.set_sqch, 'rx_sqlch', "counter_slider", float)
        self.top_grid_layout.addWidget(self._sqch_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sdr_samp_rate_range = Range(520833 , 61440000, 100000, samp_rate*12, 200)
        self._sdr_samp_rate_win = RangeWidget(self._sdr_samp_rate_range, self.set_sdr_samp_rate, 'sdr_sample_rate', "counter_slider", float)
        self.top_grid_layout.addWidget(self._sdr_samp_rate_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_tx_options = (0, 1, )
        self._rx_tx_labels = ('RX', 'TX', )
        self._rx_tx_group_box = Qt.QGroupBox('rx_tx_pushbutton')
        self._rx_tx_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._rx_tx_button_group = variable_chooser_button_group()
        self._rx_tx_group_box.setLayout(self._rx_tx_box)
        for i, label in enumerate(self._rx_tx_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._rx_tx_box.addWidget(radio_button)
        	self._rx_tx_button_group.addButton(radio_button, i)
        self._rx_tx_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_tx_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._rx_tx_options.index(i)))
        self._rx_tx_callback(self.rx_tx)
        self._rx_tx_button_group.buttonClicked[int].connect(
        	lambda i: self.set_rx_tx(self._rx_tx_options[i]))
        self.top_grid_layout.addWidget(self._rx_tx_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = Range(0, 50, 1, 10, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'rx_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_freq_range = Range(88000000, 174000000, 25000, 141050000, 200)
        self._rx_freq_win = RangeWidget(self._rx_freq_range, self.set_rx_freq, 'rx_freq', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_freq_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_aud_range = Range(0, 0.5, 0.05, 0.300, 200)
        self._rx_aud_win = RangeWidget(self._rx_aud_range, self.set_rx_aud, 'rx_audio_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_aud_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._offset_options = (5000000, 600000, )
        self._offset_labels = ('5Mhz', '600kHz', )
        self._offset_tool_bar = Qt.QToolBar(self)
        self._offset_tool_bar.addWidget(Qt.QLabel('rx_tx_offset'+": "))
        self._offset_combo_box = Qt.QComboBox()
        self._offset_tool_bar.addWidget(self._offset_combo_box)
        for label in self._offset_labels: self._offset_combo_box.addItem(label)
        self._offset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._offset_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._offset_options.index(i)))
        self._offset_callback(self.offset)
        self._offset_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_offset(self._offset_options[i]))
        self.top_grid_layout.addWidget(self._offset_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_freq_tool_bar = Qt.QToolBar(self)

        if None:
          self._tx_freq_formatter = None
        else:
          self._tx_freq_formatter = lambda x: eng_notation.num_to_str(x)

        self._tx_freq_tool_bar.addWidget(Qt.QLabel('tx_freq'+": "))
        self._tx_freq_label = Qt.QLabel(str(self._tx_freq_formatter(self.tx_freq)))
        self._tx_freq_tool_bar.addWidget(self._tx_freq_label)
        self.top_grid_layout.addWidget(self._tx_freq_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_freq_fine_range = Range(-10000, 10000, 100, 0, 200)
        self._rx_freq_fine_win = RangeWidget(self._rx_freq_fine_range, self.set_rx_freq_fine, 'rx_freq_fine', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_freq_fine_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_0_1 = filter.rational_resampler_ccf(
                interpolation=samp_rate,
                decimation=sdr_samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate,
                decimation=sdr_samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=sdr_samp_rate,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	256, #fftsize
        	firdes.WIN_HAMMING, #wintype
        	rx_freq, #fc
        	25000, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 4, 0, 6, 3)
        for r in range(4, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)


        self.qtgui_sink_x_0.enable_rf_freq(True)



        self.pluto_source_0 = iio.pluto_source('', rx_freq, sdr_samp_rate, 15000, 0x4000, True, True, True, "manual", rx_gain*((-rx_tx)+1), '', True)
        self.pluto_sink_0 = iio.pluto_sink('192.168.2.1', rx_freq-offset, sdr_samp_rate, 5000, 0x4000, False, -tx_gain*(rx_tx), '', True)
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, samp_rate, 20000, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 10e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 16000, 200, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((rx_aud*(-(rx_tx)+1), ))
        self.audio_sink_0 = audio.sink(48000, "Speakers (Conexant SmartAudio HD)", True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sqch, 1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(sdr_samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=50e-6,
        	max_dev=12.5e3,
          )
        self.Internal_Microphone = audio.source(48000, '', True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.Internal_Microphone, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.pluto_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.pluto_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_1, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NBFM_transceiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sdr_samp_rate(self.samp_rate*12)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, 20000, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 10e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 16000, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.set_tx_freq(self._tx_freq_formatter(self.rx_freq-self.offset))
        self.qtgui_sink_x_0.set_frequency_range(self.rx_freq, 25000)
        self.pluto_source_0.set_params(self.rx_freq, self.sdr_samp_rate, 15000, True, True, True, "manual", self.rx_gain*((-self.rx_tx)+1), '', True)
        self.pluto_sink_0.set_params(self.rx_freq-self.offset, self.sdr_samp_rate, 5000, -self.tx_gain*(self.rx_tx), '', True)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self._offset_callback(self.offset)
        self.set_tx_freq(self._tx_freq_formatter(self.rx_freq-self.offset))
        self.pluto_sink_0.set_params(self.rx_freq-self.offset, self.sdr_samp_rate, 5000, -self.tx_gain*(self.rx_tx), '', True)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.pluto_sink_0.set_params(self.rx_freq-self.offset, self.sdr_samp_rate, 5000, -self.tx_gain*(self.rx_tx), '', True)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        Qt.QMetaObject.invokeMethod(self._tx_freq_label, "setText", Qt.Q_ARG("QString", self.tx_freq))

    def get_sqch(self):
        return self.sqch

    def set_sqch(self, sqch):
        self.sqch = sqch
        self.analog_simple_squelch_cc_0.set_threshold(self.sqch)

    def get_sdr_samp_rate(self):
        return self.sdr_samp_rate

    def set_sdr_samp_rate(self, sdr_samp_rate):
        self.sdr_samp_rate = sdr_samp_rate
        self.pluto_source_0.set_params(self.rx_freq, self.sdr_samp_rate, 15000, True, True, True, "manual", self.rx_gain*((-self.rx_tx)+1), '', True)
        self.pluto_sink_0.set_params(self.rx_freq-self.offset, self.sdr_samp_rate, 5000, -self.tx_gain*(self.rx_tx), '', True)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.sdr_samp_rate)

    def get_rx_tx(self):
        return self.rx_tx

    def set_rx_tx(self, rx_tx):
        self.rx_tx = rx_tx
        self._rx_tx_callback(self.rx_tx)
        self.pluto_source_0.set_params(self.rx_freq, self.sdr_samp_rate, 15000, True, True, True, "manual", self.rx_gain*((-self.rx_tx)+1), '', True)
        self.pluto_sink_0.set_params(self.rx_freq-self.offset, self.sdr_samp_rate, 5000, -self.tx_gain*(self.rx_tx), '', True)
        self.blocks_multiply_const_vxx_0.set_k((self.rx_aud*(-(self.rx_tx)+1), ))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.pluto_source_0.set_params(self.rx_freq, self.sdr_samp_rate, 15000, True, True, True, "manual", self.rx_gain*((-self.rx_tx)+1), '', True)

    def get_rx_freq_fine(self):
        return self.rx_freq_fine

    def set_rx_freq_fine(self, rx_freq_fine):
        self.rx_freq_fine = rx_freq_fine

    def get_rx_aud(self):
        return self.rx_aud

    def set_rx_aud(self, rx_aud):
        self.rx_aud = rx_aud
        self.blocks_multiply_const_vxx_0.set_k((self.rx_aud*(-(self.rx_tx)+1), ))


def main(top_block_cls=NBFM_transceiver, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
