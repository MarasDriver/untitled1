import linecache
class otoczona():

    def szukaj(self, u):
        czytaj = open(u, "r+")
        zawartość = czytaj.read()
        print(zawartość)

        zawartość.split(" ")
        print(zawartość)
        czytaj.close()
        print(count, "Linijek")
        zawartość = list(zawartość)
        count = len((zawartość).readlines())
        print(zawartość)


        #for i in zawartość:

            #print("Mam małą literę")

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

