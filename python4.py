import linecache
class otoczona():

    def szukaj(self, u):
        czytaj = open(u, "r+")
        zawartość = czytaj.read()
        czytaj.close()
        print("Start\n" + zawartość + "\nKoniec\n")

        count = zawartość.__len__()

        print(count, "Liter")
        count_lines=(count+1)/81
        print(count_lines, "Linijek")

        #zawartość = list(zawartość)
        lista_dużych = []
        for i in zawartość:
            a=i
            if i.lower() == i:
               print("Mam małą literę", i)
            elif i.upper() == i:
                print("Mam wielką literę", i)
                lista_dużych.append(i)
            else:
                return lista_dużych

        print(lista_dużych)
        print(lista_dużych.__len__())

print("Wyberasz plik python4.txt? (t/n)")
a=input()

if a=="t":
    obj = otoczona()
    b = "python4.txt"
    obj.szukaj(b)
if a=="n":
    print("Wpisz nazwę pliku")
    obj = otoczona()
    u=input()
    obj.szukaj(u)

