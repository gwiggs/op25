#!/usr/bin/env python

# Copyright 2011, 2012, 2013, 2014, 2015 Max H. Parke KA1RBI
# 
# This file is part of OP25
# 
# OP25 is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# OP25 is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with OP25; see the file COPYING. If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Boston, MA
# 02110-1301, USA.

import sys
import os
import time
import subprocess

from gnuradio import gr, gru, eng_notation
from gnuradio import blocks, audio
from gnuradio.eng_option import eng_option
import numpy as np
from gnuradio import gr
from math import pi

_def_debug = 0
_def_sps = 5
_def_sps_mult = 2

GNUPLOT = '/usr/bin/gnuplot'

<<<<<<< HEAD
FFT_AVG  = 0.25
MIX_AVG  = 0.15
BAL_AVG  = 0.05
FFT_BINS = 512
=======
FFT_AVG  = 0.05
MIX_AVG  = 0.10
BAL_AVG  = 0.05
FFT_BINS = 512    # number of fft bins
FFT_FREQ = 0.05   # time interval between fft updates
MIX_FREQ = 0.02   # time interval between mixer updates
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782

def degrees(r):
	d = 360 * r / (2*pi)
	while d <0:
		d += 360
	while d > 360:
		d -= 360
	return d

def limit(a,lim):
	if a > lim:
		return lim
	return a

class wrap_gp(object):
<<<<<<< HEAD
	def __init__(self, sps=_def_sps, logfile=None):
=======
	def __init__(self, sps=_def_sps, plot_name=""):
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
		self.sps = sps
		self.center_freq = 0.0
		self.relative_freq = 0.0
		self.offset_freq = 0.0
		self.width = None
		self.ffts = ()
		self.freqs = ()
		self.avg_pwr = np.zeros(FFT_BINS)
		self.avg_sum_pwr = 0.0
		self.buf = []
		self.plot_count = 0
		self.last_plot = 0
		self.plot_interval = None
		self.sequence = 0
		self.output_dir = None
		self.filename = None
<<<<<<< HEAD
		self.logfile = logfile
=======
                if plot_name == "":
                        self.plot_name = ""
                else:
			self.plot_name = plot_name + " "
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782

		self.attach_gp()

	def attach_gp(self):
		args = (GNUPLOT, '-noraise')
		exe  = GNUPLOT
		self.gp = subprocess.Popen(args, executable=exe, stdin=subprocess.PIPE)

        def set_sps(self, sps):
            self.sps = sps

	def kill(self):
		try:
			self.gp.stdin.close()   # closing pipe should cause subprocess to exit
		except IOError:
			pass
		sleep_count = 0
		while True:                     # wait politely, but only for so long
			self.gp.poll()
			if self.gp.returncode is not None:
				break
			time.sleep(0.1)
<<<<<<< HEAD
			if self.gp.returncode is not None:
				break
			sleep_count += 1
			if (sleep_count & 1) == 0:
				self.gp.kill()
			if sleep_count >= 3:
				break
=======
			sleep_count += 1
			if (sleep_count % 5) == 0:
				self.gp.kill()
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782

	def set_interval(self, v):
		self.plot_interval = v

	def set_output_dir(self, v):
		self.output_dir = v

	def plot(self, buf, bufsz, mode='eye'):
		BUFSZ = bufsz
		consumed = min(len(buf), BUFSZ-len(self.buf))
		if len(self.buf) < BUFSZ:
			self.buf.extend(buf[:consumed])
			return consumed

		self.plot_count += 1
		if mode == 'eye' and self.plot_count % 20 != 0:
			self.buf = []
			return consumed

		plots = []
		s = ''
		plot_size = (320,240)
		while(len(self.buf)):
			if mode == 'eye':
				if len(self.buf) < self.sps:
					break
				for i in range(self.sps):
					s += '%f\n' % self.buf[i]
				s += 'e\n'
				self.buf=self.buf[self.sps:]
				plots.append('"-" with lines')
 			elif mode == 'constellation':
				plot_size = (240,240)
				self.buf = self.buf[:100]
 				for b in self.buf:
					s += '%f\t%f\n' % (degrees(np.angle(b)), limit(np.abs(b),1.0))
 				s += 'e\n'
 				plots.append('"-" with points')
				for b in self.buf:
					#s += '%f\t%f\n' % (b.real, b.imag)
					s += '%f\t%f\n' % (degrees(np.angle(b)), limit(np.abs(b),1.0))
				s += 'e\n'
				self.buf = []
				plots.append('"-" with lines')
			elif mode == 'symbol':
				for b in self.buf:
					s += '%f\n' % (b)
				s += 'e\n'
				self.buf = []
				plots.append('"-" with points')
			elif mode == 'fft' or mode == 'mixer':
				sum_pwr = 0.0
