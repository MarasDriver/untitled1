
class TooColdException(Exception):
   def __init__(self, temp):
       super().__init__("Temp {} is too low".format(temp))

def celsius_to_kelvin(temp):
    if temp<-273.15:
        raise TooColdException(temp)
    print(temp)
    return temp+273.15



print(celsius_to_kelvin(0))
