class Uzytkownik():
    def __init__(self):
        self.lista = []
    def dopisz(self, imie, nazwisko):
        obj.lista.append(imie)
        print(imie, nazwisko)
        obj.lista.append(nazwisko)
        obj.lista=str(lista)
        print(obj.lista)
        print("Zapisać? t/n")
        r = input()
        if r=="t":
            print("Koniec wpisywania")
        if r=="n":
            print("Nie zapisałem")
            obj.lista=[]

    def zapisz(self):
            print("Program zakończony, pomyślnie zapisano do pliku")
            czytaj = open("Imiona.txt", "a+")
            czytaj.write(str(obj.lista))
            print(czytaj.read())
            czytaj.close()

    def odczyt(self):
        czytaj = open("Imiona.txt", "r")
        zawartosc=czytaj.read()
        print("To zczytałem z Twojego pliku")
        print(zawartosc, "\n" "\n")



print("Co zamierzasz zrobić?")
print("Wpisujemy, czy odczytujemy? (w/o)")
obj = Uzytkownik()

lista=obj.lista
p=input()
if p=="w":
    print("Podaj imie, a po wciśnięciu ENTER wpisz Nazwisko")
    obj.dopisz(imie=input(), nazwisko=input())
    if obj.lista!=[]:
        print("Zapisać do pliku Imiona.txt? (t/n)")
        u=input()
        if u=="t":
            obj.zapisz()
        if u=="n":
            print("Podaj inny plik")
            g=input()
            czytaj = open(g, "a+")
            czytaj.write(str(obj.lista))
            czytaj.close()

    print("Odczytać z pliku Imiona.txt? (t/n))")
    p = input()
    if p == "t":
        obj.odczyt()
        print("Koniec programu")
    if p == "n":
        print("Koniec programu")

if p=="o":
    print("Sortujemy po imionach czy nazwiskach? (i/n)")
    z=input()
    if z=="i":
        b=lista.sort(key=lambda r: r[0])
        print(b)

    if z=="n":
        c=lista.sort(key=lambda r: r[1])
        print(c)