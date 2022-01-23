import linecache
print("Zaczynamy")
class defklas():

    def otworz(self, u):
        czytaj = open(u, "r+")
        self.zawartosc=czytaj.read()
        #print(self.zawartosc)
        czytaj.close()
        #print("To zczytałem z Twojego pliku", "\n")
        #print(self.zawartosc, "\n" "\n")


    def zmiana(self, u):
        czytaj = open(u, "r+")
        count = len((czytaj).readlines())
        print(count)
        g=0
        while g<count:
            wiersz = linecache.getline(u, g)
            g=g+1
            a = wiersz.find('class')
            if a!=-1:
                print(a)
                print("MAM CLASS")
                wiersz="<class>"+wiersz.rstrip()+"</class>       ""\r"
                open("temp.txt", 'a').write(wiersz)
            else:
                open("temp.txt", 'a').write(wiersz)
        g=0
        while g<count:
            wiersz = linecache.getline("temp.txt", g)
            g=g+1
            b=wiersz.find("def")
            if b!=-1:
                print(b)
                print("MAM DEF")
                wiersz="<def>"+wiersz.rstrip()+"</def>       ""\r"
                open(w, 'a').write(wiersz)
            else:
                open(w, 'a').write(wiersz)




obj = defklas()
print("Wpisz nazwę swojego pliku", "\n")
u=input()
print("Wpisz nazwę pliku do którego zapiszemy zmiany")
w=input()
obj.otworz(u)
obj.zmiana(u)

