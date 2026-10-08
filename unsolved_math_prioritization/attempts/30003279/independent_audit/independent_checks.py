#!/usr/bin/env python3
"""Independent exact controls. Standard library only; no author-module imports."""
import argparse
from fractions import Fraction
from functools import cmp_to_key
import itertools
import json
import math
from pathlib import Path

class AuditError(Exception): pass
CHECKS = 0

def need(value, message):
    global CHECKS
    CHECKS += 1
    if not value: raise AuditError(message)

def obj(pairs):
    out = {}
    for k,v in pairs:
        if k in out: raise AuditError('duplicate JSON key')
        out[k]=v
    return out

def bad_constant(x): raise AuditError('nonfinite JSON number')

def parse(text): return json.loads(text, object_pairs_hook=obj, parse_constant=bad_constant)

def poly(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)

def add(a,b): return poly([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return poly(out)
def ev(a,t):
    z=0
    for c in reversed(a): z=z*t+c
    return z

def det(A):
    A=[[Fraction(x) for x in r] for r in A]; out=Fraction(1)
    for j in range(len(A)):
        k=next((k for k in range(j,len(A)) if A[k][j]),None)
        if k is None:return 0
        if k!=j:A[j],A[k]=A[k],A[j];out=-out
        p=A[j][j];out*=p
        for i in range(j+1,len(A)):
            q=A[i][j]/p
            for k in range(j,len(A)):A[i][k]-=q*A[j][k]
    need(out.denominator==1,'nonintegral determinant')
    return out.numerator

def resultant(a,b):
    m=len(a)-1;n=len(b)-1;aa=list(reversed(a));bb=list(reversed(b))
    return det([[0]*i+aa+[0]*(n-1-i) for i in range(n)]+[[0]*i+bb+[0]*(m-1-i) for i in range(m)])

def factors(n):
    need(type(n) is int and n>0,'factor domain')
    f={};p=2
    while p*p<=n:
        while n%p==0:f[p]=f.get(p,0)+1;n//=p
        p+=1 if p==2 else 2
    if n>1:f[n]=f.get(n,0)+1
    return f

def admitted(n):return n>1 and all(p%4==1 and e==1 for p,e in factors(n).items())
def norm(z):return z[0]**2+z[1]**2
def dif(z,w):return (z[0]-w[0],z[1]-w[1])
def prod(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def np(z):return add(mul(z[0],z[0]),mul(z[1],z[1]))
def cp(z,w):return (sub(mul(z[0],w[0]),mul(z[1],w[1])),add(mul(z[0],w[1]),mul(z[1],w[0])))
def cfg(n,points):
    need(type(n) is int and n>1,'norm type')
    need(type(points) is list and len(points)>=3,'point list type')
    need(all(type(p) is list and len(p)==2 and all(type(x) is int for x in p) for p in points),'coordinate type')
    need(len(set(map(tuple,points)))==len(points),'duplicate point')
    need(all(norm(p)==n for p in points),'norm mismatch')

def validate(c):
    need(type(c) is dict and set(c)=={'problem_id','route_count','full_problem_solved','novelty_claim','all_triple_parameters_admissible','three_point_witness','four_point_witness','general_sample'},'claim schema')
    need(type(c['problem_id']) is int and c['problem_id']==30003279,'problem id')
    need(type(c['route_count']) is int and c['route_count']==5,'route count')
    need(all(c[k] is False for k in ['full_problem_solved','novelty_claim','all_triple_parameters_admissible']),'scope')
    for name,keys in [('three_point_witness',{'t','n','points'}),('four_point_witness',{'u','n','points'}),('general_sample',{'s','t','n','points'})]:
        x=c[name];need(type(x) is dict and set(x)==keys,'witness schema')
        for k in keys-{'points'}:need(type(x[k]) is int,'witness integer type')
        cfg(x['n'],x['points']);need(admitted(x['n']),'inadmissible witness')
    need(c['three_point_witness']['t']>=1 and c['four_point_witness']['u']>=2 and c['general_sample']['s']>=2 and c['general_sample']['t']>=1,'parameter domain')

def lattice(n):
    out=[]
    for x in range(-math.isqrt(n),math.isqrt(n)+1):
        y=math.isqrt(n-x*x)
        if x*x+y*y==n:
            out.append((x,y))
            if y:out.append((x,-y))
    return out

def polar_cmp(a,b):
    h=lambda p:0 if p[1]>0 or (p[1]==0 and p[0]>0) else 1
    if h(a)!=h(b):return -1 if h(a)<h(b) else 1
    cross=a[0]*b[1]-a[1]*b[0]
    return -1 if cross>0 else 1 if cross<0 else 0

def controls(c):
    validate(c)
    qs=[(1,0,4),(1,2,2),(1,-2,2)];H=mul(mul(qs[0],qs[1]),qs[2])
    need(H==(1,0,4,0,4,0,16),'triple norm polynomial')
    need([q[1]**2-4*q[0]*q[2] for q in qs]==[-16,-4,-4],'quadratic discriminants')
    need([resultant(qs[i],qs[j]) for i,j in [(0,1),(0,2),(1,2)]]==[20,20,32],'resultants')
    need(ev(H,0)==1,'fixed-prime obstruction')
    P=[((-1,0,0,4),(0,2,2)),((0,0,0,4),(1,0,2)),((1,0,0,4),(0,-2,2))]
    for z in P:need(np(z)==H,'symbolic common norm')
    need([np((sub(P[j][0],P[i][0]),sub(P[j][1],P[i][1]))) for i,j in [(0,1),(1,2),(0,2)]]==[(2,-4,4),(2,4,4),(4,0,16)],'symbolic squared distances')
    u=(sub(P[1][0],P[0][0]),sub(P[1][1],P[0][1]));v=(sub(P[2][0],P[0][0]),sub(P[2][1],P[0][1]))
    need(sub(mul(u[0],v[1]),mul(u[1],v[0]))==(-2,),'triple area exactly one')
    need(Fraction(16**3,H[-1])==16**2,'exact limiting constant squared-cube')
    triple_good=[]
    for t in range(1,1001):
        f={}
        for q in qs:
            for p,e in factors(ev(q,t)).items():
                need(p%4==1,'nonsplit prime in triple');f[p]=f.get(p,0)+e
        need(math.gcd(t,t+1)==math.gcd(t,t-1)==1,'primitive components')
        if all(e==1 for e in f.values()):triple_good.append(t)
    need(1 not in triple_good and 2 in triple_good,'admissibility counter-control')
    a=c['three_point_witness'];need(a['n']==ev(H,a['t']) and a['points']==[[ev(x,a['t']),ev(y,a['t'])] for x,y in P],'input triple formula')
    triangles=0
    for n in range(1,151):
        for a,b,d in itertools.combinations(lattice(n),3):
            u=dif(b,a);v=dif(d,a);area2=u[0]*v[1]-u[1]*v[0]
            need(area2!=0 and area2%2==0,'circle triangle parity')
            sides=[norm(dif(a,b)),norm(dif(a,d)),norm(dif(b,d))]
            need(math.prod(sides)==4*n*area2**2,'exact circumradius');triangles+=1
    prime_cases=0
    for p in range(5,501,4):
        if factors(p)!={p:1}:continue
        ps=sorted(lattice(p),key=cmp_to_key(polar_cmp));need(len(ps)==8,'prime representation count')
        for j,a in enumerate(ps):
            b=ps[(j+2)%8];need(a[0]*b[0]+a[1]*b[1]==0 and a[0]*b[1]-a[1]*b[0]==p,'three consecutive prime-radius points span quarter-circle')
        prime_cases+=1
    vandermonde_subsets=0
    for n in [5,13,65,85]:
        ps=lattice(n);ff=factors(n)
        roots={p:next(r for r in range(p) if (r*r+1)%p==0) for p in ff}
        for m in range(3,min(7,len(ps))+1):
            M=math.comb(m,2);E=(m-1)**2//4
            for subpts in itertools.combinations(ps,m):
                excess=1
                for p,r in roots.items():
                    a=sum((x-r*y)%p==0 for x,y in subpts)
                    q=math.comb(a,2)+math.comb(m-a,2)
                    excess*=p**(q-E)
                squares=[norm(dif(a,b)) for a,b in itertools.combinations(subpts,2)]
                V=math.prod(squares);divisor=2**M*n**E*excess
                need(V%divisor==0 and max(squares)**M>=V,'Gaussian product divisor and bound');vandermonde_subsets+=1
    for m in range(2,201):
        s=m//2;E=(m-1)**2//4
        need(min(math.comb(a,2)+math.comb(m-a,2) for a in range(m+1))==E,'balanced minimum')
        for a in range(m+1):need(math.comb(a,2)+math.comb(m-a,2)-E==((a-s)**2 if m%2==0 else (a-s)*(a-s-1)),'imbalance formula')
    fs=[0,1]
    for j in range(2,904):fs.append(fs[-1]+fs[-2])
    for u in range(2,301):
        raw=[fs[2*u-1],fs[2*u+1],fs[2*u+3]]
        need(all(math.gcd(a,b)==1 for a,b in itertools.combinations(raw,2)),'Fibonacci coprimality')
        even=[v for v in raw if v%2==0];need(len(even)==1 and even[0]%4==2,'Fibonacci two-valuation')
        gs=[v//2 if v%2==0 else v for v in raw];n=5*math.prod(gs)
        need(all(v%2 for v in gs),'Fibonacci odd factors')
        need(all(v%5 for v in gs)==(u%5 in [0,4]),'Fibonacci five-avoidance')
        ws=[(-2*fs[u-1],2*fs[u+2]),(-fs[u-2],fs[u+1]),(fs[u-1],-fs[u+2]),(fs[u],-fs[u+3])]
        pts=[[fs[3*u+3]//2+(-1)**u*x,fs[3*u]//2+(-1)**u*y] for x,y in ws]
        cfg(n,pts);need(max(norm(dif(a,b)) for a,b in itertools.combinations(pts,2))==10*fs[2*u+3],'Fibonacci diameter')
        if u==c['four_point_witness']['u']:need(n==c['four_point_witness']['n'] and pts==c['four_point_witness']['points'],'input Fibonacci formula')
    balanced_vectors=0
    for s in [2,3,4]:
        d=2*s;small=[p for p in range(2,2*d+1) if factors(p)=={p:1}];B=math.prod(small);Q=(1,)
        for j in range(1,d+1):Q=mul(Q,(B*B*j*j+1,2*B*B*j,B*B))
        polynomials=[]
        for choices in itertools.combinations(range(1,d+1),s):
            z=((1,),(0,))
            for j in range(1,d+1):z=cp(z,((B*j,B),(1 if j in choices else -1,)))
            need(np(z)==Q,'balanced symbolic norm')
            need(len(z[0])==d+1 and z[0][-1]==B**d and z[0][-2]==B**d*d*(d+1)//2,'balanced real leading coefficients')
            need(len(z[1])<=d-1,'balanced imaginary cancellation')
            polynomials.append(z);balanced_vectors+=1
        for z,w in itertools.combinations(polynomials,2):need(max(len(sub(z[0],w[0])),len(sub(z[1],w[1])))<=d-1,'balanced difference degree')
        for p in small:need(Q[0]%p==1 and all(a%p==0 for a in Q[1:]),'local small-prime avoidance')
        if s==c['general_sample']['s']:
            t=c['general_sample']['t'];pts=[[ev(x,t),ev(y,t)] for x,y in polynomials]
            need(ev(Q,t)==c['general_sample']['n'] and pts==c['general_sample']['points'],'input balanced formula')
    return {'verdict':'PASS_INDEPENDENT_EXACT_CONTROLS','checks':CHECKS,'symbolic_triple_norm_distance_area_resultant_checks':True,'triple_parameters':1000,'squarefree_triple_parameters':len(triple_good),'first_squarefree_triple_parameters':triple_good[:12],'triangle_configurations':triangles,'prime_radius_cases':prime_cases,'vandermonde_subsets':vandermonde_subsets,'imbalance_cardinalities':199,'fibonacci_parameters':299,'balanced_symbolic_vectors':balanced_vectors,'limitations':'Exact controls support, but do not replace, universal arguments or the published squarefree-value theorem.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--claims',type=Path,required=True);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
    try:
        c=parse(a.claims.read_text());validate(c) if a.validate_only else None
        result={'verdict':'PASS_STRICT_CLAIMS'} if a.validate_only else controls(c)
    except (AuditError,ValueError,TypeError,KeyError,OSError,OverflowError) as e:
        print(json.dumps({'verdict':'FAIL','reason':str(e)},sort_keys=True));return 1
    print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
