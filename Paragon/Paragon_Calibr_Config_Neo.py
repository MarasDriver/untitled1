import paramiko
import time
import Setup_Conifguration_file
import linecache
RxandTx=[]

class telnet_Calibration_file_operation():
    def open_calibration_file(device,host,port):
        print(f"Logging into Host: "+host+" on Port:",port)
        user="root"
        Password="ChgMeNOW"
        client= telnetlib.Telnet()
        client.open(host, port, 5)
        client.exec_command('\r'.encode('ascii'))
        client.read_until(b'Login')
        client.exec_command(user.encode('ascii'))
        client.read_until(b'root')
        client.exec_command(b'\r')
        client.exec_command(b'\x0D')
        time.sleep(2)
        client.read_until(b"Password:")
        client.exec_command('ChgMeNOW'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('con sys'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('Qdebug Udebug arris0123'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('cd ..'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('cd etc'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command(("vim osa"+device+"_calibration.xml").encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(1)
        i=0
        while i<90:
            client.exec_command('\n'.encode('ascii'))
            i=i+1
        z_xmla = client.read_until(b"</resources>")
        z_xmla=str(z_xmla)
        zapisz = open("xml_kalibracyjny.txt", "w+")
        zapisz.write(z_xmla)
        client.exec_command(':qa!'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('exit'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)
        client.exec_command('logout'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
        time.sleep(2)

class phy_Delays():
    def getPhyDelays(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print(f"Logging into Host: "+host)
        user="root"
        Password="ChgMeNOW"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=Password)

        client.exec_command(user.encode('ascii'))
        client.exec_command(Password.encode('ascii'))
        client.exec_command('con sys'.encode('ascii'))
        client.exec_command('Qdebug Udebug arris0123'.encode('ascii'))
        client.exec_command('devTools-dc'.encode('ascii'))
        client.exec_command('con hal 2'.encode('ascii'))
        client.exec_command('fpgadebug'.encode('ascii'))
        getphy_command = "getPhyDelays " + str(mediatype) + " " + str(speed_Phy) + " " + str(acc_port)
        client.exec_command((str(getphy_command)).encode('ascii'))
        z_PhyDelays=z_PhyDelays[135:170]
        zPHyDelays_rx = z_PhyDelays[:20]
        zPHyDelays_tx = z_PhyDelays[20:]
        zPHyDelays_rx=str(zPHyDelays_rx)
        zPHyDelays_tx=str(zPHyDelays_tx)

        zapisz = open("z_PhyDelays.txt", "w+")
        z_PhyDelays2=zPHyDelays_rx+"\r"+zPHyDelays_tx
        # print(z_PhyDelays2)
        zapisz.write(z_PhyDelays2)
        client.exec_command('exit'.encode('ascii'))

        client.exec_command('exit'.encode('ascii'))

        client.exec_command('logout'.encode('ascii'))
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
        client.close()
        time.sleep(2)


    def setDelays(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print(f"Logging into Host: " + host + " on Port:", port)
        user = "root"
        Password = "ChgMeNOW"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=Password)

        client.exec_command(user.encode('ascii'))
        client.exec_command(Password.encode('ascii'))
        client.exec_command('con sys'.encode('ascii'))
        client.exec_command('Qdebug Udebug arris0123'.encode('ascii'))
        client.exec_command('devTools-dc'.encode('ascii'))
        client.exec_command('con hal 2'.encode('ascii'))
        client.exec_command('fpgadebug'.encode('ascii'))
        client.exec_command('\r'.encode('ascii'))
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
        client.exec_command((str(getphy_command)).encode('ascii'))
        client.exec_command('exit'.encode('ascii'))
        client.exec_command('exit'.encode('ascii'))
        client.exec_command('logout'.encode('ascii'))
        client.close()
        time.sleep(2)


    def jump_acc_port(self, host=Setup_Conifguration_file.run.host, port=Setup_Conifguration_file.run.port, acc_port=Setup_Conifguration_file.run.acc_port, mediatype=Setup_Conifguration_file.run.mediatype, speed_Phy=Setup_Conifguration_file.run.speed_Phy):
        print("Restart Access Port:",acc_port,"Logging into Host: " + host + " on Port:", port)
        user = "root"
        Password = "ChgMeNOW"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(host, disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})
        client.connect(host, username=user, password=Password)


        client.exec_command(user.encode('ascii'))
        client.exec_command(Password.encode('ascii'))
        client.exec_command('network-element ne-1'.encode('ascii'))
        client.exec_command('conf nte nte'.encode('ascii'))
        acc_port_str=str(acc_port)
        conf_acc_port=str("conf access-port access-1-1-1-"+acc_port_str)
        client.exec_command(conf_acc_port.encode('ascii'))
        client.exec_command('admin-state unassigned'.encode('ascii'))
        other_speed=str(Setup_Conifguration_file.run.OSA_other_speed)
        tested_speed = str(Setup_Conifguration_file.run.OSA_tested_speed)
        speed_to_set=str('speed '+other_speed)
        client.exec_command(speed_to_set.encode('ascii'))
        speed_to_set = str('speed '+tested_speed)
        client.exec_command(speed_to_set.encode('ascii'))
        client.exec_command('admin-state in-service'.encode('ascii'))
        client.exec_command('logout'.encode('ascii'))
        client.close()
        time.sleep(2)



asd=phy_Delays()
asd.getPhyDelays()
asd.jump_acc_port()