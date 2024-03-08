import PyPDF2
import Paragon_Calibr_Config

# strony = [2, 5, 8, 3, 6, 9]
lista = ["t1Time.txt", "t4Time.txt", "2WayTime.txt", "t1Filt.txt", "t4Filt.txt", "2WayFilt.txt"]
numbers = {("t1Time.txt", 2), ("t4Time.txt", 5), ("2WayTime.txt", 8), ("t1Filt.txt", 3), ("t4Filt.txt", 6),
           ("2WayFilt.txt", 9)}

class klasa_readPDF():
    def czytaj(self):
        # print("Ścieżka z której czytam PDF:", Paragon_Calibr_Config.ścieżkaPDF)
        reader = PyPDF2.PdfReader(Paragon_Calibr_Config.ścieżkaPDF)
        # print(reader,Paragon_Calibr_Config.ścieżkaPDF)
        # reader=PyPDF2.PdfReader("D:/Robocze/P-X Automation/Results/16.01.2024 10.29 ELECTRICAL 1GBE.pdf")
        for key, e in numbers:
            # print(e)
            eeee = reader.pages[e].extract_text()
            # print(eeee)
            if e in [2, 5]:
                a1 = eeee.split("Include Correction Field On", 1)[0]
                a1 = a1[:19]
                a2 = str(eeee.split("Include Correction Field On", 1)[1])
                eeee = a1 + a2
            elif e in [8]:
                a2 = str(eeee.split("Include Correction Field On", 1)[1])
                a2 = a2[1:]
                eeee = a2
            elif e in [3, 6]:
                eeee = eeee
            zapisz = open(key, "w+")
            zapisz.write(eeee)
            zapisz.close()
            # print(key, e)


    def zgarnij_linijki(self):
        for key, value in numbers:
            # print(key)
            cala_strona=open(key, "r")
            whole_file = cala_strona.readlines()
            # print(whole_file)
            t1min=whole_file[2][:-3]
            t1max=whole_file[3][:-3]
            t1mean=whole_file[1][:-3]
            pomiar_format = "****************\n" + key + "\n" + t1min + "\n" + t1max + "\n" + t1mean + "\n****************"
            # if key =="2WayTime.txt":
            #     print(pomiar_format)
            zapisz3 = open("Measurements " + key, "w+")
            zapisz3.write(pomiar_format)
            zapisz3.close()

wyniki = klasa_readPDF()
# wyniki=klasa_readPDF.czytaj("1")
# wyniki=klasa_readPDF.zgarnij_linijki("2")


