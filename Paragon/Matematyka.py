import linecache
import math
RxandTx=[]
Mean_val=[]
names={("t1Time.txt", 'Measurements t1Time.txt'), ("t4Time.txt", 'Measurements t4Time.txt'), ("2WayTime.txt", 'Measurements 2WayTime.txt'), ("t1Filt.txt", 'Measurements t1Filt.txt'), ("t4Filt.txt", 'Measurements t4Filt.txt'),("2WayFilt.txt", 'Measurements 2WayFilt.txt')}
class klasa_Matematyka():
    def getRxandTx(self):
        zapisz = open("RxandTx.txt", "a+")

        Rx = linecache.getline("RxandTx.txt", 1)
        Tx = linecache.getline("RxandTx.txt", 2)
        zapisz.close()
        Rx=Rx.strip("\n")
        Tx =Tx.strip("\n")
        Rx = Rx.strip("")
        Tx = Tx.strip("")
        Rx=int(Rx)
        Tx=int(Tx)
        klasa_Matematyka.matma("1",Rx,Tx)
        return Rx,Tx,RxandTx

    def matma(self,Rx,Tx):
        global Mean_val
        Mean_val = []
        for plik1, plik2 in names:
            # print("Otwieram plik o nazwie: ", plik1)
            cala_strona2 = open(plik1, "r")
            whole_file2 = cala_strona2.readlines()
            min = float(whole_file2[2][4:-3])
            max = float(whole_file2[3][4:-3])
            mean = float(whole_file2[1][4:-3])
            math.floor(mean)
            mean = int(mean)
            if plik2 == 'Measurements t1Time.txt':
                newTx = Tx - mean
            elif plik2 == 'Measurements t4Time.txt':
                newRx = Rx + mean
            elif plik2 == 'Measurements 2WayTime.txt':
                Mean_val = []
                Mean_val.append(mean)
                # print("MeanVal[0]:",Mean_val[0])
        # print("NewRx=", newRx, "NewTx=", newTx)
        print("OLD RX,TX:", Rx, Tx, "Mean value:", Mean_val[0])
        zapisz = open("New_RxandTx.txt", "w+")
        nowy_wynik = str(newRx) + "\r" + str(newTx) + "\r" + str(Mean_val[0])
        zapisz.write(nowy_wynik)
        zapisz.close()
        return newRx,newTx,Mean_val,mean
#
licz=klasa_Matematyka()
klasa_Matematyka.getRxandTx("1")

