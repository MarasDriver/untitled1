liczba=int(input("Wpisz liczbę", ))
print(f"To jest twoja liczba: {liczba}")
a=0
while(liczba>0):
    a=a+1
    print("Liczba przed:", liczba)
    liczba=liczba//10
    print(f"Liczba po: {liczba}")
print("Ilość cyfr w liczbie to", a)


