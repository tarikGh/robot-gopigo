#!/usr/bin/python

from gopigo import * #Has the basic functions for controlling the GoPiGo Robot

import time;
import sys, select, os	#Used for closing the running programimport sys
import time
import atexit
atexit.register(stop)

global sp

#Write in file
def write_data(spleft,spright):
    global sec1,sec2,Nbrmesure
    Nbrmesure=0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print "I'm doing stuff. Press Enter to stop me! and change speed "
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            #line = raw_input()
            stop()
            break

        val0=enc_read(0)	#en cm
        val1=enc_read(1)	#en cm

        if spleft >255:
            spleft =255
        elif spleft <0:
            spleft =0

        if spright >255:
            spright =255
        elif spright <0:
            spright =0

        f.write( str(spleft)  )
        f.write("\t")
        f.write( str(spright)  )
        f.write("\t")
        f.write( str(val0)  )      # str() converts to string
        f.write("\t")
        f.write(str(val1)  )      # str() converts to string
        f.write("\n")
        Nbrmesure=Nbrmesure+1

f1 =open("dataWithPID.txt", "a+")
f2 =open("dataWithoutPID.txt", "a+")
f1.write("CmdVMg\tCmdVMd\tM1\tM2\n")
f2.write("CmdVMg\tCmdVMd\tM1\tM2\n")


while True:
	print "This is a  example for the GoPiGo Robot read and save data in file\n"
	print "Press:\n\tp: Move With PID \n\tb:Move without PID\n",
	print "Enter the Command:",
	a=raw_input()   # Fetch the input from the terminal
	if a=='p':
		#f = open("dataWithPID.txt", "a+")# save data in PID File
		f=f1
		pid=1
	if a=='b':
		#f = open("dataWithoutPID.txt", "a+")# save data in file  without PID
		f=f2
		pid=0

	print "Enter la Commande du vitesse moteur left :\n",
	spleft=raw_input()   # Fetch the input from the terminal
	spleft=int(spleft)
	print "Enter la Commande du vitesse moteur Right :\n",
	spright=raw_input()   # Fetch the input from the terminal
	spright=int(spright)

	set_left_speed(spleft)
	set_right_speed(spright)


	localtime = time.localtime(time.time())
	sec1=localtime.tm_sec
	if pid==0:
		motor_fwd()# sans PID
	else:
		fwd()# avec PID

	time.sleep(1)
	print read_motor_speed()
	time.sleep(1)


	#set_left_speed(10)
	#time.sleep(5)

	write_data(spleft,spright)

	localtime = time.localtime(time.time())
	sec2=localtime.tm_sec
	Duree=sec2-sec1
	f.write("temps (s):\t")
	f.write(str(Duree))
	f.write("\n echantillonage (s):\t")
	echanti=Duree/Nbrmesure
	f.write(str(echanti))

f.close()
