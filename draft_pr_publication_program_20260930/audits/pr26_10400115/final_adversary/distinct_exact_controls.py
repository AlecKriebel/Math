#!/usr/bin/env python3
"""Fresh positive-cone/cyclic-reduction and polynomial-quotient controls.
Standard library only; no prior script or receipt is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
from datetime import datetime,timezone
from hashlib import sha256
from math import gcd
import json,sys
checks=Counter()
def check(k,v):
    if not v:raise AssertionError(k)
    checks[k]+=1
I=(1,0,0,1);S=(0,1,-1,0);R=(0,1,-1,1);C=(-1,0,0,1)
P=(1,1,0,1);Q=(1,0,1,1)
def mm(a,b):
    u,v,w,z=a;r,s,t,h=b
    return (u*r+v*t,u*s+v*h,w*r+z*t,w*s+z*h)
def neg(a):return tuple(-v for v in a)
def mi(a):
    u,v,w,z=a;d=u*z-v*w
    return (F(z,d),F(-v,d),F(-w,d),F(u,d))
def mp(a,n):
    if n<0:return mp(mi(a),-n)
    r=I
    for _ in range(n):r=mm(r,a)
    return r
def qm(w):
    out=I
    for f,n in w:out=mm(out,mp(S if f==2 else R,n))
    return out
def reduce(w):
    stack=[]
    for f,n in w:
        if stack and stack[-1][0]==f:n+=stack.pop()[1]
        n%=f
        if n:stack.append((f,n))
    return tuple(stack)
def iw(w):return tuple((f,-n) for f,n in reversed(w))
def cyclic(w):
    w=reduce(w);h=()
    while len(w)>1 and w[0][0]==w[-1][0]:
        first=w[0];w=reduce(w[1:]+(first,));h=h+(first,)
    if len(w)>1 and w[0][0]==3:
        first=w[0];w=w[1:]+(first,);h=h+(first,)
    return w,h
def stream(maxlength):
    yield ()
    for length in range(1,maxlength+1):
        for first in (2,3):
            fs=[first if i%2==0 else 5-first for i in range(length)]
            for exps in product(*[(1,) if f==2 else (1,2) for f in fs]):
                yield tuple(zip(fs,exps))
def scalar(m):return m[1]==m[2]==0 and m[0]==m[3]
def cone(w):
    reduced=reduce(w);c,h=cyclic(reduced)
    # Projective equality permits only a sign for these determinant-one matrices.
    transformed=mm(mm(mi(qm(h)),qm(reduced)),qm(h))
    check('tracked_cyclic_conjugacy',transformed==qm(c) or transformed==neg(qm(c)))
    if len(c)==1:
        check('factor_case_nonscalar',not scalar(qm(c)))
    elif c:
        check('cyclic_shape',len(c)%2==0 and c[0][0]==2 and c[-1][0]==3)
        pos=I
        for i in range(0,len(c),2):
            previous=sum(pos);pos=mm(pos,P if c[i+1][1]==1 else Q)
            check('positive_cone_strict_growth',sum(pos)>previous and all(v>=0 for v in pos) and pos[0]>=1 and pos[3]>=1)
        expected=mm(mm(C,qm(c)),C)
        if len(c)//2%2:expected=neg(expected)
        check('positive_cone_exact_block_identity',pos==expected)
        check('positive_cone_identity_exclusion',sum(pos)>2 and not scalar(pos))
    check('whole_word_projective_identity_equivalence',scalar(qm(reduced))==(not reduced))

check('orders',mp(S,2)==mp(R,3)==neg(I))
check('positive_block_one',neg(mm(mm(C,mm(S,R)),C))==P)
check('positive_block_two',neg(mm(mm(C,mm(S,mp(R,2))),C))==Q)
words=list(stream(10));conjugators=list(stream(5));conjugation_count=0;rotation_count=0
for w in words:
    cone(w)
    for cut in range(len(w)):
        rotated=reduce(w[cut:]+w[:cut]);cone(rotated)
        check('cyclic_rotation_trace',abs(qm(w)[0]+qm(w)[3])==abs(qm(rotated)[0]+qm(rotated)[3]))
        rotation_count+=1
    for h in conjugators:
        conjugated=reduce(h+w+iw(h));cone(conjugated)
        check('arbitrary_conjugation_trace',abs(qm(w)[0]+qm(w)[3])==abs(qm(conjugated)[0]+qm(conjugated)[3]))
        conjugation_count+=1
check('trace_only_mutant_rejected',mp(P,17)[0]+mp(P,17)[3]==2 and mp(P,17)!=I)
check('empty_after_relation_boundary',not reduce(((2,1),(2,1))) and scalar(qm(((2,1),(2,1)))))

def trim(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)
def pa(p,q):
    return trim((p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q))))
def ps(p,c):return trim(v*c for v in p)
def pm(p,q):
    if not p or not q:return ()
    a=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):a[i+j]+=x*y
    return trim(a)
def remainder(p,q):
    p=trim(p);q=trim(q)
    if not q:raise ZeroDivisionError
    while len(p)>=len(q):
        c=F(p[-1],q[-1]);n=len(p)-len(q)
        p=pa(p,ps((0,)*n+q,-c))
    return p
def qpow(a,n,p):
    out=(F(1),)
    for _ in range(n):out=remainder(pm(out,a),p)
    return out
def ladd(a,b):
    d=dict(a)
    for k,v in b.items():d[k]=d.get(k,0)+v
    return {k:v for k,v in d.items() if v}
def lg(a,b):return a[0]+b[0],ladd(a[1],{k+a[0]:v for k,v in b[1].items()})
def literal_construction(f):
    # Expanded signed D/b letters, independent of quotient or matrix arithmetic.
    out=(0,{})
    for k,c in sorted(f.items()):
        letters=[(1 if k>=0 else -1,{})]*abs(k)
        letters+=[(0,{0:1 if c>=0 else -1})]*abs(c)
        letters+=[(-1 if k>=0 else 1,{})]*abs(k)
        for a in letters:out=lg(out,a)
    return out
poly_count=0;shift_count=0;nonmonic=0
for degree in range(1,5):
    for ends in product((-2,-1,1,2),repeat=2):
        for middle in product((-2,-1,0,1,2),repeat=degree-1):
            p=(ends[0],)+middle+(ends[1],);poly_count+=1
            if abs(p[-1])!=1:nonmonic+=1
            x=remainder((0,F(1)),p)
            inverse=remainder(tuple(-F(v,p[0]) for v in p[1:]),p)
            check('quotient_X_inverse',remainder(pm(x,inverse),p)==(F(1),))
            for shift in (-9,-1,0,6):
                f={i+shift:int(v) for i,v in enumerate(p) if v}
                formal=literal_construction(f)
                check('arbitrary_polynomial_literal_word',formal==(0,f) and formal!=(0,{}))
                value=()
                for i,c in f.items():
                    power=qpow(x if i>=0 else inverse,abs(i),p)
                    value=remainder(pa(value,ps(power,c)),p)
                check('arbitrary_polynomial_quotient_annihilation',value==())
                shift_count+=1
# Zero constant is deliberately rejected for the inverse formula.
try:tuple(-F(v,0) for v in (1,1));zero_rejected=False
except ZeroDivisionError:zero_rejected=True
check('zero_parameter_domain_mutant_rejected',zero_rejected)
check('quotient_algebra_not_claimed_field',remainder(pm((-1,1),(1,1)),(-1,0,1))==() and remainder((-1,1),(-1,0,1))!=())

# Independent polynomial-array radical elimination and mod-3 irreducibility.
a=(4,2,2);b=(3,8,1)
eliminated=pa(ps(pm(a,a),2),ps(pm(b,b),-1))
check('radical_u_polynomial',eliminated==(23,-16,-30,0,7))
sub=();u=(-1,2);power=(1,)
for c in eliminated:
    sub=pa(sub,ps(power,c));power=pm(power,u)
minimal=(1,2,3,-14,7)
check('radical_x_polynomial',sub==ps(minimal,16))
f=(1,2,0,1,1)
def fmod(p,q):
    p=[v%3 for v in trim(p)];q=[v%3 for v in trim(q)]
    while p and len(p)>=len(q):
        c=p[-1]*pow(q[-1],-1,3)%3;n=len(p)-len(q)
        for i,v in enumerate(q):p[i+n]=(p[i+n]-c*v)%3
        p=list(trim(p))
    return tuple(p)
values=[sum(c*t**i for i,c in enumerate(f))%3 for t in range(3)]
check('mod3_no_linear_roots',values==[1,2,2])
irreducible=[]
for b0,b1 in product(range(3),repeat=2):
    q=(b0,b1,1)
    if all((t*t+b1*t+b0)%3 for t in range(3)):irreducible.append(q)
remainders=[fmod(f,q) for q in irreducible]
check('mod3_all_irreducible_quadratics',len(irreducible)==3 and all(remainders))
check('primitive_nonmonic_polynomial',gcd(*[abs(v) for v in minimal])==1 and minimal[-1]==7)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','assertions':sum(checks.values()),'checks_by_category':dict(checks),'quotient_words':len(words),'conjugators':len(conjugators),'cyclic_rotations':rotation_count,'arbitrary_conjugations':conjugation_count,'generated_integer_polynomial_types':poly_count,'nonmonic_types':nonmonic,'Laurent_shift_constructions':shift_count,'mod3_values':values,'irreducible_quadratics_low_first':[list(v) for v in irreducible],'mod3_remainders_low_first':[list(v) for v in remainders],'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'arithmetic':'Python stdlib exact integers/Fraction; no numerical roots, SymPy, companion matrices, or prior-script imports','scope':'Finite checks verify new implementations. Universal statements rest on the separate derivations. No higher-strand proof search, novelty claim, general nonexistence claim or new substantive attempt.'}
Path(__file__).with_name('DISTINCT_CONTROL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','assertions','quotient_words','cyclic_rotations','arbitrary_conjugations','generated_integer_polynomial_types','Laurent_shift_constructions']}))
