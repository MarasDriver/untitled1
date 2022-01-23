



czytaj = open("python4.txt", "r+")
zawartosc=czytaj.read()
czytaj.close()
print("To zczytałem z Twojego pliku", "\n")
print(zawartosc, "\n" "\n")

for i in zawartosc:
    if ord(i) > 97 and ord(i)<122:
        print(i)
        print("mała")
        j=str(i+1)
        h=str(i=1)
        for j in zawartosc:
            if (ord(j)>65 and ord(j)<90) and (ord(h)>65 and ord(h)<90):
                print(" Duża na prawo")
                print(j)