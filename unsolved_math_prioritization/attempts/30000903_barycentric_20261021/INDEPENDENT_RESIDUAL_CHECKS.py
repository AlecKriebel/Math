from itertools import product
from math import comb
import hashlib,json

# Independent chain enumeration on concrete finite face posets.
# No formulas from the residual verification program are imported.
def cube(d):
    elements=[None]+list(product(range(3),repeat=d))
    ranks=[0]+[x.count(2)+1 for x in elements[1:]]
    def leq(x,y):
        if x is None: return True
        if y is None: return False
        return all(b==2 or a==b for a,b in zip(x,y))
    return elements,ranks,leq

def ordered(data):
    elements,ranks,leq=data
    pairs=sorted(zip(elements,ranks),key=lambda p:p[1])
    return [p[0] for p in pairs],[p[1] for p in pairs],leq

def pyramid(data):
    e,r,leq=ordered(data)
    pairs=[(i,b) for i in range(len(e)) for b in [0,1]]
    ranks=[r[i]+b for i,b in pairs]
    return pairs,ranks,lambda a,b: leq(e[a[0]],e[b[0]]) and a[1]<=b[1]

def prism(data):
    e,r,leq=ordered(data)
    # Segment nonempty face labels: vertices 0,1 and whole edge 2.
    pairs=[None]+[(i,j) for i in range(1,len(e)) for j in range(3)]
    ranks=[0]+[r[i]+(j==2) for i,j in pairs[1:]]
    def pleq(a,b):
        if a is None: return True
        if b is None: return False
        return leq(e[a[0]],e[b[0]]) and (a[1]==b[1] or b[1]==2)
    return pairs,ranks,pleq

def proper_h(data):
    e,r,leq=ordered(data)
    assert r[0]==0 and sum(v==r[-1] for v in r)==1
    d=r[-1]-1
    assert all(leq(e[0],y) and leq(y,e[-1]) for y in e)
    elements=e[1:-1]
    dp=[]
    chains=[1]+[0]*d
    for i,x in enumerate(elements):
        counts=[0]*(d+1)
        counts[1]=1
        for j,y in enumerate(elements[:i]):
            if leq(y,x):
                for k in range(1,d): counts[k+1]+=dp[j][k]
        dp.append(counts)
        chains=[a+b for a,b in zip(chains,counts)]
    return [sum(chains[i]*(-1)**(k-i)*comb(d-i,k-i) for i in range(k+1)) for k in range(d+1)]

def operator(h,lam):
    d=len(h)-1
    return [(1+lam*k)*(h[k] if k<=d else 0)
            +(lam*d+1-lam*(k-1))*(h[k-1] if k else 0)
            for k in range(d+2)]

results={}
for d in range(5):
    P=cube(d)
    h=proper_h(P)
    hp=proper_h(pyramid(P))
    hq=proper_h(prism(P))
    hpq=proper_h(prism(pyramid(P)))
    assert hp==operator(h,1),(d,hp)
    assert hq==operator(h,2),(d,hq)
    assert hpq==operator(hp,2),(d,hpq)
    results[str(d)]={'cube_h':h,'pyramid_h':hp,'prism_h':hq,'prism_pyramid_h':hpq}
assert results['3']['cube_h']==[1,23,23,1]
assert results['3']['pyramid_h']==[1,50,138,50,1]
assert results['3']['prism_pyramid_h']==[1,159,1040,1040,159,1]
results['status']='PASS: 15 operator identities checked against actual face-poset chain enumeration.'
results['source_sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
print(json.dumps(results,indent=2))
