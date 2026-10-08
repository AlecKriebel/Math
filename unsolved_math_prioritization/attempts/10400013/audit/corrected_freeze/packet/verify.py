#!/usr/bin/env python3
"""Exact finite author diagnostics. No assert statements; no external dependencies."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import json, sys

class CheckError(Exception): pass
COUNTS={}
def require(ok, label):
    if not ok: raise CheckError(label)
    COUNTS[label.split(':')[0]]=COUNTS.get(label.split(':')[0],0)+1

def strict_object(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise CheckError('duplicate JSON key')
        d[k]=v
    return d

def load(path):
    return json.loads(Path(path).read_text(),object_pairs_hook=strict_object,
                      parse_constant=lambda s: (_ for _ in ()).throw(CheckError('nonfinite JSON')))

def clean(p): return {k:v for k,v in p.items() if v}
def add(p,q):
    r=dict(p)
    for k,v in q.items():r[k]=r.get(k,0)+v
    return clean(r)
def scale(p,c):return clean({k:c*v for k,v in p.items()})
def mul(p,q):
    r={}
    for a,x in p.items():
        for b,y in q.items():
            k=tuple(i+j for i,j in zip(a,b));r[k]=r.get(k,0)+x*y
    return clean(r)
def power(p,n):
    if n<0:
        if len(p)!=1:raise CheckError('negative power requires monomial')
        k,v=next(iter(p.items()))
        if v not in (1,-1):raise CheckError('nonunit monomial')
        return {tuple(i*n for i in k):(1 if v == 1 or n % 2 == 0 else -1)}
    k=next(iter(p)) if p else (0,)
    r={tuple(0 for _ in k):1}
    for _ in range(n):r=mul(r,p)
    return r
def mono(k,c=1):return {tuple(k):c} if c else {}
def span(p,axis=0):return max(k[axis] for k in p)-min(k[axis] for k in p)
def deriv1(p,n=1):
    r=0
    for (k,),v in p.items():
        z=1
        for i in range(n):z*=k-i
        r+=z*v
    return r
def evalat(p,x):return sum(v*x**k[0] for k,v in p.items())
def substitute(p,images):
    r={}
    for exps,c in p.items():
        term=mono((0,)*len(next(iter(images[0]))),c)
        for e,z in zip(exps,images):term=mul(term,power(z,e))
        r=add(r,term)
    return r

def remainder(p,mod):
    # Used only for ordinary univariate polynomials and monic moduli.
    p=dict(p);d=max(k[0] for k in mod)
    while p and max(k[0] for k in p)>=d:
        e=max(k[0] for k in p);v=p[(e,)]
        p=add(p,scale(mul(mod,mono((e-d,))),-v))
    return p

def matmul(a,b):
    return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]
def matpow(a,n):
    r=[[mono((0,)),{}],[{},mono((0,))]]
    for _ in range(n):r=matmul(r,a)
    return r

def tlmul(x,y,delta):
    return (mul(x[0],y[0]), add(add(mul(x[0],y[1]),mul(x[1],y[0])),mul(mul(x[1],y[1]),delta)))
def tlpow(x,n,delta):
    r=(mono((0,)),{})
    for _ in range(n):r=tlmul(r,x,delta)
    return r

def main():
    root=Path(__file__).resolve().parent
    require(len(sys.argv) in (1,3),'cli:arity')
    require(len(sys.argv)==1 or sys.argv[1]=='--claims','cli:flag')
    claims=load(root/'CLAIMS.json' if len(sys.argv)==1 else sys.argv[2])
    expected={'schema':'fixed-span-claims-v1','problem_id':10400013,'rank':1009,'problem_number':'AMR-103-0013','status':'unsolved','approaches':5,'full_resolution':False,'knot_counterexample':False,'link_jones_counterexample_credited':True,'traczyk_components':2,'traczyk_span':2,'fixed_braid_index_required':True,'fixed_adequate_diagram_genus_required':True,'fixed_twist_exterior_required':True,'formal_specializations_are_realized':False,'novelty_claimed':False,'independent_audit_completed':False,'finite_checks_are_proof':False}
    require(type(claims) is dict and set(claims)==set(expected),'claims:keys')
    for k,v in expected.items():require(type(claims[k]) is type(v) and claims[k]==v,'claims:'+k)
    one=mono((0,)); t=mono((1,))
    for d in range(5):
        for a in product(range(-2,3),repeat=d+1):
            if not a[0] or not a[-1] or sum(a)!=1:continue
            m=-sum(j*v for j,v in enumerate(a));p={(m+j,):v for j,v in enumerate(a) if v}
            require(evalat(p,Fraction(1))==1 and deriv1(p)==0,'normalization:identities')
            require(abs(m)<=2*d*(d+1)//2,'normalization:bound')
    # Residue sums prove the small-span diagnostic in this finite window.
    for m in range(-15,16):
        for d in range(3):
            for a in product(range(-3,4),repeat=d+1):
                if not a[0] or not a[-1] or sum(a)!=1:continue
                b=[sum(v for j,v in enumerate(a) if (m+j)%3==r) for r in range(3)]
                if b[0]-b[2]!=1 or b[1]-b[2]!=0:continue
                require(b==[1,0,0],'low_span:residues')
                if sum((m+j)*v for j,v in enumerate(a))==0:
                    require(d==0 and m==0 and a==(1,),'low_span:only_constant')
    h=one
    for f in [{(2,):1,(1,):-2,(0,):1},{(2,):1,(1,):2,(0,):1},{(2,):1,(0,):1},{(2,):1,(1,):1,(0,):1},{(2,):1,(1,):-1,(0,):1}]:h=mul(h,f)
    require(h=={(10,):1,(6,):-1,(4,):-1,(0,):1},'formal_jones:factorization')
    for n in range(1,51):
        p=add(one,scale(h,n))
        require(span(p)==10 and evalat(p,1)==1 and deriv1(p)==0,'formal_jones:span_normalization')
        require(evalat(p,-1)==1 and deriv1(p,2)==48*n,'formal_jones:determinant_derivative')
        for mod in [{(2,):1,(0,):1},{(2,):1,(1,):1,(0,):1},{(2,):1,(1,):-1,(0,):1}]:
            require(remainder(p,mod)==one,'formal_jones:root_remainder')
    a=[[mono((1,),-1),one],[{},one]];b=[[one,{}],[t,mono((1,),-1)]]
    d=matmul(matmul(a,b),a)
    require(d==matmul(matmul(b,a),b),'burau:braid_relation')
    require(d==[[{},mono((1,),-1)],[mono((2,),-1),{}]],'burau:delta')
    require(matmul(d,d)==[[mono((3,)),{}],[{},mono((3,))]],'burau:square')
    for n in range(30):
        q=matpow(d,2*n+1)
        require(add(q[0][0],q[1][1])=={},'burau:odd_trace')
        # x=sqrt(t), hence the t-span is half the x-span.
        v={(6*n+1,):-1,(6*n+5,):-1}
        require(span(v)==4 and min(k[0] for k in v)==6*n+1,'burau:link_span_shift')
    for s in range(26):
        delta=Fraction(4,(s+2)*(s+3))
        for r in range(3,s+4):
            for q in range(r+1,s+4):
                gap=Fraction(1,r)-Fraction(1,q)
                require(Fraction(1,(s+2)*(s+3))<=gap<=Fraction(1,3),'interpolation:rational_separation')
                require(4*gap>=delta,'interpolation:chord_lower_bound_input')
    # Lagrange interpolation exact coefficient replay at distinct rational nodes.
    for s in range(8):
        p={(j,):(-1)**j*(j+1) for j in range(s+1)};rec={}
        for r in range(s+1):
            basis=one;den=1
            for q in range(s+1):
                if q!=r:basis=mul(basis,{(1,):1,(0,):-q});den*=r-q
            rec=add(rec,scale(basis,Fraction(evalat(p,r),den)))
        require(rec==p,'interpolation:exact_lagrange_identity')
    for c in range(1,41):
        for va in range(1,c+2):
            for vb in range(1,c+2):
                z=2+c-va-vb
                if z<0 or z%2:continue
                g=z//2;st=Fraction(2*c+2*va+2*vb-4,4)
                require(st==c-g,'adequacy:state_genus_identity')
                for j in (1,2,3):
                    require(c-2*j+2*(va+j-2-1)==c+2*va-6,'adequacy:strict_state_drop')
    delta={(2,):-1,(-2,):-1};T=(t,mono((-1,)));Ti=(mono((-1,)),t)
    require(tlmul(T,Ti,delta)==(one,{}),'twist:inverse')
    for n in range(-24,25):
        z=tlpow(T if n>=0 else Ti,abs(2*n),delta)
        left=(mul(delta,z[0]),mul(delta,z[1]))
        right=(mul(delta,mono((2*n,))),add(mono((-6*n,)),mono((2*n,),-1)))
        require(left==right,'twist:full_twist_spectral_identity')
    for u,v in [(-4,-12),(8,0)]:
        for n in range(-30,31):
            if 8*abs(n)<=8:continue
            p={(u*n-4,):2,(u*n+3,):-1};q={(v*n-2,):1,(v*n+4,):3}
            require(span(add(p,q))>=8*abs(n)-8,'twist:separated_support')
    l=mono((1,0));mi=mono((0,1));o=mono((0,0));l2=power(l,2);lm2=power(l,-2)
    R=add(add(power(mi,4),scale(power(mi,2),4)),add(scale(o,2),scale(add(l2,lm2),-1)))
    S=add(power(mi,2),scale(add(add(l2,lm2),scale(o,-2)),-1))
    perturb=mul(mul(add(l2,scale(o,-1)),power(mi,2)),mul(R,S))
    xx=mono((1,));xin=mono((-1,));jimages=[power(xx,2),add(xx,scale(xin,-1))]
    fvar=mono((1,0));zvar=mono((0,1));TT=add(add(power(zvar,3),scale(zvar,-3)),add(fvar,power(fvar,-1)))
    fp=mul(mul(power(add(fvar,scale(power(fvar,-1),-1)),2),power(zvar,2)),power(TT,2))
    for n in range(1,21):
        pp=add(o,scale(perturb,n));ff=add(o,scale(fp,n))
        require((span(pp,0),span(pp,1))==(10,8),'specialization:homfly_spans')
        require(substitute(pp,jimages)==one,'specialization:homfly_jones')
        require(substitute(pp,[one,xx])==one,'specialization:homfly_alexander')
        require(substitute(pp,[xx,add(xin,scale(xx,-1))])==one,'specialization:homfly_unit_curve')
        require(all(i%2==0 and j%2==0 for i,j in pp),'specialization:homfly_parity')
        require((span(ff,0),span(ff,1))==(8,8),'specialization:kauffman_spans')
        require(substitute(ff,[mono((-3,),-1),add(xx,xin)])==one,'specialization:kauffman_jones')
        require(substitute(ff,[one,xx])==one,'specialization:kauffman_q')
        require(all((i+j)%2==0 for i,j in ff),'specialization:kauffman_parity')
    return {'schema':'fixed-span-diagnostics-v1','status':'PASS','problem_id':10400013,'approaches':5,'checks':sum(COUNTS.values()),'categories':COUNTS,'scope':'Exact finite algebra diagnostics; not a general knot-polynomial proof certificate.'}

if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (CheckError,OSError,ValueError,TypeError,KeyError,ZeroDivisionError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