<<<<<<< HEAD
				self.ffts = np.fft.fft(self.buf * np.blackman(BUFSZ)) / (0.42 * BUFSZ)
=======
				self.ffts = np.fft.fft((self.buf * np.blackman(BUFSZ)), BUFSZ , 0) / (0.42 * BUFSZ)
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
				self.ffts = np.fft.fftshift(self.ffts)
				self.freqs = np.fft.fftfreq(len(self.ffts))
				self.freqs = np.fft.fftshift(self.freqs)
				tune_freq = (self.center_freq - self.relative_freq) / 1e6
				if self.center_freq and self.width:
                                	self.freqs = ((self.freqs * self.width) + self.center_freq + self.offset_freq) / 1e6
				for i in xrange(len(self.ffts)):
					if mode == 'fft':
						self.avg_pwr[i] = ((1.0 - FFT_AVG) * self.avg_pwr[i]) + (FFT_AVG * np.abs(self.ffts[i]))
					else:
						self.avg_pwr[i] = ((1.0 - MIX_AVG) * self.avg_pwr[i]) + (MIX_AVG * np.abs(self.ffts[i]))
					s += '%f\t%f\n' % (self.freqs[i], 20 * np.log10(self.avg_pwr[i]))
					if (mode == 'mixer') and (self.avg_pwr[i] > 1e-5):
						if (self.freqs[i] - self.center_freq) < 0:
							sum_pwr -= self.avg_pwr[i]
						elif (self.freqs[i] - self.center_freq) > 0:
							sum_pwr += self.avg_pwr[i]
						self.avg_sum_pwr = ((1.0 - BAL_AVG) * self.avg_sum_pwr) + (BAL_AVG * sum_pwr)
<<<<<<< HEAD
				s += 'e\n'
				self.buf = []
				plots.append('"-" with lines')
			elif mode == 'float':
				for b in self.buf:
					s += '%f\n' % (b)
=======
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
				s += 'e\n'
				self.buf = []
				plots.append('"-" with lines')
		self.buf = []

		# FFT processing needs to be completed to maintain the weighted average buckets
		# regardless of whether we actually produce a new plot or not.
		if self.plot_interval and self.last_plot + self.plot_interval > time.time():
			return consumed
		self.last_plot = time.time()

		filename = None
		if self.output_dir:
			if self.sequence >= 2:
				delete_pathname = '%s/plot-%s-%d.png' % (self.output_dir, mode, self.sequence-2)
				if os.access(delete_pathname, os.W_OK):
					os.remove(delete_pathname)
			h0= 'set terminal png size %d, %d\n' % (plot_size)
			filename = 'plot-%s-%d.png' % (mode, self.sequence)
			h0 += 'set output "%s/%s"\n' % (self.output_dir, filename)
			self.sequence += 1
		else:
			h0= 'set terminal x11 noraise\n'
		background = ''
		h = 'set key off\n'
		if mode == 'constellation':
			h+= background
			h+= 'set size square\n'
			h+= 'set xrange [-1:1]\n'
			h+= 'set yrange [-1:1]\n'
