"""Independent finite diagnostic for the all-degree equivalence derived in REVIEW.md.
No third-party full text is embedded. Arithmetic is exact over F_2.
Run from any directory. The proof, not this finite diagnostic, establishes all degrees.
"""
from collections import Counter
from pathlib import Path
import json

# Polynomial represented by exponent tuple (x,y,u,v), coefficient in F_2.
def poly(*terms):
    c=Counter(terms)
    return {t for t,k in c.items() if k % 2 and min(t)>=0 and t[0]<2 and t[1]<2}

def add(*ps):
    return poly(*(t for p in ps for t in p))

def mul(p,q):
    return poly(*(tuple(a+b for a,b in zip(t,s)) for t in p for s in q))

def diff(p,i):
    out=[]
    for t in p:
        if t[i]%2:
            s=list(t);s[i]-=1;out.append(tuple(s))
    return poly(*out)

def bracket(p,q):
    return add(mul(diff(p,0),diff(q,2)),mul(diff(p,2),diff(q,0)),mul(diff(p,1),diff(q,3)),mul(diff(p,3),diff(q,1)))

def gen(n,q):
    if q==1 and n>=0:return poly((0,1,0,n))
    if q==2 and n>=0:return poly((1,1,0,n))
    if q==3 and n>=1:return poly((0,0,1,n-1))
    if q==4 and n>=1:return poly((1,0,1,n-1))
    return set()

def scale(k,p):return p if k%2 else set()

def require(a,b,tag):
    if a!=b:raise RuntimeError((tag, sorted(a), sorted(b)))

LIMIT=12
counts={'ring_relations':0,'bracket_relations':0,'basis_checks':0}
def ring(a,b,tag):
    require(a,b,tag);counts['ring_relations']+=1

def lie(a,b,tag):
    require(a,b,tag);counts['bracket_relations']+=1

for m in range(LIMIT+1):
 for n in range(LIMIT+1):
    for q,r in [(1,1),(1,2),(2,2)]:ring(mul(gen(m,q),gen(n,r)),set(),(m,n,q,r))
    if n>=1:
        ring(mul(gen(m,2),gen(n,4)),set(),('2*4',m,n))
        ring(mul(gen(m,2),gen(n,3)),mul(gen(m,1),gen(n,4)),('23=14',m,n))
    if m>=1 and n>=1:
        ring(mul(gen(m,4),gen(n,4)),set(),('4*4',m,n))
        for q in (3,4):ring(mul(gen(m,1),gen(n,q)),mul(gen(0,1),gen(m+n,q)),('1*q',m,n,q))
        if m>=2:
            for q in (3,4):ring(mul(gen(m,3),gen(n,q)),mul(gen(1,3),gen(m+n-1,q)),('3*q',m,n,q))
        s=m+n-1
        for q in (1,2):lie(bracket(gen(m,1),gen(n,q)),scale(m+n,gen(s,q)),('11/12',m,n,q))
        for q in (3,4):lie(bracket(gen(m,1),gen(n,q)),scale(n-1,gen(s,q)),('13/14',m,n,q))
        lie(bracket(gen(m,2),gen(n,2)),set(),('22',m,n))
        lie(bracket(gen(m,2),gen(n,4)),gen(s,2),('24',m,n))
        lie(bracket(gen(m,2),gen(n,3)),add(gen(s,1),scale(n-1,gen(s,4))),('23',m,n))
        lie(bracket(gen(m,3),gen(n,3)),set(),('33',m,n))
        lie(bracket(gen(m,4),gen(n,3)),gen(s,3),('43',m,n))
        lie(bracket(gen(m,4),gen(n,4)),set(),('44',m,n))
for m in range(1,LIMIT+1):
    for q in (1,2):lie(bracket(gen(m,q),gen(0,1)),scale(m,gen(m-1,q)),('q,01',m,q))
    for q in (3,4):lie(bracket(gen(m,q),gen(0,1)),scale(m-1,gen(m-1,q)),('q,01',m,q))
    lie(bracket(gen(m,1),gen(0,2)),scale(m,gen(m-1,2)),('1,02',m))
    lie(bracket(gen(m,2),gen(0,2)),set(),('2,02',m))
    lie(bracket(gen(m,3),gen(0,2)),add(gen(m-1,1),scale(m-1,gen(m-1,4))),('3,02',m))
    lie(bracket(gen(m,4),gen(0,2)),gen(m-1,2),('4,02',m))

# Images of the paper's normal basis, organized by degree, are exactly L's monomials.
for d in range(LIMIT+1):
    images=[poly((0,0,0,0))] if d==0 else []
    images += [gen(d,1),gen(d,2)]
    if d>=1:
        images += [gen(d,3),gen(d,4)]
        for l in range(d):
            n=d-l
            images += [mul(gen(0,1),mul(poly((0,0,l,0)),gen(n,q))) for q in (3,4)]
        # Normal-basis higher-u family indexed separately by degree l+1+n.
        for n in range(1,d):
            power=d-n
            images += [mul(poly((0,0,power,0)),gen(n,q)) for q in (3,4)]
    monomials=set().union(*images)
    if len(monomials)!=len(images) or any(len(p)!=1 for p in images):
        raise RuntimeError(('normal-basis images not distinct monomials',d))
    expected={(a,b,i,d-i) for a in (0,1) for b in (0,1) for i in range(d+1) if i>=1 or b==1}
    if d==0:expected.add((0,0,0,0))
    require(monomials,expected,('degree-basis',d));counts['basis_checks']+=1

result={'status':'PASS','exact_field':'F_2','degree_index_bound':LIMIT,'counts':counts,'scope':'finite diagnostic only; all-degree algebraic proof in REVIEW.md','generator_map':{'X_n1':'y*v^n','X_n2':'x*y*v^n','X_n3':'u*v^(n-1)','X_n4':'x*u*v^(n-1)'}}
Path(__file__).with_name('COMPARISON_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
