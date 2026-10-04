"""Independent exact algebraic-endpoint controls, using integer square roots."""
from math import isqrt
import json

# Integer pairs a,b denote a+b*sqrt(2). All phases tested below have integer pairs.
def plus(x,y):
    return x[0]+y[0],x[1]+y[1]
def minus(x,y):
    return x[0]-y[0],x[1]-y[1]
def times(x,n):
    return x[0]*n,x[1]*n
def floor_pair(x):
    a,b=x
    if b==0:
        return a
    t=isqrt(2*b*b)
    return a+t if b>0 else a-t-1
def fraction_pair(x):
    return x[0]-floor_pair(x),x[1]
def compare(x,y):
    z=minus(x,y)
    if z==(0,0):
        return 0
    return 1 if floor_pair(z)>=0 else -1

alpha=(-1,1)
def symbol(u,k):
    return floor_pair(plus(u,times(alpha,k+1)))-floor_pair(plus(u,times(alpha,k)))

failures=[]
checks=0
endpoint_pairs=0
for n in range(1,129):
    na=times(alpha,n)
    q=floor_pair(na)
    t=fraction_pair(na)
    threshold=minus((1,0),t)
    # Future includes equality; past excludes equality.
    for kind,u,want in [('future',threshold,1),('past',t,0)]:
        observed=(floor_pair(plus(u,na))-q if kind=='future' else -floor_pair(minus(u,na))-q)
        checks+=1
        if observed!=want:
            failures.append({'kind':kind,'n':n,'u':u,'observed':observed,'expected':want})
        endpoint_pairs+=1
        for m in range(-5,6):
            v=fraction_pair(plus(u,times(alpha,m)))
            forward=backward=0
            for length in range(1,65):
                forward+=symbol(v,length-1)
                backward+=symbol(v,-length)
                la=times(alpha,length)
                lq=floor_pair(la)
                lt=fraction_pair(la)
                lhs=forward-lq
                rhs=int(compare(v,minus((1,0),lt))>=0)
                plhs=backward-lq
                prhs=int(compare(v,lt)<0)
                checks+=3
                if lhs!=rhs or plhs!=prhs or symbol(v,length-1)!=symbol(u,m+length-1):
                    failures.append({'kind':kind,'n':n,'m':m,'length':length,'forward':[lhs,rhs],'past':[plhs,prhs]})

result={'status':'PASS' if not failures else 'FAIL','arithmetic':'Integer pairs and integer square roots only',
        'alpha':'sqrt(2)-1','exact_threshold_cases':endpoint_pairs,'checks':checks,'failures':failures,
        'scope':'Supplementary finite endpoint and shift-recoding controls; density proves all-length recovery'}
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if not failures else 1)
