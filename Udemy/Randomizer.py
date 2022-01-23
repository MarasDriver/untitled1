from random import randint
b=1
a=101
dol=int(input("Wpisz dolną część przedziału"))
gora=int(input("Wpisz górną część przedziału"))
c=int(input("Wpisz szukaną liczbę", ))
while a!=c:
    a = randint(dol,gora)
    if a==c:
        continue
    print(a, "To nie ta liczba", "podejście numer",b)
    #print(a,c)
    b+=1
else:
    print(a, "Znalazłem za ", b,"-tym razem")