<<<<<<< HEAD
			h += 'unset border\n'
			h += 'set polar\n'
			h += 'set angles degrees\n'
			h += 'unset raxis\n'
			h += 'set object circle at 0,0 size 1 fillcolor rgb 0x0f01 fillstyle solid behind\n'
			h += 'set style line 10 lt 1 lc rgb 0x404040 lw 0.1\n'
			h += 'set grid polar 45\n'
			h += 'set grid ls 10\n'
			h += 'set xtics axis\n'
			h += 'set ytics axis\n'
			h += 'set xtics scale 0\n'
			h += 'set xtics ("" 0.2, "" 0.4, "" 0.6, "" 0.8, "" 1)\n'
			h += 'set ytics 0, 0.2, 1\n'
			h += 'set format ""\n'
			h += 'set style line 11 lt 1 lw 2 pt 2 ps 2\n'

                        h+= 'set title "Constellation"\n'
		elif mode == 'eye':
			h+= background
			h+= 'set yrange [-4:4]\n'
                        h+= 'set title "Datascope"\n'
		elif mode == 'symbol':
			h+= background
			h+= 'set yrange [-4:4]\n'
                        h+= 'set title "Symbol"\n'
=======
                        h+= 'set title "%sConstellation"\n' % self.plot_name
		elif mode == 'eye':
			h+= background
			h+= 'set yrange [-4:4]\n'
                        h+= 'set title "%sDatascope"\n' % self.plot_name
		elif mode == 'symbol':
			h+= background
			h+= 'set yrange [-4:4]\n'
                        h+= 'set title "%sSymbol"\n' % self.plot_name
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
		elif mode == 'fft' or mode == 'mixer':
			h+= 'unset arrow; unset title\n'
			h+= 'set xrange [%f:%f]\n' % (self.freqs[0], self.freqs[len(self.freqs)-1])
                        h+= 'set xlabel "Frequency"\n'
                        h+= 'set ylabel "Power(dB)"\n'
                        h+= 'set grid\n'
			h+= 'set yrange [-100:0]\n'
			if mode == 'mixer':	# mixer
<<<<<<< HEAD
                                h+= 'set title "Mixer: balance %3.0f (smaller is better)"\n' % (np.abs(self.avg_sum_pwr * 1000))
			else:			# fft
                                h+= 'set title "Spectrum"\n'
				if self.center_freq:
					arrow_pos = (self.center_freq - self.relative_freq) / 1e6
					h+= 'set arrow from %f, graph 0 to %f, graph 1 nohead\n' % (arrow_pos, arrow_pos)
					h+= 'set title "Spectrum: tuned to %f Mhz"\n' % arrow_pos
		elif mode == 'float':
			h+= 'set yrange [-2:2]\n'
                        h+= 'set title "Oscilloscope"\n'
		dat = '%s%splot %s\n%s' % (h0, h, ','.join(plots), s)
                if self.logfile is not None:
                    with open(self.logfile, 'a') as fd:
                        fd.write(dat)
=======
                                h+= 'set title "%sMixer: balance %3.0f (smaller is better)"\n' % (self.plot_name, (np.abs(self.avg_sum_pwr * 1000)))
			else:			# fft
                                h+= 'set title "%sSpectrum"\n' % self.plot_name
				if self.center_freq:
					arrow_pos = (self.center_freq - self.relative_freq) / 1e6
					h+= 'set arrow from %f, graph 0 to %f, graph 1 nohead\n' % (arrow_pos, arrow_pos)
					h+= 'set title "%sSpectrum: tuned to %f Mhz"\n' % (self.plot_name, arrow_pos)
		dat = '%splot %s\n%s' % (h, ','.join(plots), s)
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
		self.gp.poll()
		if self.gp.returncode is None:	# make sure gnuplot is still running 
			try:
				self.gp.stdin.write(dat)
			except (IOError, ValueError):
				pass
		if filename:
			self.filename = filename
		return consumed

	def set_center_freq(self, f):
		self.center_freq = f

	def set_relative_freq(self, f):
		self.relative_freq = f

	def set_offset(self, f):
		self.offset_freq = f

	def set_width(self, w):
		self.width = w

	def set_logfile(self, logfile=None):
		self.logfile = logfile

class eye_sink_f(gr.sync_block):
    """
    """
    def __init__(self, debug = _def_debug, sps = _def_sps, plot_name = ""):
        gr.sync_block.__init__(self,
            name="eye_sink_f",
            in_sig=[np.float32],
            out_sig=None)
        self.debug = debug
        self.sps = sps * _def_sps_mult
        self.gnuplot = wrap_gp(sps=self.sps, plot_name=plot_name)

    def set_sps(self, sps):
        self.sps = sps * _def_sps_mult
        self.gnuplot.set_sps(self.sps)

    def work(self, input_items, output_items):
        in0 = input_items[0]
	consumed = self.gnuplot.plot(in0, 100 * self.sps, mode='eye')
        return consumed ### len(input_items[0])

    def kill(self):
        self.gnuplot.kill()

