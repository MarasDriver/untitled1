class Konto:

    def __init__(self,właściciel,stan_konta):

        self.właściciel=właściciel
        self.stan_konta=stan_konta

    def __str__(self):
        return f'Właściciel konta:   {self.właściciel}\nStan konta:         {self.stan_konta} zł'

    def wpłać(self):
        ile1 = int(input(("Ile pieniędzy wpłacasz?")))
        while ile1<0:
            ile1 = int(input(("Ile pieniędzy wpłacasz?")))
        self.stan_konta += ile1
        print("Przyjęto wpłatę")

    def wypłać(self):

        ile = int(input("Ile wypłacasz?\n"))
        while ile<0:
            ile = int(input(("Ile pieniędzy wypłacasz?")))
        if self.stan_konta>=ile:
            self.stan_konta = self.stan_konta-ile
            print("Wypłacono {} zł, \nPozostało {} zł.".format(ile,self.stan_konta))
        else:
            print("Wypłata odrzucona, brak środków!")
    def replay():
        return input("Kontunuujemy? (y/n)\n").lower().startswith('y')

    def close():
        print("Transakcje zakończone.")


bank=Konto(właściciel=input("Wprowadź imię właściciela\n"),stan_konta=int(input("Wprowadz stan konta\n")))


while True:
    x = input(("\n\nCo robimy?\nSprawdzamy stan konta (s)     Wpłacamy (wp)     Wypłacamy (wy)\n"))
    if x =="s":
        print(bank)
        if not Konto.replay():
            close()
        else:
            x= None
    if x =="wp":
        bank.wpłać()
        if not Konto.replay():
            Konto.close()
            break
        else:
            x= None
    if x== "wy":
        bank.wypłać()
        if not Konto.replay():
            Konto.close()
            break
        else:
            x= None
