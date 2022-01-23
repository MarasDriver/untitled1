import time
import math

def co():
    co="x"
    while co!="p" and co!="o":
        co = input("Co chcesz policzyć? Pole czy obwód? (P/O) \n").lower()
        start = time.time()
        if co=="o":
            print("Wybrałes liczenie obwodu!")
            obwod()
            gz=input(("Czy chcesz jeszcze policzyć pole? (y/n)"))
            while gz!="y" and gz!="n":
                gz=input(("Czy chcesz jeszcze policzyć pole? (y/n)"))
            if gz=="y":
                pole_z_obw()
            else:
                pass
            print("Brawo, zajęło Ci to:", int(time.time() - start), "Sekund!")
            if not replay():
                close()
                break
            else:
                co="x"
        elif co=="p":
            print("Wybrałes liczenie pola!")
            pole()
            print("Brawo, zajęło Ci to:", int(time.time() - start), "Sekund!")
            if not replay():
                close()
                break
            else:
                co="x"

def close():
    print("Calculator is closing.")
    time.sleep(1)
    print("Calculator is closing..")
    time.sleep(0.5)
    print("Calculator is closed.")

def wysokosc_bok():
    bok=" "
    while bok!="a" and bok!="b" and bok!="c":
        try:
            bok=input(("Na który bok upuszczamy wysokość?? (a/b/c)??? \n"))
        except ValueError:
            print("To nie jest (a/b/c)!!!")

    while bok=="a":
        try:
            h=int(input(("Podaj długość wysokości 'h', opuszczonej na bok 'a' \n")))
            while h<=0:
                print("Ujemna długość boku...")
                time.sleep(0.5)
                print("Pozdrawiam :)")
                h = int(input(("Podaj długość wysokości 'h', oopuszczonej na bok 'a' \n")))
            return h, bok
        except ValueError:
            print("To nie jest długość!!!")
    while bok=="b":
        try:
            h=int(input(("Podaj długość wysokości 'h', opuszczonej na bok 'b' \n")))
            while h<=0:
                print("Ujemna długość boku...")
                time.sleep(0.5)
                print("Pozdrawiam :)")
                h = int(input(("Podaj długość wysokości 'h', opuszczonej na bok 'b' \n")))
            return h, bok
        except ValueError:
            print("To nie jest długość!!!")
    while bok=="c":
        try:
            h=int(input(("Podaj długość wysokości 'h', opuszczonej na bok 'c' \n")))
            while h<=0:
                print("Ujemna długość boku...")
                time.sleep(0.5)
                print("Pozdrawiam :)")
                h = int(input(("Podaj długość wysokości 'h', opuszczonej na bok 'c' \n")))
            return h, bok
        except ValueError:
            print("To nie jest długość!!!")

def pole():
    h, bok = wysokosc_bok()
    print("Liczę polę dla boku",bok, "i wysokości", h)
    bok_2=" "
    while bok_2==" ":
        try:
            print("Podaj długość boku", bok)
            bok_2 = float(input())
            while bok_2 <=0:
                print("Podaj długość boku", bok, "gnoju!")
                bok_2 = int(input())
        except ValueError:
            print("Litery to nie długość głąbie!!!")
        pole = (bok_2*h)/2
        print("Pole powierzchni trójkąta wynosi", round(pole,2), "[j^2].")

def obwod():
    while True:
        try:
            global a
            a=float(input(("Podaj długość boku 'a' \n")))
            if a > 0:
                break
        except ValueError:
            print("To nie jest długość!!!")
        except a<=0:
            print("Ujemna długość boku...")
            time.sleep(0.5)
            print("Pozdrawiam :)")
            time.sleep(1)
    while True:
        try:
            global b
            b = float(input(("Podaj długość boku 'b' \n")))
            if b > 0:
                break
        except ValueError:
            print("To nie jest długość!!!")
        except b <= 0:
            print("Ujemna długość boku...")
            time.sleep(0.5)
            print("Pozdrawiam :)")
            time.sleep(1)
    while True:
        try:
            global c
            c = float(input(("Podaj długość boku 'c' \n")))
            if c > 0:
                break
        except ValueError:
            print("To nie jest długość!!!")
        except c <= 0:
            print("Ujemna długość boku...")
            time.sleep(0.5)
            print("Pozdrawiam :)")
            time.sleep(1)
    z=sprawdz_obw()
    while z is True:
        global obw
        obw= a + b + c
        obw=round(obw,5)
        print("Obwód wynosi", round(obw,2), "[j]")
        return a,b,c,obw
    if z is False:
        print("Taki trójkąt nie istenieje")
        ghg=input("Próbujemy trójkąt który ma prawo istnieć?? (y/n)").lower()
        while ghg!="y" and ghg!="n":
            ghg = input("Próbujemy trójkąt który ma prawo istnieć?? (y/n)").lower()
        if ghg=="y":
            obwod()

def sprawdz_obw():
    return (a+b>c and a+c>b and b+c>a)

def pole_z_obw():

    a,b,c,obw
    ob=obw/2
    pole2=math.sqrt(ob*(ob-a)*(ob-b)*(ob-c))
    print("Pole powierzchni trójkąta wynosi", round(pole2,2), "[j^2].")

def replay():
    return input("Liczymy jeszcze raz? (y/n)").lower().startswith('y')

print("Oto najbardziej zaawansowany technicznie, technologicznie i software'owo kalkulator do liczenia pola lub obwodu trójkąta.")
time.sleep(1)
print("Co liczymy?")
co()
time.sleep(2)