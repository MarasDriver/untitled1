class bezwzgledna():
    def wypisz(self):
        czytaj = open("plik.txt", "r+")
        zawartosc = czytaj.read()
        print(zawartosc)

    def make(self):
        czytaj = open("plik.txt", "r+")
        zawartosc = czytaj.read()
        intab="abcdefghijklmnopqrstuvwxyz"
        outtab="cdefghijklmnopqrstuvwxyzab"
        b=str.maketrans(intab, outtab)
        print(zawartosc.translate(b))



    def zbierz(self):
        czytaj = open("plik.txt", "r+")
        zawartosc = czytaj.read()
        print(zawartosc)


        for i in zawartosc:

            x = ord(i)
            x=int(x)
            if x==32:
                print("UWAGA SPACJA")
                x=30
            if x==121:
                print("UWAGA Y")
                x=95
            if x==122:
                print("UWAGA Z")
                x=96
            if x==46:
                x=44
            print(i)
            print("Zmiana na liczbę")
            print(x)
            print("zmiana na literę plus 2")
            y = x+2
            print(y)
            print("wypisuje po zamianie")
            z=chr(y)
            print(z)
            lista.append(z)
            nowa_lista=" ".join(lista)
list=[]
list=str(list)
lista=[]
nowa_lista=[]
obj=bezwzgledna()
print("Tak było")
obj.wypisz()
obj.zbierz()
nowa_lista=" ".join(lista)
print("LISTA APPEND")
print(nowa_lista)
print("TRANS", "\n")
obj.make()
