
import time

t1 = time.time()
print("Zegar Start")
time.sleep(1)

t2=time.time()
e=time.time()-t1
print("Uruchamiam stoper czy timer? (s/t)")
a=input()

if a=="s":
    print("Uruchamiam stoper")
    while True:

        if e >= 1:
            t1 = time.time()
            time.sleep(1)
            e=time.time()-t1
        if time.time()-t2>9.5 and time.time()-t2<10.5:
            print("Minęło 10 sekund")
        if time.time() - t2 > 19.5 and time.time() - t2 < 20.5:
            print("Minęło 20 sekund")
        if time.time()-t2>29.5 and time.time()-t2<30.5:
            print("Minęło 30 sekund")
        if time.time()-t2>44.5 and time.time()-t2<45.5:
            print("Minęło 45 sekund")
        if time.time() - t2 >= 60:
            print("Minęło 60 sekund")
            break
if a=="t":
    print("Uruchamiam timer")
    print("Wpisz czas do odliczania")

    s = input()
    s=int(s)

    b0 = time.time()


    while s>0:
        print("Zostało", s-1, "sekund")
        s=s-1
        time.sleep(1)

    else:
        print("Czas stop")


print("Zegar wyłączony")