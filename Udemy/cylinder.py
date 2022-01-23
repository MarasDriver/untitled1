class Cylinder:

    def __init__(self, h, r):
        self.h=h
        self.r=r
        self.pi=3.14
    def volume(self):
        h=self.h
        r=self.r
        pi=self.pi
        v=pi*r**2*h
        return v


    def surface_area(self):
        h = self.h
        r = self.r
        pi = self.pi
        p=2*pi*r**2+2*pi*r*h
        return p



print("Liczymy pole powierzchni i objętość walca")
cylinder=Cylinder(h=int(input("Wprowadz wysokość:")),r=int(input("Wprowadz promień:")))

p=cylinder.surface_area()
v=cylinder.volume()
print("Objęość wynosi: {} [j^3], natomiast pole powierzchni całkowitej {} [j^2]".format(v,p))