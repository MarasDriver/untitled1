import time
t1=time.time()

print("Podaj x")
x = input()
x = float(x)

print("Mnożymy, dzielimy, dodajemy czy odejmujemy? (1/2/3/4)")
o=input()
o=int(o)
while o>4:
    print("Ej, ale tak się nie bawię :)")
    break
else:
    t2=time.time()-t1
    t2=int(t2)
    print("WOW, zdecydowałes się w", t2, "sekund(ę/y), koooozak!")

z="Dupa"

if o==1:
    print("Okej, więc mnożymy x*y")
    print("Przez co mnożymy?")
    y=input()
    y=float(y)
    z=x*y
    z=int(z)

if o==2:
    print("Okej, więc dzielimy")
    print("Podaj dzielnik")
    y = input()
    y = float(y)
    while y==0:
        try:
            z=x/y
        except ZeroDivisionError:
            print("Ty pacanie, co z Ciebie za inżynier")
            print("Dzielisz przez 0")
            time.sleep(5)
            print("Facepalm \n")
            time.sleep(2)
            break



if o==3:
    print("Okej, no to dodajemy")
    print("Podaj y")
    y = input()
    y = float(y)
    z = x + y

if o==4:
    print("Czyli odejmowanie, wporządku")
    print("Podaj y")
    y = input()
    y = float(y)
    z = x - y

while z=="Dupa":
    print("Wynik to", z)
    break
else:
    print("Wynik to", z)
    time.sleep(1)
    t=time.time()-t1
    t=int(t)
    print("Policzyłes to w", t, "sekund(ę/y), brawo!")