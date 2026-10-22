#!/usr/bin/env python3
"""Independent exact audit; Python standard library only, no author-code imports.

The mathematical implications are explained in FULL_AUDIT.md. This checks their
finite arithmetic inputs, not modularity, theorem truth, or source authenticity.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

PIN = '7162a7e1927ccaaf5454fde977da28f50d910ed695931e08431eb77d9a878991'
F = {713: [1,-4,2,2,1,-2,1], 893: [1,-2,-3,-2,-2,0,1]}
H = {713: [1,0,-1,1], 893: [1,1,0,1]}
G = {713: [0,-1,1], 893: [0,-1,-1,-1,-1]}
PRIMES = (2,3,5,7,11,13,17,29,37,41)

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def strict_json(path):
    def obj(pairs):
        out = {}
        for k,v in pairs:
            require(k not in out, 'duplicate JSON key: '+k)
            out[k] = v
        return out
    def invalid(value):
        raise ValueError('nonfinite JSON value: '+value)
    return json.loads(Path(path).read_text(), object_pairs_hook=obj,
                      parse_constant=invalid)

def same(a,b,label):
    require(json.dumps(a,sort_keys=True,separators=(',',':')) ==
            json.dumps(b,sort_keys=True,separators=(',',':')), label)

def trim(a):
    a = list(a)
    while len(a)>1 and a[-1]==0:
        a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a): c[i]+=v
    for i,v in enumerate(b): c[i]+=v
    return trim(c)

def pmul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b): c[i+j]+=v*w
    return trim(c)

def derivative(a):
    return trim([i*a[i] for i in range(1,len(a))] or [0])

def rem(a,b,p):
    a=trim([v%p for v in a]); b=trim([v%p for v in b])
    require(b != [0], 'zero polynomial divisor')
    while a != [0] and len(a)>=len(b):
        n=len(a)-len(b); q=a[-1]*pow(b[-1],-1,p)%p
        for j,v in enumerate(b): a[n+j]=(a[n+j]-q*v)%p
        a=trim(a)
    return a

def gcd(a,b,p):
    while trim(b) != [0]: a,b=b,rem(a,b,p)
    return [(v*pow(a[-1],-1,p))%p for v in a]

def ppow(a,n,f,p):
    r=[1]
    while n:
        if n&1: r=rem(pmul(r,a),f,p)
        a=rem(pmul(a,a),f,p); n//=2
    return r

def irreducible(f,p):
    f=trim([v%p for v in f]); n=len(f)-1
    if n<1: return False
    x=[0,1]; xp=x
    for k in range(1,n+1):
        xp=ppow(xp,p,f,p)
        difference=add(xp,[0,-1])
        if k<=n//2 and len(gcd(f,difference,p))>1: return False
    return rem(add(xp,[0,-1]),f,p)==[0]

def determinant(a):
    a=[list(r) for r in a]; sign=1; previous=1; n=len(a)
    for k in range(n-1):
        if a[k][k]==0:
            row=next((i for i in range(k+1,n) if a[i][k]),None)
            if row is None: return 0
            a[k],a[row]=a[row],a[k]; sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value=a[i][j]*pivot-a[i][k]*a[k][j]
                require(value%previous==0, 'Bareiss exact division')
                a[i][j]=value//previous
        for i in range(k+1,n): a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]

def resultant(f,g):
    m=len(f)-1; n=len(g)-1; a=[]
    for i in range(n): a.append([0]*i+list(reversed(f))+[0]*(n-i-1))
    for i in range(m): a.append([0]*i+list(reversed(g))+[0]*(m-i-1))
    return determinant(a)

def evaluate(f,x,p):
    r=0
    for a in reversed(f): r=(r*x+a)%p
    return r

def extension(p):
    # Deliberately different from the author's u^2=d basis: u^2+u+c=0.
    c=next(c for c in range(p) if all((x*x+x+c)%p for x in range(p)))
    def mul(x,y):
        a,b=x%p,x//p; d,e=y%p,y//p
        return (a*d-c*b*e)%p+p*((a*e+b*d-b*e)%p)
    def plus(x,y): return (x%p+y%p)%p+p*((x//p+y//p)%p)
    def ev(f,x):
        r=0
        for v in reversed(f): r=plus(mul(r,x),v%p)
        return r
    return mul,plus,ev,c

def count_curve(N,p,r):
    if r==1:
        if p==2:
            return 2+sum((y*y+evaluate(H[N],x,p)*y-evaluate(G[N],x,p))%p==0
                         for x in range(p) for y in range(p))
        squares=Counter(y*y%p for y in range(p))
        return 2+sum(squares[evaluate(F[N],x,p)] for x in range(p))
    mul,plus,ev,c=extension(p); q=p*p
    if p==2:
        return 2+sum(plus(mul(y,y),mul(ev(H[N],x),y))==ev(G[N],x)
                     for x in range(q) for y in range(q))
    squares=Counter(mul(y,y) for y in range(q))
    return 2+sum(squares[ev(F[N],x)] for x in range(q))

def laurent_mul(a,b):
    c=Counter()
    for i,v in a.items():
        for j,w in b.items(): c[i+j]+=v*w
    return {i:v for i,v in c.items() if v}

def theta(a,b):
    # Each row gives the coefficients of alpha and beta, in source order.
    matrix=((0,1),(0,2),(1,1),(-1,1),(1,2),(2,0),(1,0),(0,4),
            (2,3),(1,3),(0,3),(-1,3),(2,2),(0,2),(-1,2),(-2,2),
            (2,1),(1,1),(0,1),(-1,1),(-2,1),(1,0),(0,0),(0,0))
    d=[abs(u*a+v*b) for u,v in matrix]
    c=[5,3,3,3,2,2,2]+[1]*17; e=[x*y for x,y in zip(c,d)]
    k=d.count(0); m=math.prod(x for x,y in zip(c,d) if y==0)
    phi=sorted(x for x in d if x); xi=sorted(x for x in e if x)
    # Exact GPY polynomial identity in t=zeta^(1/2), without division.
    bp={0:1}; bx={0:m}; sigma1=Counter(); sigma2=Counter()
    for x in phi:
        ri={2*x:1,-2*x:1}
        for power,value in laurent_mul(dict(sigma1),ri).items(): sigma2[power]+=value
        sigma1.update(ri); bp=laurent_mul(bp,{x:1,-x:-1})
    for x in xi: bx=laurent_mul(bx,{x:1,-x:-1})
    rhs=Counter(sigma2)
    for power,value in sigma1.items(): rhs[power]+=(2*k-1)*value
    rhs[0]+=2*k*k-3*k+len(phi)
    require(bx==laurent_mul(bp,dict(rhs)), 'exact inflation identity')
    require(sum(phi)%2==0 and sum(xi)%2==0,'theta Heisenberg characters')
    require(2*k+2*len(phi)==48,'eta multiplier exponent')
    require(Fraction(2*k,24)+len(phi)*Fraction(1,12)==2,'q order')
    return {'parameters':[a,b],'weight':k,'m':m,'phi_entries':phi,
            'xi_entries':xi,'index':sum(x*x for x in phi)//2,
            'inflated_index':sum(x*x for x in xi)//2,'q_order':2}

def rational_irreducible_quartic(c):
    divisors=[s*d for d in range(1,abs(c[0])+1) if c[0]%d==0 for s in (-1,1)]
    require(all(sum(v*r**i for i,v in enumerate(c)) for r in divisors),'linear factor')
    for a in divisors:
        b=c[0]//a
        if a!=b:
            u=Fraction(c[1]-a*c[3],b-a); v=c[3]-u
            require(u.denominator!=1 or u*v+a+b!=c[2],'quadratic factor')
        elif c[1]==a*c[3]:
            delta=c[3]**2-4*(c[2]-a-b)
            require(delta<0 or math.isqrt(delta)**2!=delta or
                    (c[3]+math.isqrt(delta))%2!=0,'equal-constant quadratic factor')

def verify(cert):
    require(type(cert) is dict,'certificate object')
    same(set_as_list(cert),sorted(['problem_id','status','approaches_used','scope','curves',
         'borcherds_inputs','residual','simplicity','finite_match_control']),'top-level keys')
    same(cert['problem_id'],30003140,'problem id')
    same(cert['status'],'UNSOLVED','unproved global status')
    same(cert['approaches_used'],5,'approach count')
    same(cert['scope'],'bounded arithmetic partials; no Hecke matching or global modularity proof','scope')
    require(set(cert['curves'])=={'713','893'},'curve keys')
    rows={}
    for N in (713,893):
        same(add(pmul(H[N],H[N]),[4*x for x in G[N]]),F[N],'integral model')
        hprime=derivative(H[N]); gprime=derivative(G[N])
        require(gcd(H[N],add(pmul(gprime,gprime),pmul(pmul(hprime,hprime),G[N])),2)==[1],
                'geometric smoothness at 2')
        disc=(-1)**15*resultant(F[N],derivative(F[N]))
        same(disc,4096*N,'discriminant')
        good=[]
        for p in PRIMES:
            n1,n2=count_curve(N,p,1),count_curve(N,p,2)
            a=p+1-n1; b=Fraction(a*a-p*p-1+n2,2)
            require(b.denominator==1,'integral b'); b=int(b)
            good.append(dict(p=p,count_p=n1,count_p2=n2,a=a,b=b,
                             euler_ascending=[1,-a,b,-p*a,p*p],ordinary=b%p!=0))
            rows[N,p]=good[-1]
        bad=[]
        for p in ([23,31] if N==713 else [19,47]):
            common=gcd(F[N],derivative(F[N]),p)
            require(len(common)==2,'single double root')
            r=(-common[0])%p
            # Divide twice by (x-r), via independent synthetic division.
            q=F[N]
            for unused in range(2):
                quotient=[0]*(len(q)-1); quotient[-1]=q[-1]%p
                for j in range(len(quotient)-2,-1,-1): quotient[j]=(q[j+1]+r*quotient[j+1])%p
                require((q[0]+r*quotient[0])%p==0,'synthetic-division remainder')
                q=quotient
            require(gcd(q,derivative(q),p)==[1],'squarefree normalization')
            value=evaluate(q,r,p); require(value!=0,'node nondegeneracy')
            epsilon=1 if any(y*y%p==value for y in range(p)) else -1
            ec=2+sum((y*y-evaluate(q,x,p))%p==0 for x in range(p) for y in range(p))
            ae=p+1-ec
            bad.append(dict(p=p,double_root=r,normalization_ascending=[x if x<=p//2 else x-p for x in q],
                            node_value=value,epsilon=epsilon,elliptic_count=ec,elliptic_trace=ae,
                            euler_ascending=pmul([1,-epsilon],[1,-ae,p])))
        same(cert['curves'][str(N)],dict(sextic_ascending=F[N],h_ascending=H[N],g_ascending=G[N],
             discriminant=disc,good_factors=good,bad_factors=bad,
             local_root_number_product=math.prod(-x['epsilon'] for x in bad)), 'curve arithmetic '+str(N))
    blocks=[theta(a,b) for a,b in ((1,4),(-5,3),(5,3))]
    same(cert['borcherds_inputs'],blocks,'theta inputs')
    same(blocks[0]['phi_entries'],blocks[1]['phi_entries'],'713 phi equality')
    same(blocks[0]['xi_entries'],blocks[1]['xi_entries'],'713 xi equality')
    u=[-1,0,1,1]; v=[-1,4,-3,1]
    same(pmul(u,v),F[713],'cubic factorization')
    require(all(sum(a*r**i for i,a in enumerate(f))!=0 for f in (u,v) for r in (-1,1)), 'irreducible cubics')
    same([-resultant(f,derivative(f)) for f in (u,v)],[-23,-31],'cubic discriminants')
    same(resultant(u,v),64,'cubic resultant')
    same(cert['residual']['713'],dict(factor_degrees=[3,3],cubic_discriminants=[-23,-31],resultant=64,
         group='S3 x S3',representation='reducible 2+2'),'713 residual statement')
    require(set(cert['residual'])=={'713','893'},'residual keys')
    res=cert['residual']['893']
    require(set(res)=={'group','representation','frobenius_factorizations'},'893 residual keys')
    same(res['group'],'S6','893 residual group')
    same(res['representation'],'absolutely irreducible','893 representation')
    require(len(res['frobenius_factorizations'])==3,'three factorization witnesses')
    for row,p,degrees in zip(res['frobenius_factorizations'],(3,7,349),([6],[1,5],[1,1,1,1,2])):
        require(set(row)=={'p','degrees','factors_ascending'},'factorization keys')
        same(row['p'],p,'witness prime'); same(row['degrees'],degrees,'factor degrees')
        factors=row['factors_ascending']; product=[1]
        require(sorted(len(f)-1 for f in factors)==degrees,'actual factor degrees')
        for f in factors:
            require(all(type(x) is int for x in f) and f[-1]==1,'factor coefficient types')
            require(irreducible(f,p),'Rabin irreducibility'); product=pmul(product,f)
        same([x%p for x in product],[x%p for x in F[893]],'factor product')
        require(gcd(F[893],derivative(F[893]),p)==[1],'unramified witness')
    q713=list(reversed(rows[713,11]['euler_ascending']))
    q893=list(reversed(rows[893,5]['euler_ascending']))
    require(irreducible(q713,3),'713 irreducible Frobenius')
    rational_irreducible_quartic(q893)
    same(cert['simplicity'],{'713':dict(prime=11,characteristic_ascending=q713,irreducible_modulus=3),
          '893':dict(prime=5,characteristic_ascending=q893,method='all possible integral factors excluded')},'simplicity')
    q=120121
    require(all(q%d for d in range(2,math.isqrt(q)+1)),'twist prime primality')
    require(q%(8*3*5*7*11*13)==1,'twist congruence')
    same(cert['finite_match_control'],dict(twist_prime=q,matching_primes=[2,3,5,7,11,13],
         new_conductor_multiplier=q**4,warning='changes conductor; not a counterexample at fixed level'),'twist claims')
    return dict(status='PASS_INDEPENDENT_BOUNDED_ARITHMETIC',good_factors=20,bad_factors=4,
                exact_theta_identities=3,borcherds_B=[sum(b['phi_entries'])//2 for b in blocks],
                eta_exponent=48,global_modularity='NOT_PROVED',optimization=sys.flags.optimize)

def set_as_list(d): return sorted(d)

def inventory(root):
    path=root/'MANIFEST.json'
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PIN,'frozen manifest pin')
    m=strict_json(path)
    require(set(m)=={'files','exceptions'},'manifest schema')
    same(m['exceptions'],['MANIFEST.json is externally pinned and excludes itself'],'manifest exception')
    entries=list(root.rglob('*'))
    require(all(not p.is_symlink() for p in entries),'no symlinks')
    require({p.relative_to(root).as_posix() for p in entries if p.is_file()}==set(m['files'])|{'MANIFEST.json'},'inventory')
    for name,record in m['files'].items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'safe path')
        raw=(root/name).read_bytes()
        same(record,dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),'file identity '+name)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('packet',type=Path)
    parser.add_argument('--certificate',type=Path,help='Use a separate claim file after verifying frozen packet')
    args=parser.parse_args()
    inventory(args.packet)
    report=verify(strict_json(args.certificate or args.packet/'certificate.json'))
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':
    try: main()
    except Exception as error:
        print('AUDIT_REJECT: '+str(error),file=sys.stderr)
        sys.exit(2)
