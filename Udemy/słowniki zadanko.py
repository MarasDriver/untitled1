d = {'simple_key':'hello'}
print(d)
a = {'k1':{'k2':'hello'}}
b= {'k1': [{'nest_key': ['this is deep', ['hello']]}]}
c={'k1':[1,2,{'k2':['this is tricky',{'tough':[1,2,['hello']]}]}]}
print(a)
print(b)
print(c)
print(c.keys())
print(c.values())
print(c.items())

print(c["k1"][2]['k2'][1]['tough'][2][0])
