# TimbreTranslation
This is was my thesis project at Reed college in which I designed and implemented a method to recognize timbre and apply that to another sound in sound files with only one instrument.

This program uses the library of sms-tools. I personally implemented `timbreTransfer.py` and `stftTransfer.py`. What this program does is takes two input files, donor and reciever, where donor is giving timbre (instrument) to the reciever. 
This is done through digital singal processing. 

Usage: 

'''
python timbreTranfer.py

'''

You can adjust the sound files and the level of transfer in the `timbreTransfer.py` file 
