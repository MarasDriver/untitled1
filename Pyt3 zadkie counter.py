class licznik():
    def licz(self):
        czytaj = open("rzadkie.txt", "r+")
        rzadkie = czytaj.read(10000)

        for i in rzadkie:
            liczba=rzadkie.count(i)


            if rzadkie.count(i) < 25:
                litery.append(i)
                cyfry.append(rzadkie.count(i))
                e = cyfry.index(min(cyfry))
        print(min(cyfry))
        print(litery)

        print("Twój element zajmuje", e, "miejsce w liście powyżej")



litery=[]
cyfry=[]

obj=licznik()
obj.licz()


