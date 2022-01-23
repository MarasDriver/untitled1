from __future__ import print_function
import sys
import os
import time
import datetime

destination = "D:/Robocze/P-X Automation"

sys.path.insert(0, 'C:/Users/marekk/Documents/Calnex/Paragon-X/RemoteControl/Python/')
import paragon as p
d = datetime.datetime.now()

def prepare_results():
    print("Collecting results")
    time.sleep(2)
    p.paragonset("Cat", "SyncE")
    time.sleep(3)

h=70

try:
    os.startfile("C:/Users/marekk/Desktop/Paragon-X.lnk")
    p.connect("10.12.6.3", "localhost", 9000, 9990)
except:
    print("\nCould Not Connect to Paragon Instrument. Exiting")
    exit()

try:

    #########  Przygotowanie Paragona ##########
    p.paragonset("SimulMeasImpairMode", "MEASUREONLY")
    print("SimulMeasImpairMode, MEASUREONLY")
    p.paragonset("OperatingMode", "SYNCE")
    print("OperatingMode", "SYNCE")
    p.paragonset("TxRxMode", "TRUE")
    print("TxRxMode", "TRUE")
    p.paragonset("Physical Coupled", "TRUE")
    print("Physical Coupled", "TRUE")
    p.paragonset("Physical EthSyncEClock", "FALSE")
    print("Physical EthSyncEClock", "FALSE")
    p.paragonset("Physical LineRate", "1GBE")
    print("Physical LineRate", "1GBE")
    p.paragonset("Physical LineInterface", "OPTICAL")
    print("Physical LineInterface", "OPTICAL")
    p.paragonset("Physical EthAutonegotiate", "TRUE")
    print("Physical EthAutonegotiate", "TRUE")
    p.paragonset("Physical RefClkSource", "EXT_R75_E1")
    print("Physical RefClkSource", "EXT_R75_E1")
    p.paragonset("Capture SyncE WanderCaptEnable", "TRUE")
    print("Capture SyncE WanderCaptEnable", "TRUE")
    p.paragonset("Capture Pdh T1WanderCaptEnable", "FALSE")
    print("Capture Pdh T1WanderCaptEnable", "FALSE")
    p.paragonset("Capture Pdh E1WanderCaptEnable", "FALSE")
    print("Capture Pdh E1WanderCaptEnable", "FALSE")
    p.paragonset("Capture Pdh M2WanderCaptEnable", "FALSE")
    print("Capture Pdh M2WanderCaptEnable", "FALSE")
    p.paragonset("Capture OnePps AccuracyCaptEnable", "FALSE")
    print("Capture OnePps AccuracyCaptEnable", "FALSE")
    p.paragonset("Capture OnePps WanderCaptEnable", "FALSE")
    print("Capture OnePps WanderCaptEnable", "FALSE")
    p.paragonset("Capture Control Mode", "FIXED")
    print("Capture Control Mode", "FIXED")

    ###### Oczekiwanie na ustabilizowanie referencji ###
    ###### Pomiar 1 minuta  ####
    p.paragonset("Capture Control FixedPeriod", "1MIN")
    print("Capture Control FixedPeriod", "60 SECS")
    p.paragonset("Capture SyncE MeasurementPort", "PORT1")
    print("Test, 1 minute measurement", "PORT 1")
    p.starttimingcapture()
    print("Waiting.")
    time.sleep(51)
    print("Waiting..")
    time.sleep(5)
    print("Waiting...")
    time.sleep(5)

    ### Rozpoczęcie pierwszego pomiaru ###

    print("Test Finished, proceeding to perform 1 Hour G.8262 Frequency Accuracy test on Port1")
    p.stopcapture()
    time.sleep(1)
    print("Capture Stopped")
    p.paragonset("Capture Control FixedPeriod", "1HOUR")
    print("Capture Control FixedPeriod", "1 HOUR")
    print(d.strftime("Start Time: %H:%M:%S %d.%b.%Y"))
    p.starttimingcapture()
    print("Start Capture")
    time.sleep(h+20)
    p.stopcapture()
    time.sleep(2)
    print("Capture Stopped")
    p.exportdata(str(destination+r"/Frequency Accuracy Port1.cpd"))
    print("Saving first measurement")

    p.paragonset("Cat", "SyncE")
    p.paragonset("Cat Show", "TRUE")
    p.paragonset("Cat MTIE Enable", "True")

    ### Bez maski ###

    #p.paragonset("Cat MTIE Mask ", "G.8262 EEC Opt. 1 Wander Gen Const. Temp.")

    ##################

    p.paragonset("Cat Calculate", "1")
    p.paragonset("Cat GenerateReport True ",destination+r"/Frequency Accuracy Port1.pdf")

    ### Zapiasnie wyników pierwszego pomiaru ###
    ### Rozpoczęcie drugiego pomiaru ###

    p.paragonset("Capture SyncE MeasurementPort", "PORT2")
    print("Port under measurement changed from port 1 to port 2")
    print("Waiting...")
    time.sleep(5)
    print("Proceeding to perform 1 Hour G.8262 Frequency Accuracy test on Port2")
    print(d.strftime("Start Time: %H:%M:%S %d.%b.%Y"))
    p.starttimingcapture()
    print("Start Capture")
    time.sleep(h+20)
    p.stopcapture()
    time.sleep(2)
    print("Capture Stopped")
    p.exportdata(str(destination+r"/Frequency Accuracy Port2.cpd"))
    print("Saving second measurement")

    p.paragonset("Cat", "SyncE")
    p.paragonset("Cat Show", "TRUE")
    p.paragonset("Cat MTIE Enable", "True")
    ### Bez maski ###

    # p.paragonset("Cat MTIE Mask ", "G.8262 EEC Opt. 1 Wander Gen Const. Temp.")

    ##################


    p.paragonset("Cat Calculate", "1")
    p.paragonset("Cat GenerateReport True ", destination+"/Frequency Accuracy Port2.pdf")

    ### Zapiasnie wyników drugiego pomiaru ###

    p.paragonset("Cat", "Close")
except Exception as e:
    print("\nError on line " + str(sys.exc_info()[2].tb_lineno) + ", Processing Command: \n" + e.args[0] + "\nExiting")
p.disconnect()
