from collections import Counter
from itertools import product

def mul(a,b):
    if a is None or b is None or a[0]!=b[0]: return None
    return (a[0],a[1]+b[1])

def ev(args):
    if any(a is None for a in args): return Counter()
    return Counter({((),tuple(args),()):1})

def left(a,c):
    if a is None or a[0]=='q': return Counter()
    return Counter({(a[1]+l,p,r):v for (l,p,r),v in c.items()})

def right(c,a):
    if a is None or a[0]=='q': return Counter()
    return Counter({(l,p,r+a[1]):v for (l,p,r),v in c.items()})

def add(out,c,sign=1):
    for k,v in c.items():out[k]+=sign*v

def differential(cochain,args):
    n=len(args)-1
    out=Counter()
    add(out,left(args[0],cochain(args[1:])))
    for j in range(n):
        add(out,cochain(args[:j]+[mul(args[j],args[j+1])]+args[j+2:]),(-1)**(j+1))
    add(out,right(cochain(args[:-1]),args[-1]),(-1)**(n+1))
    return out

def J(cochain,args):
    if any(a is None for a in args):return Counter()
    first=next((i for i,a in enumerate(args) if a[0]=='q'),None)
    if first is None:return Counter()
    out=Counter()
    add(out,cochain(args[:first]+[('q',())]+args[first:]),(-1)**(first+1))
    return out

count=0
for n in range(1,10):
    for tags in product(('z','q'),repeat=n):
        args=[(tag,(i,)) for i,tag in enumerate(tags)]
        actual=differential(lambda aa:J(ev,aa),args)
        add(actual,J(lambda aa:differential(ev,aa),args))
        expected=ev(args) if 'q' in tags else Counter()
        allkeys=set(actual)|set(expected)
        bad={k:actual[k]-expected[k] for k in allkeys if actual[k]!=expected[k]}
        if bad:raise AssertionError((n,tags,bad))
        count+=1
print('Formal central-pattern homotopy identity verified in degrees 1 through 9, for',count,'patterns; q acts by zero on the output module.')
