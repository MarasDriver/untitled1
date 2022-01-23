import time
t1 = time.time()

class Calculator():

    def dodaj(self,x,y):
        z=x+y
        print(z)
    def odejmij(self,x,y):
        z=x-y
    def pomnóż(self,x,y):
        z=x*y
    def podziel(self,x,y):
        z=x/y

print("Podaj x")
x=input()
x=float(x)
print("Dodajemy, odejmujemy mnożymy czy dzielimy, ? (1/2/3/4)")
o=input()
o=int(o)
z="Dupa"

if o==1:
    print("Podaj y")
    y=input()
    y=float(y)
    calc=Calculator()
    z=calc.dodaj(x,y)
    print("Wynik to", z)
if o==2:
    print("Podaj y")
    y = input()
    y = float(y)
    calc = Calculator()
    z = calc.odejmij(x, y)
    print("Wynik to", z)
if o==3:
    print("Podaj y")
    y = input()
    y = float(y)
    calc = Calculator()
    z = calc.pomnóż(x, y)
    print("Wynik to", z)
if o==4:
    print("Podaj y")
    y = input()
    y = float(y)
    calc = Calculator()
    z = calc.podziel(x, y)
    print("Wynik to", z)


while z=="Dupa":
    print("Wynik to", z)
    break
else:
    time.sleep(1)
    t=time.time()-t1
    t=int(t)
    print("Policzyłes to w", t, "sekund(ę/y), brawo!")


