import webbrowser
t=0
ip=input("Wpisz IP:")
list=ip.split(".")

while len(list)!=4:
    ip=input("Wpisz poprawne IP (X.X.X.X):")
    list = ip.split(".")
nowe_ip = []
for i in list:
    t=t+1
    try:
        i=int(i)
        while i > 254 and list[t - 1] < 0:
            i = int(input())
    except ValueError:
        print("Błąd w ",t,"oktecie (Tylko liczba)")
        print(list)
        print(nowe_ip)
        print("Wpisz ponownie",t,"oktet")
        try:
            i=int(input())
            while i>254 and i<0:
                i=int(input())
        except ValueError:
            print("Liczba z przedziału 0-254!")
    nowe_ip.append(i)
print(nowe_ip)
t=0
for i in nowe_ip:
    t=t+1
    if int(i)>254:
        print("Błąd w ", t, "oktecie (oktet większy od 254)")
        print("Wpisz ponownie ", t, "oktet")
        try:
            nowe_ip[t-1]=int(input())
        except ValueError:
            print("Tylko liczba!")
        while nowe_ip[t-1]>254:
            print("Wpisz ponownie ", t, "oktet")
            nowe_ip[t - 1] = int(input())
    if int(i) < 0:
        print("Błąd w ", t, "oktecie (oktet mniejszy od 0)")
        print("Wpisz ponownie ", t, "oktet")
        try:
            nowe_ip[t - 1] = int(input())
        except ValueError:
            print("Tylko liczba!")
        while nowe_ip[t - 1] > 254:
            print("Wpisz ponownie ", t, "oktet")
            nowe_ip[t - 1] = int(input())
    else:
        print(t,"oktet poprawny")

print("IP",nowe_ip," w końcu poprawne!")
str_ip=""
for i in nowe_ip:
    str_ip=str_ip+str(i)
    str_ip=str_ip+"."
string_ip=str_ip[0:len(str_ip)-1]
print(string_ip)
webbrowser.open(string_ip)