class constellation_sink_c(gr.sync_block):
    """
    """
    def __init__(self, debug = _def_debug, plot_name = ""):
        gr.sync_block.__init__(self,
            name="constellation_sink_c",
            in_sig=[np.complex64],
            out_sig=None)
        self.debug = debug
        self.gnuplot = wrap_gp(plot_name=plot_name)

    def work(self, input_items, output_items):
        in0 = input_items[0]
	self.gnuplot.plot(in0, 1000, mode='constellation')
        return len(input_items[0])

    def kill(self):
        self.gnuplot.kill()

class fft_sink_c(gr.sync_block):
    """
    """
    def __init__(self, debug = _def_debug, plot_name = ""):
        gr.sync_block.__init__(self,
            name="fft_sink_c",
            in_sig=[np.complex64],
            out_sig=None)
        self.debug = debug
        self.gnuplot = wrap_gp(plot_name=plot_name)
        self.next_due = time.time()

    def work(self, input_items, output_items):
<<<<<<< HEAD
        self.skip += 1
        if self.skip >= 50:
            self.skip = 0
=======
        if time.time() > self.next_due:
            self.next_due = time.time() + FFT_FREQ
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
            in0 = input_items[0]
	    self.gnuplot.plot(in0, FFT_BINS, mode='fft')
        return len(input_items[0])

    def kill(self):
        self.gnuplot.kill()

    def set_center_freq(self, f):
        self.gnuplot.set_center_freq(f)
	self.gnuplot.set_relative_freq(0.0)

    def set_relative_freq(self, f):
        self.gnuplot.set_relative_freq(f)

    def set_offset(self, f):
        self.gnuplot.set_offset(f)

    def set_width(self, w):
        self.gnuplot.set_width(w)

class mixer_sink_c(gr.sync_block):
    """
    """
<<<<<<< HEAD
    def __init__(self, debug = _def_debug):
=======
    def __init__(self, debug = _def_debug, plot_name = ""):
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
        gr.sync_block.__init__(self,
            name="mixer_sink_c",
            in_sig=[np.complex64],
            out_sig=None)
        self.debug = debug
<<<<<<< HEAD
        self.gnuplot = wrap_gp()
        self.skip = 0

    def work(self, input_items, output_items):
        self.skip += 1
        if self.skip >= 10:
            self.skip = 0
            in0 = input_items[0]
            self.gnuplot.plot(in0, FFT_BINS, mode='mixer')
=======
        self.gnuplot = wrap_gp(plot_name=plot_name)
        self.next_due = time.time()

    def work(self, input_items, output_items):
        if time.time() > self.next_due:
            self.next_due = time.time() + MIX_FREQ
            in0 = input_items[0]
	    self.gnuplot.plot(in0, FFT_BINS, mode='mixer')
>>>>>>> 1be5c53665b61077eeea558c0c35dfd45e773782
        return len(input_items[0])

    def kill(self):
        self.gnuplot.kill()

class symbol_sink_f(gr.sync_block):
    """
    """
    def __init__(self, debug = _def_debug, plot_name = ""):
        gr.sync_block.__init__(self,
            name="symbol_sink_f",
            in_sig=[np.float32],
            out_sig=None)
        self.debug = debug
        self.gnuplot = wrap_gp(plot_name=plot_name)

    def work(self, input_items, output_items):
        in0 = input_items[0]
	self.gnuplot.plot(in0, 2400, mode='symbol')
        return len(input_items[0])

    def kill(self):
        self.gnuplot.kill()

class float_sink_f(gr.sync_block):
    """
    """
    def __init__(self, debug = _def_debug):
        gr.sync_block.__init__(self,
            name="float_sink_f",
            in_sig=[np.float32],
            out_sig=None)
        self.debug = debug
        self.gnuplot = wrap_gp()

    def work(self, input_items, output_items):
        in0 = input_items[0]
        self.gnuplot.plot(in0, 2000, mode='float')
        return len(input_items[0])

    def kill(self):
        self.gnuplot.kill()
