import time
print("Wpisz hasło")
f="z"
h=input()
class defklas():

    def otworz(self):
        czytaj = open("hasło.txt", "r+")
        self.f = czytaj.read()
        czytaj.close()
    def zmień(self):
        print("Zmieniamy hasło? Wpisz (t/n)")
        a=input()
        if a == "t":
            print("Wpisz nowe hasło")
            b = input()
            open("hasło.txt", 'w').write(b)
            print("Zapisano")
            time.sleep(1.5)
            print("Koniec")
            time.sleep(4)
        if a == "n":
            print("Zmiana hasła odrzucona")
            time.sleep(1.5)
            print("Koniec")
            time.sleep(4)

obj = defklas()
obj.otworz()
#print(obj.f)

if h==obj.f:
    print("Złamałeś hasło!")
    obj.zmień()
else:
    print("Błędne hasło")
    time.sleep(2)

    print("Spróbuj ponownie")
    h=input()
    while h!=obj.f:
        print("Spróbuj ponownie")
        h=input()
    else:
        print("Złamałeś hasło!")
        obj.zmień()


