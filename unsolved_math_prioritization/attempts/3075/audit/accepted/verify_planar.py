"""Independent exact polygon-clipping verifier for the authored 8-line witness."""
from fractions import Fraction as Q
from itertools import product,combinations
from collections import Counter

def need(x,message):
    if not x:raise ValueError(message)

def area(poly):
    return sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1]))

def simplify(poly):
    p=[]
    for x in poly:
        if not p or p[-1]!=x:p.append(x)
    if len(p)>1 and p[-1]==p[0]:p.pop()
    changed=True
    while changed and len(p)>2:
        changed=False
        for i in range(len(p)):
            a,b,c=p[i-1],p[i],p[(i+1)%len(p)]
            if (b[0]-a[0])*(c[1]-b[1])==(b[1]-a[1])*(c[0]-b[0]):
                p.pop(i);changed=True;break
    return p

def clip(poly,a,b,c):
    if not poly:return []
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        fp=a*p[0]+b*p[1]-c;fq=a*q[0]+b*q[1]-c
        if fp>=0:out.append(p)
        if (fp<0<fq) or (fq<0<fp):
            t=fp/(fp-fq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return simplify(out)

def inspect(rows):
    vertices=[]
    for i,j in combinations(range(len(rows)),2):
        a,b,c=rows[i];e,f,g=rows[j];det=a*f-b*e
        need(det!=0,'Parallel witness lines')
        p=(Q(c*f-b*g,det),Q(a*g-c*e,det))
        need(all(k in (i,j) or x*p[0]+y*p[1]!=z for k,(x,y,z) in enumerate(rows)),'Concurrent witness lines')
        vertices.append(p)
    M=max(abs(x) for p in vertices for x in p)+1
    bounded=[];feasible=0
    for signs in product((-1,1),repeat=len(rows)):
        p=[(-M,-M),(M,-M),(M,M),(-M,M)]
        for s,(a,b,c) in zip(signs,rows):p=clip(p,s*a,s*b,s*c)
        if len(p)<3 or area(p)==0:continue
        feasible+=1
        if any(abs(x)==M or abs(y)==M for x,y in p):continue
        bounded.append({'signs':list(signs),'sides':len(p),'diameter':len(p)//2,
                        'polygon':[[str(x),str(y)] for x,y in p]})
    n=len(rows)
    need(feasible==1+n*(n+1)//2,'Wrong planar chamber count')
    need(len(bounded)==(n-1)*(n-2)//2,'Wrong planar bounded count')
    return {'bounded_cells':len(bounded),'diameter_sum':sum(x['diameter'] for x in bounded),
            'facet_histogram':{str(k):v for k,v in sorted(Counter(x['sides'] for x in bounded).items())},
            'cells':bounded}
