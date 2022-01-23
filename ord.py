print("Wprowadz string'a")
b=input()

l=[]
po=[]
koniec=[]
for i in b:
    i=ord(i)
    print(i)
    l.append(i)
    i=i+2
    po.append(i)

print(l)
print(po)

for i in po:
    i=chr(i)
    print(i)
    koniec.append(i)

koniec = "".join(koniec)
print(koniec)

