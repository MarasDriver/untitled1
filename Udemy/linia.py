import math
class Line():

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def distance(self):
        x1=self.x1
        x2=self.x2
        y1=self.y1
        y2=self.y2
        d=((x2-x1)**2+(y2-y1)**2)**0.5
        return d

    def slope(self):
        x1=self.x1
        x2=self.x2
        y1=self.y1
        y2=self.y2
        s=(y2-y1)/(x2-x1)
        return s



print("Liczymy długość odcinka z punktu o współrzędnych (x1,y1), do punktu (x2,y2)")
linia=Line(x1=int(input("Wprowadz x1")),y1=int(input("Wprowadz y1")),x2=int(input("Wprowadz x2")),y2=int(input("Wprowadz y2")))

d=linia.distance()
s=linia.slope()

print("Odległość między punktami wynosi:",d,"[j], natomiast nachylenie wynosi:",s,".")