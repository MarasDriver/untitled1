from __future__ import print_function
import datetime
import sys
import math
import time
import paragon as p
import Setup_Conifguration_file
import Telnet_OSACalibrationXML


sys.path.insert(0, 'C:/Users/marekk/Documents/Calnex/Paragon-X/RemoteControl/Python/')
measurement_time = 50
czas_przed = time.time()
teraz = datetime.datetime.now()
teraz = teraz.strftime("%d.%m.%Y %H.%M")
teraz = str(teraz)
destination = "D:/Robocze/P-X Automation/Results/"

# ścieżkaPDF = str(destination + teraz + " " + Setup_Conifguration_file.run.paragon_mediaType + " " + Setup_Conifguration_file.run.paragon_speed + r".pdf")
# ścieżkaCPD = str(destination + teraz + " " + Setup_Conifguration_file.run.paragon_mediaType + " " + Setup_Conifguration_file.run.paragon_speed + r".cpd")
# print(ścieżkaCPD + "\n" + ścieżkaPDF)
# paragon Config:
print(Setup_Conifguration_file.run.paragon_mediaType, Setup_Conifguration_file.run.paragon_speed)
teraz = datetime.datetime.now()
print("Running == 1, Paragon Configuration in progress...")
host = Setup_Conifguration_file.run.host
port = Setup_Conifguration_file.run.port
acc_port = Setup_Conifguration_file.run.acc_port
mediatype = Setup_Conifguration_file.run.mediatype
paragon_speed = Setup_Conifguration_file.run.paragon_speed
paragon_mediaType = Setup_Conifguration_file.run.paragon_mediaType
speed_Phy= Setup_Conifguration_file.run.speed_Phy
OSA_tested_speed= Setup_Conifguration_file.run.OSA_tested_speed
OSA_other_speed= Setup_Conifguration_file.run.OSA_other_speed


class paragon_config():
    def create_path(self):
        teraz = datetime.datetime.now()
        teraz = teraz.strftime("%d.%m.%Y %H.%M")
        teraz = str(teraz)
        global ścieżkaCPD, ścieżkaPDF
        ścieżkaCPD = str(destination + teraz + " " + Setup_Conifguration_file.run.paragon_mediaType + " " + Setup_Conifguration_file.run.paragon_speed + r".cpd")
        ścieżkaPDF = str(destination + teraz + " " + Setup_Conifguration_file.run.paragon_mediaType + " " + Setup_Conifguration_file.run.paragon_speed + r".pdf")
        # print(ścieżkaCPD + "\n" + ścieżkaPDF)
        print(ścieżkaPDF)
        return ścieżkaCPD, ścieżkaPDF

    def config_calibration(self):
        p.connect("10.12.152.3", "localhost", 9000, 9990)
        p.stopcapture()
        p.paragonset("SimulMeasImpairMode", "MEASUREONLY")
        p.paragonset("OperatingMode", "PTP")
        p.paragonset("MasterSlave Slave Enabled", "FALSE")
        p.paragonset("MasterSlave Enabled", "TRUE")
        p.paragonset("MasterSlave Enabled", "TRUE")
        p.paragonset("Physical LineInterface", Setup_Conifguration_file.run.paragon_mediaType)
        p.paragonset("Physical LineRate", Setup_Conifguration_file.run.paragon_speed)
        if Setup_Conifguration_file.run.paragon_speed == "10GBE":
            p.paragonset("Physical EthAutonegotiate", "TRUE")
        elif Setup_Conifguration_file.run.OSA_tested_speed == "100-full":
            p.paragonset("Physical EthAutonegotiate", "FALSE")
        else:
            p.paragonset("Physical EthAutonegotiate", "TRUE")
        p.paragonset("Physical RefClkSource", "EXT_10M")
        p.paragonset("Physical OnePpsRefPort", "R75_UNBAL")
        p.paragonset("MasterSlave Slave Enabled", "FALSE")
        p.paragonset("MasterSlave StandardsProfile", "G.8275.1_PHASE_PROFILE")
        p.paragonset("MasterSlave TestConfiguration", "MASTER_TEST")
        p.paragonset("MasterSlave Slave Enabled", "TRUE")
        p.paragonset("Capture OnePps WanderCaptEnable", "TRUE")
        p.paragonset("Capture OnePps AccuracyCaptEnable", "FALSE")
        p.paragonset("Capture OnePps WanderCaptEnable", "FALSE")
        teraz2 = time.time()
        time.sleep(5)
        p.starttimingcapture()
        Telnet_OSACalibrationXML.phy_Delays.jump_acc_port("jump")
        p.stopcapture()
        time.sleep(3)
        p.starttimingcapture()
        d = 0
        for i in range(Setup_Conifguration_file.run.iterations):
            d=d+1
            par.jumps_calibration(d)
        p.stopcapture()
        par.save_measurement()
        print("Whole measurement took exactly:",math.floor(time.time()-teraz2),"seconds.")

    def save_measurement(self):
        p.paragonset("Cat Show", "TRUE")
        p.paragonset("Cat", "1588TimeError")
        p.paragonset("Cat SelectSlot", "2Way")
        p.paragonset("Cat TIMEERROR ThresholdLimitEnabled", "False")
        p.paragonset("Cat Autoreload Force", "1")
        p.paragonset("Cat Autoreload Force", "1")
        p.paragonset("Cat Calculate", "1")
        # par=paragon_config.create_path("ścieżki")
        p.exportdata(ścieżkaCPD)
        p.paragonset("Cat GenerateReport True", ścieżkaPDF)
        p.paragonset("Cat", "Close")

    def jumps_calibration(self,d):
        print("***** ITERATION ***** (",d,"/",Setup_Conifguration_file.run.iterations,")")
        Telnet_OSACalibrationXML.phy_Delays.jump_acc_port("jump")


par = paragon_config()