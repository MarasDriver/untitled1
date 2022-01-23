def myfunc(a,b):
    list=[x if x%2==0 else 0 for x in (a,b)]
    print(list)
    return list

print(myfunc(-2,3))
