#!/usr/bin/env python

# Spikemark Listener
# Receives and displays position information sent by Creative Conners Spikemark scenic automation software
# Author: John Musarra
# Copyright 2016 John Musarra

# TODO: Add multicast listening


import Tkinter
import socket
import re

def createSpikeList():
	spikes = {}
	for spike in range(1,8):
		spikes[spike] = {}
	# import spike information from xml showfile, manual for now
	spikes[1]['name'], spikes[1]['position'] = "NEAR EOT", 140
	spikes[2]['name'], spikes[2]['position'] = "LEVIS PICKUP", 142.65
	spikes[3]['name'], spikes[3]['position'] = "YAGO PICKUP", 180.83
	spikes[4]['name'], spikes[4]['position'] = "LEVIS PRE", 193.56
	spikes[5]['name'], spikes[5]['position'] = "LEVIS ONSTAGE", 503.7
	spikes[6]['name'], spikes[6]['position'] = "YAGO ONSTAGE", 812.86
	spikes[7]['name'], spikes[7]['position'] = "FAR EOT", 860
	return spikes


position = 0

UDP_IP = "0.0.0.0"
UDP_PORT = 3040
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


root = Tkinter.Tk()
root.title("Spikemark Listener")
root.geometry("600x225+450+100")
bgImage=Tkinter.PhotoImage(file="darkCheckerBG.gif")
lblBG=Tkinter.Label(root,image = bgImage)
lblBG.place(x=0, y=0, relwidth=1, relheight=1)

spikes = createSpikeList()
print spikes

machineName=Tkinter.StringVar()
pos = Tkinter.StringVar()
machineName.set("waiting for data...")
pos.set("Waiting for data....")


lblPosCounter = Tkinter.Label(root, textvariable=pos, image=bgImage, compound="center", height="90", width="400", fg="white", padx=20, font=("Consolas", 120))
lblPosCounter.grid(row=4, column=1, rowspan=5)
lblMachineName = Tkinter.Label(root, textvariable=machineName, bg="#2d2d2d",  fg="white", font=("Consolas", 24))
lblMachineName.grid(row=2, column=1)
lblSpike1 = Tkinter.Label(root, text=spikes[1]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike1.grid(row=1, column=2, sticky='e')
lblSpike2 = Tkinter.Label(root, text=spikes[2]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike2.grid(row=2, column=2, sticky='e')
lblSpike3 = Tkinter.Label(root, text=spikes[3]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike3.grid(row=4, column=2, sticky='e')
lblSpike4 = Tkinter.Label(root, text=spikes[4]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike4.grid(row=5, column=2, sticky='e')
lblSpike5 = Tkinter.Label(root, text=spikes[5]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike5.grid(row=6, column=2, sticky='e')
lblSpike6 = Tkinter.Label(root, text=spikes[6]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike6.grid(row=7, column=2, sticky='e')
lblSpike7 = Tkinter.Label(root, text=spikes[7]['name'], bg="black",  fg="white", font=("Consolas", 18))
lblSpike7.grid(row=8, column=2, sticky='e')


def listen():              # receives Watchout feedback from Spikemark, parse into machine name and position data
	global position        # TODO: add error handling if no connection
	global machineName
	spikemarkData, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	dataSplit = re.split('"', spikemarkData)
	position = format(float(dataSplit[2]), '.2f')
	machineName.set(dataSplit[1])
	pos.set(position)
	root.after(50, listen)

def allLabelsWhite():                          # TODO: pull label names from iterable
	lblSpike1.configure(fg="white")
	lblSpike2.configure(fg="white")
	lblSpike3.configure(fg="white")
	lblSpike4.configure(fg="white")
	lblSpike5.configure(fg="white")
	lblSpike6.configure(fg="white")
	lblSpike7.configure(fg="white")


def indicateProximity():       # changes color of spike text labels based on current position
	p=float(position)          # TODO: take position range from spikes[].position values +1 and -1 inch
	if p <= 130:
		lblSpike1.configure(fg="red")   # near end of travel - less than 150"
	elif 141.65 <= p <= 143.65:
		lblSpike2.configure(fg="green") # Levis pickup - 142.65"
	elif 179.91 <= p <= 181.91:
		lblSpike3.configure(fg="green") # Yago pickup - 180.91"
	elif 192.56 <= p <= 194.56:
		lblSpike4.configure(fg="green") # Levi's Pre - 193.56
	elif 502.7 <= p <= 504.7:
		lblSpike5.configure(fg="green") # Levi's onstage - 503.7"
	elif 811.86 <= p <= 813.16:
		lblSpike6.configure(fg="green") # Yago onstage - 812.86"
	elif p > 860:
		lblSpike7.configure(fg="red")   # far end of travel - greater than 860"
	else:
		allLabelsWhite()	
	root.after(250, indicateProximity)	


def printDebug():
	print position
	print str(machineName)         #is a Tkinter StringVar, so stringify for printing... which doesn't work either FIXME
	root.after(5000, printDebug)



root.after(40, listen)
root.after(250, indicateProximity)
#root.after(5000, printDebug)
root.mainloop()


#setInput "N" 180.082123160924 








