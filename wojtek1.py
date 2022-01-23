print("Podnosimy do kwadratu czy pierwiastkujemy? (1/2)")
u = input()

class Calculator():
    def pierwiastek(self, x):
        z=(x)**(1/2)
        return z

    def kwadrat(self, x):
        z=x*x
        return z
if u=="1":
    print("Podnosimy do kwadratu")
    print("podaj x")
    x=input()
    dupa = Calculator()
    z=dupa.kwadrat(float(x))

if u=="2":
    print("Pierwiastkujemy")
    print("Podaj x")
    x=input()
    x=float(x)
    dupa=Calculator()
    z=dupa.pierwiastek(x)

print(z)
print("Wynik to", z)



