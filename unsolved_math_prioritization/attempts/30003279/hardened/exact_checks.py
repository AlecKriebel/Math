#!/usr/bin/env python3
"""Finite exact controls for the accompanying analytic report. No assert statements."""
import argparse
import copy
import itertools
import json
import math
from pathlib import Path

class CheckError(Exception):
    pass

COUNT = 0

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise CheckError('duplicate JSON key: '+key)
        out[key] = value
    return out

def reject_constant(value):
    raise CheckError('nonfinite JSON number: '+value)

def strict_json(text):
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)

def require(ok, message):
    global COUNT
    COUNT += 1
    if not ok:
        raise CheckError(message)

def integer(x):
    return type(x) is int

def factors(n):
    require(integer(n) and n > 0, 'factor input must be a positive integer')
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out

def norm(p):
    return p[0]*p[0]+p[1]*p[1]

def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])

def sub(a,b):
    return (a[0]-b[0],a[1]-b[1])

def admitted(n):
    f=factors(n)
    return n>1 and all(p%4==1 and e==1 for p,e in f.items())

def config(n, pts):
    require(integer(n) and n>0,'bad norm')
    require(type(pts) is list and len(pts)>=2,'bad point list')
    require(all(type(p) is list and len(p)==2 and all(integer(x) for x in p) for p in pts),'bad coordinates')
    require(len({tuple(p) for p in pts})==len(pts),'repeated points')
    require(all(norm(p)==n for p in pts),'unequal norms')

def triple(t):
    return [[4*t**3-1,2*t*t+2*t],[4*t**3,2*t*t+1],[4*t**3+1,2*t*t-2*t]]

def H(t):
    return 16*t**6+4*t**4+4*t*t+1

def fibs(n):
    f=[0,1]
    for i in range(2,n+1):
        f.append(f[-1]+f[-2])
    return f

