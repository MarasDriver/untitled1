class czytaj:
    def otworz(self):
        czyta = open("ramka.txt", "r+")
        a = czyta.read()
        czyta.close()
        return a


obj = czytaj()
a=obj.otworz()
z=0
lista=a.split(" ")
print(a)
b=""
c=""
for x in a:
    print("LP:", z,"a znak to",x)
    z=z+1

for x in a[19:33]:
    b=b+x

for x in a[39:49]:
    print("Jest przedział")
    c = c + x

for x in a[84:88]:
    c = c + x


print("MAC Nadawcy: ",b)
print("MAC Odbiorcy: ",c)

