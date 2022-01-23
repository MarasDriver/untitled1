#klasa która zbiera ciąg liczb na wejsciu oddzielonych spacjami
#enter konczy
#sortuje je po modulo
class bezwzgledna():
    def dupa(self, mod):
        return abs(int(mod))

    def zbierz(self):
        liczby = input()
        a = liczby.split(" ")
        b = sorted(a, key=self.dupa)
        self.x=" ".join(b)
        return self.x
    def jednakolumna(self):
        f=self.x.split(" ")
        return "\r\n".join(f)


obj = bezwzgledna()
obj.zbierz()
print(obj.jednakolumna())
