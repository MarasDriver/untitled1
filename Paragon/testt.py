from __future__ import print_function
import sys
import time

sys.path.insert(0, 'C:/Users/marekk/Documents/Calnex/Paragon-X/RemoteControl/Python/')

import paragon as p





try:
    p.connect("10.12.6.3", "localhost", 9000, 9990)
except:
    print("\nCould Not Connect to Paragon Instrument. Exiting")
    exit()

try:
    p.paragonset("Cat", "SyncE")
    p.paragonset("Cat Show", "TRUE")
    p.paragonset("Cat MTIE Enable", "True")
    p.paragonset("Cat MTIE Mask ", "G.8262 EEC Opt. 1 Wander Gen Const. Temp.")
    p.paragonset("Cat Calculate", "1")
    p.paragonset("Cat GenerateReport True ","C:/Users/marekk/Documents/Calnex/CAT/Reports/Wandertest.pdf")



except Exception as e:
    print("\nError on line " + str(sys.exc_info()[2].tb_lineno) + ", Processing Command: \n" + e.args[0] + "\nExiting")

p.disconnect()