def fib_config(u):
    f=fibs(3*u+3)
    require(f[3*u+3]%2==f[3*u]%2==0,'Fibonacci half parity')
    base=(f[3*u+3]//2,f[3*u]//2)
    w=[(-2*f[u-1],2*f[u+2]),(-f[u-2],f[u+1]),(f[u-1],-f[u+2]),(f[u],-f[u+3])]
    pts=[[base[0]+(-1)**u*a,base[1]+(-1)**u*b] for a,b in w]
    return 5*f[2*u-1]*f[2*u+1]*f[2*u+3]//2,pts

def prime_list(limit):
    return [n for n in range(2,limit+1) if all(n%p for p in range(2,math.isqrt(n)+1))]

def balanced(s,t):
    d=2*s
    B=math.prod(prime_list(2*d))
    pts=[]
    for positive in itertools.combinations(range(d),s):
        z=(1,0)
        for j in range(d):
            z=mul(z,(B*(t+j+1),1 if j in positive else -1))
        pts.append(list(z))
    n=math.prod((B*(t+j+1))**2+1 for j in range(d))
    return n,pts,B

def lattice(n):
    pts=[]
    for x in range(-math.isqrt(n),math.isqrt(n)+1):
        y2=n-x*x
        y=math.isqrt(y2)
        if y*y==y2:
            pts.append([x,y])
            if y:pts.append([x,-y])
    return pts

def triangle_check(pts,n):
    a,b,c=pts
    u,v=sub(b,a),sub(c,a)
    det=u[0]*v[1]-u[1]*v[0]
    require(det!=0 and det%2==0,'triangle area parity')
    prod=norm(sub(a,b))*norm(sub(a,c))*norm(sub(b,c))
    require(prod==4*det*det*n,'squared circumradius identity')
    require(prod>=16*n,'triangle product lower bound')

def vandermonde(pts,n):
    m=len(pts);M=m*(m-1)//2;E=(m-1)**2//4
    V=math.prod(norm(sub(a,b)) for a,b in itertools.combinations(pts,2))
    B=1
    for p in factors(n):
        root=next(x for x in range(p) if (x*x+1)%p==0)
        a=sum((z[0]-root*z[1])%p==0 for z in pts)
        require(all(not(z[0]%p==0 and z[1]%p==0) for z in pts),'zero isotropic vector')
        q=a*(a-1)//2+(m-a)*(m-a-1)//2
        require(q>=E,'balanced split minimum')
        B*=p**(q-E)
    divisor=2**M*n**E*B
    require(V%divisor==0,'Vandermonde divisibility')
    diameter2=max(norm(sub(a,b)) for a,b in itertools.combinations(pts,2))
    require(diameter2**M>=V>=divisor,'Vandermonde diameter bound')

def validate_claims(c):
    require(type(c) is dict,'claims must be an object')
    require(set(c)=={'problem_id','route_count','full_problem_solved','novelty_claim','all_triple_parameters_admissible','three_point_witness','four_point_witness','general_sample'},'claim schema')
    require(type(c['problem_id']) is int and c['problem_id']==30003279,'wrong problem')
    require(type(c['route_count']) is int and c['route_count']==5,'wrong route count')
    for key in ['full_problem_solved','novelty_claim','all_triple_parameters_admissible']:
        require(c[key] is False,'unsupported scope claim: '+key)
    a=c['three_point_witness']; require(type(a) is dict and set(a)=={'t','n','points'},'triple schema')
    require(type(a['t']) is int and a['t']>=1,'bad triple parameter')
    require(a['n']==H(a['t']) and a['points']==triple(a['t']),'wrong triple identity')
    config(a['n'],a['points']);require(admitted(a['n']),'inadmissible triple witness')
    b=c['four_point_witness'];require(type(b) is dict and set(b)=={'u','n','points'},'Fibonacci schema')
    require(type(b['u']) is int and b['u']>=2,'bad Fibonacci parameter')
    N,pts=fib_config(b['u']);require(N==b['n'] and pts==b['points'],'wrong Fibonacci identity')
    config(b['n'],b['points']);require(admitted(N),'inadmissible Fibonacci witness')
    g=c['general_sample'];require(type(g) is dict and set(g)=={'s','t','n','points'},'balanced schema')
    require(type(g['s']) is int and 2<=g['s']<=4 and type(g['t']) is int and g['t']>=1,'bad balanced parameter')
    N,pts,B=balanced(g['s'],g['t']);require(N==g['n'] and pts==g['points'],'wrong balanced identity')
    config(g['n'],g['points']);require(admitted(N),'inadmissible balanced witness')

def run(claims):
    validate_claims(claims)
    good=[]
    for t in range(1,501):
        pts=triple(t);n=H(t)
        config(n,pts);triangle_check(pts,n)
        qs=[4*t*t+1,2*t*t+2*t+1,2*t*t-2*t+1]
        require(math.prod(qs)==n,'factorization identity')
        ff={}
        for q in qs:
            for p,e in factors(q).items():
                require(p%4==1,'non-split triple prime')
                ff[p]=ff.get(p,0)+e
        if all(e==1 for e in ff.values()):good.append(t)
        require(norm(sub(pts[0],pts[2]))==16*t*t+4,'endpoint chord')
        require(norm(sub(pts[0],pts[1]))==4*t*t-4*t+2,'first chord')
        require(norm(sub(pts[1],pts[2]))==4*t*t+4*t+2,'second chord')
    for n in [5,13,17,65,85]:
        pts=lattice(n)
        require(len(pts)==4*2**len(factors(n)),'representation count')
        for tri in itertools.combinations(pts,3):triangle_check(tri,n)
    vcount=0
    pts=lattice(65)
    for m in range(3,9):
        for pp in itertools.combinations(pts,m):
            vandermonde(pp,65);vcount+=1
    for m in range(2,41):
        E=(m-1)**2//4
        require(min(a*(a-1)//2+(m-a)*(m-a-1)//2 for a in range(m+1))==E,'split formula')
    for u in range(2,101):
        n,pts=fib_config(u);config(n,pts)
        f=fibs(3*u+3)
        vals=[f[2*u-1],f[2*u+1],f[2*u+3]]
        require(all(math.gcd(a,b)==1 for a,b in itertools.combinations(vals,2)),'Fibonacci coprimality')
        even=[j for j,v in enumerate(vals) if v%2==0]
        require(len(even)==1 and vals[even[0]]%4==2,'Fibonacci valuation two')
        vals[even[0]]//=2
        require(5*math.prod(vals)==n,'Fibonacci odd factorization')
        require((all(v%5 for v in vals))==(u%5 in [0,4]),'Fibonacci mod-five exclusion')
        require(max(norm(sub(a,b)) for a,b in itertools.combinations(pts,2))==10*f[2*u+3],'Fibonacci diameter')
    for s in [2,3]:
        # Coefficients of each product are obtained exactly as pairs of integers.
        d=2*s;B=math.prod(prime_list(2*d));coeffs=[]
        for positive in itertools.combinations(range(d),s):
            poly=[(1,0)]
            for j in range(d):
                c=(B*(j+1),1 if j in positive else -1)
                new=[(0,0)]*(len(poly)+1)
                for k,v in enumerate(poly):
                    a=mul(v,c);new[k]=(new[k][0]+a[0],new[k][1]+a[1])
                    a=mul(v,(B,0));new[k+1]=(new[k+1][0]+a[0],new[k+1][1]+a[1])
                poly=new
            require(poly[-1]==(B**d,0),'balanced leading coefficient')
            require(poly[-2]==(B**d*d*(d+1)//2,0),'balanced next coefficient')
            coeffs.append(poly)
        require(len(coeffs)==math.comb(d,s),'balanced vector count')
        for t in range(1,21):
            n,pts,_=balanced(s,t);config(n,pts)
            for p in prime_list(2*d):require(n%p==1,'local prime avoidance')
    rejected=[]
    def reject(label,fn):
        try:fn()
        except (CheckError,ValueError,TypeError,KeyError):rejected.append(label)
        else:raise CheckError('false claim accepted: '+label)
    for key in ['full_problem_solved','novelty_claim','all_triple_parameters_admissible']:
        c=copy.deepcopy(claims);c[key]=True;reject(key,lambda c=c:validate_claims(c))
    c=copy.deepcopy(claims);c['three_point_witness']['points'][0][0]+=1;reject('altered triple point',lambda:validate_claims(c))
    c=copy.deepcopy(claims);c['three_point_witness']={'t':1,'n':25,'points':triple(1)};reject('nonsquarefree triple',lambda:validate_claims(c))
    c=copy.deepcopy(claims);c['four_point_witness']['n']//=fibs(9)[9];reject('missing middle Fibonacci factor',lambda:validate_claims(c))
    c=copy.deepcopy(claims);c['general_sample']['points'][1]=c['general_sample']['points'][0];reject('repeated balanced point',lambda:validate_claims(c))
    reject('boolean norm',lambda:config(True,[[1,0],[0,1]]))
    reject('floating coordinate',lambda:config(5,[[1.0,2],[2,1]]))
    reject('malformed point',lambda:config(5,[[1,2,3],[2,1]]))
    reject('unequal norms',lambda:config(5,[[1,2],[2,2]]))
    reject('negative norm',lambda:config(-5,[[1,2],[2,1]]))
    reject('malformed JSON',lambda:json.loads('{'))
    reject('missing claim key',lambda:validate_claims({}))
    require(len(rejected)==14,'negative control count')
    return {'verdict':'PASS_FINITE_EXACT_CONTROLS','explicit_checks':COUNT,'triple_parameters_checked':500,'squarefree_triple_parameters_found':len(good),'first_squarefree_parameters':good[:12],'vandermonde_subsets_checked':vcount,'fibonacci_parameters_checked':99,'negative_controls_rejected':rejected,'limitations':'Finite controls do not prove infinitude, the published sieve theorem, or full resolution.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--claims',type=Path,default=Path(__file__).resolve().with_name('CLAIMS.json'))
    args=p.parse_args()
    try:
        ans=run(strict_json(args.claims.read_text()))
    except (CheckError,ValueError,TypeError,KeyError,OSError) as e:
        print(json.dumps({'verdict':'FAIL','reason':str(e)},sort_keys=True));return 1
    print(json.dumps(ans,sort_keys=True,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
