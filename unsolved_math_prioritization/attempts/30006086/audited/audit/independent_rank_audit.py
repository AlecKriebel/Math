"""Independent standard-library integer audit, no author module imports.
Uses Lyndon testing by rotations, greedy longest Lyndon prefixes, raw-word
commutators, and primitive-integer elimination instead of PBW coordinates.
"""
import argparse, functools, hashlib, itertools, json, math, pathlib, sys, time
from collections import defaultdict
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parent
P=ROOT.parent/'author'
if not __debug__:
    raise RuntimeError('Run without -O: independent rank verification uses assertions.')

@functools.cache
def words(c):
    if sum(c)==0:return ((),)
    out=[]
    for i,x in enumerate(c):
        if x:
            q=list(c);q[i]-=1
            out.extend((i,)+w for w in words(tuple(q)))
    return tuple(out)

@functools.cache
def lyndon(w):
    return bool(w) and all(w < w[k:]+w[:k] for k in range(1,len(w)))

@functools.cache
def factors(w):
    if not w:return ()
    k=max(i for i in range(1,len(w)+1) if lyndon(w[:i]))
    fs=(w[:k],)+factors(w[k:])
    assert all(fs[i]>=fs[i+1] for i in range(len(fs)-1))
    return fs

def multiply(a,b):
    r=defaultdict(int)
    for u,x in a.items():
        for v,y in b.items():r[u+v]+=x*y
    return {w:x for w,x in r.items() if x}

def subtract(a,b):
    r=dict(a)
    for w,x in b.items():r[w]=r.get(w,0)-x
    return {w:x for w,x in r.items() if x}

@functools.cache
def lie(w):
    assert lyndon(w)
    if len(w)==1:return {w:1}
    v=min(w[k:] for k in range(1,len(w)))
    u=w[:-len(v)]
    assert lyndon(u) and lyndon(v)
    return subtract(multiply(lie(u),lie(v)),multiply(lie(v),lie(u)))

@functools.cache
def basis(c):
    ans=[]
    for w in words(c):
        fs=factors(w)
        if any(len(f)==1 for f in fs):continue
        a={():1}
        for f in fs:a=multiply(a,lie(f))
        assert min(a)==w and a[w]==1
        ans.append(a)
    return tuple(ans)

def normalize(r):
    g=math.gcd(*r.values())
    if r[min(r)]<0:g=-g
    return {k:x//g for k,x in r.items()}

def integer_rank(rows):
    piv={}
    for row in rows:
        r={k:x for k,x in row.items() if x}
        if r:r=normalize(r)
        while r:
            p=min(r)
            if p not in piv:piv[p]=r;break
            v=piv[p];a=r[p];b=v[p];g=math.gcd(a,b)
            r={k:x*(b//g) for k,x in r.items()}
            for k,x in v.items():r[k]=r.get(k,0)-x*(a//g)
            r={k:x for k,x in r.items() if x}
            if r:r=normalize(r)
    return len(piv)

def cyclic(a):
    r=defaultdict(int)
    for w,x in a.items():r[min(w[k:]+w[:k] for k in range(len(w))) if w else ()]+=x
    return {w:x for w,x in r.items() if x}

def delete(a,i):
    r=defaultdict(int)
    for w,x in a.items():
        for k,v in enumerate(w):
            if v==i:r[w[:k]+w[k+1:]]+=x
    return {w:x for w,x in r.items() if x}

def brackets(c):
    for i,x in enumerate(c):
        if not x:continue
        q=list(c);q[i]-=1
        for a in basis(tuple(q)):
            # Reverse author's orientation, which must have identical rank.
            b=subtract(multiply({(i,):1},a),multiply(a,{(i,):1}))
            assert not cyclic(b)
            yield b

def check(c):
    vs=basis(c)
    for v in vs:
        for i in range(len(c)):assert not delete(v,i)
    # Inclusion-exclusion from the multigraded PBW Hilbert series.
    dim=0
    for bits in itertools.product((0,1),repeat=len(c)):
        q=[x-b for x,b in zip(c,bits)]
        if min(q)>=0:
            z=math.factorial(sum(q))
            for x in q:z//=math.factorial(x)
            dim+=(-1)**sum(bits)*z
    assert len(vs)==dim
    b=integer_rank(brackets(c));j=integer_rank(map(cyclic,vs))
    return {'content':list(c),'V':dim,'bracket_rank':b,'cyclic_rank':j,'loop_quotient':dim-b}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--multilinear-max',type=int,default=8);ap.add_argument('--binary-max',type=int,default=13);args=ap.parse_args()
    expect=json.loads((P/'EXPECTED_RESULTS.json').read_text());ref={tuple(x['content']):x for k in ('multilinear','binary') for x in expect[k]}
    cases=[]
    for n in range(2,args.multilinear_max+1):cases.append(('multilinear',(1,)*n))
    for n in range(2,args.binary_max+1):
        for a in range(n+1):cases.append(('binary',(a,n-a)))
    result=[]
    for group,c in cases:
        start=time.monotonic();row=check(c)
        assert all(row[k]==ref[c][k] for k in row),(row,ref[c])
        result.append({'group':group,**row})
        print(group,c,'PASS',round(time.monotonic()-start,3),flush=True)
        (ROOT/'INDEPENDENT_RANK_REPLAY.json').write_text(json.dumps({'status':'RUNNING','cases':result},indent=2)+'\n')
    (ROOT/'INDEPENDENT_RANK_REPLAY.json').write_text(json.dumps({'status':'PASS','method':'Independent raw-word primitive-integer elimination; no author imports','cases':result},indent=2)+'\n')
if __name__=='__main__':main()
