print("Zaczynamy")
print("Wpisz nazwę swojego pliku", "\n""\n")
class defklas():

    def otworz(self, u):
        czytaj = open(u, "r+")
        self.zawartosc=czytaj.read()
        czytaj.close()
        print("To zczytałem z Twojego pliku", "\n")
        print(self.zawartosc, "\n" "\n")


    def zmiana(self, u):
        czytaj = open(u, "r+")
        zawartosc = czytaj.read()
        x="class"
        y=zawartosc.find(x)
        print(y)
        z=zawartosc.tell(x)


        zawartosc.write()
        print(czytaj.read())
        czytaj.close()



obj = defklas()
u=input()
obj.otworz(u)
obj.zmiana(u)
print(obj.zmiana(u))


