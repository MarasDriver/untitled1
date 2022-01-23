from collections import Counter

czytaj = open("rzadkie.txt", "r+")
zawartosc=czytaj.read()
czytaj.close()
print("To zczytałem z Twojego pliku", "\n")
print(zawartosc, "\n" "\n")

c = Counter(zawartosc)
print(c)
