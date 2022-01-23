import time
import datetime

d = datetime.datetime.now()
print(d.strftime("%H:%M:%S %d.%b.%Y"))
t1 = time.time()

print("Zegar Start")
time.sleep(1)

t2=time.time()
e=time.time()-t1
while True:
    if e >= 1:
        d = datetime.datetime.now()
        print("Aktualna godzina i data to:",end=' ')
        print(d.strftime("%H:%M:%S %d.%b.%Y"))
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
        break
print("Minęła minuta, zegar zatrzymany")