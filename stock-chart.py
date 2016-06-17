#!/usr/bin/env python

import sys 

import matplotlib
#matplotlib.use('TkAgg')
from pylab import rcParams
rcParams['figure.figsize'] = 21, 7
import argparse
import matplotlib.pyplot as plt
import numpy as np
import urllib
import urllib2
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import style
from matplotlib.finance import candlestick_ohlc

def moving_average(values, window):
	weights = np.repeat(1.0, window) / window
	smas = np.convolve(values, weights, 'valid')
	return smas

def bytespdate2num(fmt, encoding):
	strconverter = mdates.strpdate2num(fmt)
	def bytesconverter(b):
		s = b.decode(encoding)
		return strconverter(s)
	return bytesconverter	

def graph_data():
	fig = plt.figure(facecolor='#f0f0f0')  
	ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1) 
	plt.ylabel('Vol x 1e6')
	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1, sharex=ax3)
	plt.title("Exchange: " + ecode + "\nStock Code: " + scode)
	plt.ylabel('MAvgs')
	ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1, sharex=ax3)
	plt.ylabel('Price')
	
	stock_price_url		 = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + scode + ecode + \
							  '/chartdata;type=quote;range=' + ctime + chartperiod + '/csv'
	#print stock_price_url
	source_code_req		 = urllib2.Request(stock_price_url) 
	source_code_response = urllib2.urlopen(source_code_req) 
	source_code			 = source_code_response.read().decode()
	stock_data			 = []
	split_source		 = source_code.split('\n')

	for line in split_source:

		split_line = line.split(',')
		if len(split_line) == 6:

			if 'values' not in line and 'labels' not in line:
				stock_data.append(line)

	date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
														  delimiter=',',
														  unpack=True,
														  converters={0: bytespdate2num('%Y%m%d', 'utf-8')})
														  
	volume = volume / 1e6
		
	for label in ax2.xaxis.get_ticklabels():
		label.set_rotation(45)
		
	x = 0
	y = len(date)
	ohlc = []

	while x < y:
		append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
		ohlc.append(append_me)
		x+=1		
	
	ma1 = moving_average(closep,MA1)
	ma2 = moving_average(closep,MA2)
	
	start = len(date[MA2-1:])
	
	ax1.plot(date[-start:], ma1[-start:], linewidth=2, label=(str(MA1)+'MA'))
	ax1.plot(date[-start:], ma2[-start:], linewidth=2, label=(str(MA2)+'MA'))
	ax1.fill_between(date[-start:], ma2[-start:], ma1[-start:],
					 where=(ma1[-start:] < ma2[-start:]),
					 facecolor='r', edgecolor='r', alpha=0.5)

	ax1.fill_between(date[-start:], ma2[-start:], ma1[-start:],
					 where=(ma1[-start:] > ma2[-start:]),
					 facecolor='g', edgecolor='g', alpha=0.5)
	ax1.grid(True, color='grey', linestyle='-', linewidth=1)
	ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='lower'))
	
	candlestick_ohlc(ax2, ohlc[-start:], width=0.4, colorup='#77d879', colordown='#db3f3f')
	ax2.grid(True, color='grey', linestyle='-', linewidth=1)
	ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=7, prune='lower'))  
	bbox_props = dict(boxstyle='round',fc='w', ec='k',lw=1)
	
	ax2.annotate(str(closep[-1]), (date[-1], closep[-1]),
				 xytext = (date[-1]+4, closep[-1]), bbox=bbox_props)  
 
	ax3.fill_between(date[-start:], 0, volume[-start:], facecolor='b', edgecolor='b', alpha=0.5)	
	for label in ax3.xaxis.get_ticklabels():
		label.set_rotation(45)
	ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))
	ax3.grid(True, color='grey', linestyle='-', linewidth=1)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y')) 
	ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))

	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.subplots_adjust(left=0.06, bottom=0.18, right=0.94, top=0.85, wspace=0.2, hspace=0)
	ax1.legend()  
	leg = ax1.legend(loc=9, ncol=2,prop={'size':11})
	leg.get_frame().set_alpha(0.4)
	matplotlib.rc('font', **font)  
	fn = '/var/www/html/stock-chart/images/' + outfn	

	fig.savefig(fn, facecolor=fig.get_facecolor())
	
# Main

parser = argparse.ArgumentParser()
parser.add_argument("-f",  "--outfile"	   	,  default="test.png",  help="the output filename")
parser.add_argument("-e",  "--exchangecode" ,  default="AX"	     , 	help="the stock exchange code")
parser.add_argument("-s",  "--stockcode"	,  default="NAB"	 , 	help="the stock code")
parser.add_argument("-t",  "--charttime"	,  default="1"	   	 , 	help="length of time period back the chart goes")
parser.add_argument("-u",  "--chartperiod"  ,  default="y"	   	 , 	help="unit of length of time period back the chart goes")
args = parser.parse_args()

style.use('fivethirtyeight')
MA1 = 10
MA2 = 30

font = \
{
	'family' : 'normal',
	'weight' : 'bold',
	'size'   : 12
}

outfn   			= args.outfile
ecode			   	= args.exchangecode
scode			   	= args.stockcode
ctime			   	= args.charttime
chartperiod			= args.chartperiod

if ecode == "NYSE":
	ecode = ''
else:
	ecode = "." + ecode

graph_data()
