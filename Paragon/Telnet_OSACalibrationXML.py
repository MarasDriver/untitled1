import telnetlib
import time
import Setup_Conifguration_file
import linecache
RxandTx=[]

class telnet_Calibration_file_operation():
    def open_calibration_file(device,host,port):
        print(f"Logging into Host: "+host+" on Port:",port)
        user="root"
        Password="ChgMeNOW"
        tn = telnetlib.Telnet()
        tn.open(host, port, 5)
        tn.write('\r'.encode('ascii'))
        tn.read_until(b'Login')
        tn.write(user.encode('ascii'))
        tn.read_until(b'root')
        tn.write(b'\r')
        tn.write(b'\x0D')
        time.sleep(2)
        tn.read_until(b"Password:")
        tn.write('ChgMeNOW'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('con sys'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('Qdebug Udebug arris0123'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('cd ..'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('cd etc'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write(("vim osa"+device+"_calibration.xml").encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(1)
        i=0
        while i<90:
            tn.write('\n'.encode('ascii'))
            i=i+1
        z_xmla = tn.read_until(b"</resources>")
        z_xmla=str(z_xmla)
        zapisz = open("xml_kalibracyjny.txt", "w+")
        zapisz.write(z_xmla)
        tn.write(':qa!'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('exit'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('logout'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)

class phy_Delays():
    def getPhyDelays(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print(f"Logging into Host: "+host+" on Port:",port)
        user="root"
        Password="ChgMeNOW"
        tn = telnetlib.Telnet()
        tn.open(host, port, 5)
        tn.write('\r'.encode('ascii'))
        tn.read_until(b'Login:')
        tn.write(user.encode('ascii'))
        tn.read_until(b'root')
        tn.write(b'\r')
        tn.write(b'\x0D')
        time.sleep(2)
        tn.read_until(b"Password:")
        tn.write(Password.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('con sys'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('Qdebug Udebug arris0123'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('devTools-dc'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('con hal 2'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(4)
        tn.write('fpgadebug'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        values=tn.read_until(b"fpgadebug")
        getphy_command = "getPhyDelays " + str(mediatype) + " " + str(speed_Phy) + " " + str(acc_port)
        tn.write((str(getphy_command)).encode('ascii'))
        tn.write('\r'.encode('ascii'))
        z_PhyDelays = tn.read_until(b"lPortIdx")
        # print(z_PhyDelays)
        # print(len(z_PhyDelays))
        z_PhyDelays=z_PhyDelays[135:170]
        # print(z_PhyDelays)
        # print(len(z_PhyDelays))
        zPHyDelays_rx = z_PhyDelays[:20]
        zPHyDelays_tx = z_PhyDelays[20:]
        zPHyDelays_rx=str(zPHyDelays_rx)
        zPHyDelays_tx=str(zPHyDelays_tx)

        zapisz = open("z_PhyDelays.txt", "w+")
        z_PhyDelays2=zPHyDelays_rx+"\r"+zPHyDelays_tx
        # print(z_PhyDelays2)
        zapisz.write(z_PhyDelays2)
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('exit'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(3)
        tn.write('exit'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        # system_prompt = tn.read_until(b'] # exit')
        system_prompt = tn.read_until(b'Adtran:system-->')

        tn.write('logout'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        logout = tn.read_until(b'logout')
        while "logout" not in str(logout):
            tn.write('logout'.encode('ascii'))
            tn.write('\r'.encode('ascii'))
            time.sleep(1)
            logout = tn.read_until(b'logout')

        zPHyDelays_rx=zPHyDelays_rx
        zPHyDelays_tx=zPHyDelays_tx
        RxandTx=[]
        RxNumbers = []
        TxNumbers = []
        # print(RxandTx)
        Rx = 0
        Tx = 0
        for char in zPHyDelays_rx:
            # print(char)
            if char.isdigit():
                RxNumbers.append(int(char))
        for char in zPHyDelays_tx:
            if char.isdigit():
                TxNumbers.append(int(char))
        for char in RxNumbers:
            Rx = Rx * 10 + char
        RxandTx.append(int(Rx))
        for char in TxNumbers:
            Tx = Tx * 10 + char
        RxandTx.append(int(Tx))
        zapisz = open("RxandTx.txt", "w+")
        RxandTx = str(Rx)+"\n"+str(Tx)
        zapisz.write(RxandTx)
        print("Rx in XML was equal to:", Rx, ", and Tx in XML was equal to:", Tx)
        RxandTx = [Rx,Tx]
        # print(RxandTx)
        return Rx, Tx,RxandTx


    def setDelays(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print(f"Logging into Host: " + host + " on Port:", port)
        user = "root"
        Password = "ChgMeNOW"
        tn = telnetlib.Telnet()
        tn.open(host, port, 5)
        tn.write('\r'.encode('ascii'))
        tn.read_until(b'Login:')
        tn.write(user.encode('ascii'))
        tn.read_until(b'root')
        tn.write(b'\r')
        tn.write(b'\x0D')
        time.sleep(2)
        tn.read_until(b"Password:")
        tn.write(Password.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('con sys'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('Qdebug Udebug arris0123'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('devTools-dc'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('con hal 2'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(4)
        tn.write('\r'.encode('ascii'))
        tn.write('fpgadebug'.encode('ascii'))
        tn.write('\r'.encode('ascii'))

        values = tn.read_until(b"fpgadebug")
        plik="New_RxandTx.txt"
        zapisz = open(plik, "a+")
        newRx = linecache.getline(plik, 1)
        newTx = linecache.getline(plik, 2)
        zapisz.close()
        newRx = newRx.strip("\n")
        newTx = newTx.strip("\n")
        newRx = newRx.strip("")
        newTx = newTx.strip("")
        newRx = int(newRx)
        newTx = int(newTx)
        print("NewRx =", newRx, "NewTx =", newTx)
        getphy_command = "setPhyDelays " + str(mediatype) + " " + str(speed_Phy) + " " + str(newRx)+ " " + str(newTx)+ " " + str(acc_port)
        tn.write((str(getphy_command)).encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('exit'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(3)
        tn.write('exit'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(4)
        # system_prompt = tn.read_until(b'] # exit')
        system_prompt = tn.read_until(b'Adtran:system-->')
        tn.write('logout'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        logout = tn.read_until(b'logout')
        while "logout" not in str(logout):
            tn.write('logout'.encode('ascii'))
            tn.write('\r'.encode('ascii'))
            time.sleep(1)
            logout = tn.read_until(b'logout')

    def jump_acc_port(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print("Restart Access Port:",acc_port,"Logging into Host: " + host + " on Port:", port)
        user = "root"
        Password = "ChgMeNOW"
        tn = telnetlib.Telnet()
        tn.open(host, port, 5)
        tn.write('\r'.encode('ascii'))
        tn.read_until(b'Login:')
        tn.write(user.encode('ascii'))
        tn.read_until(b'root')
        tn.write(b'\r')
        tn.write(b'\x0D')
        time.sleep(2)
        tn.read_until(b"Password:")
        tn.write(Password.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('network-element ne-1'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('conf nte nte'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        acc_port_str=str(acc_port)
        conf_acc_port=str("conf access-port access-1-1-1-"+acc_port_str)
        tn.write(conf_acc_port.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        tn.write('admin-state unassigned'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        other_speed=str(Setup_Conifguration_file.run.OSA_other_speed)
        tested_speed = str(Setup_Conifguration_file.run.OSA_tested_speed)
        speed_to_set=str('speed '+other_speed)
        tn.write(speed_to_set.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(5)
        speed_to_set = str('speed '+tested_speed)
        tn.write(speed_to_set.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(5)
        tn.write('admin-state in-service'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        time.sleep(2)
        # tn.write('show access-port'.encode('ascii'))
        # tn.write('\r'.encode('ascii'))
        # time.sleep(2)
        stan=""
        while "normal" not in str(stan):
            tn.write('show access-port'.encode('ascii'))
            time.sleep(1)
            for i in range(14):
                tn.write('\n'.encode('ascii'))
                time.sleep(0.5)
            stan = tn.read_until(b' Operational State : ')
            stan=tn.read_until(b'Secondary States :')
            # print(stan)
        tn.write('logout'.encode('ascii'))
        tn.write('\r'.encode('ascii'))
        access = tn.read_until(b'access-1-1')
        logout = tn.read_until(b'logout')
        while "logout" not in str(logout):
            tn.write('logout'.encode('ascii'))
            tn.write('\r'.encode('ascii'))
            time.sleep(1)
            logout = tn.read_until(b'logout')