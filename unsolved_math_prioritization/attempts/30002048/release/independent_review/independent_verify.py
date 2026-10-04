#!/usr/bin/env python3
"""Independent, standard-library-only certificate. Ascending coefficient lists.
No author programs are imported or executed. Author JSON may optionally be compared.
CRT: polynomial Euclid idempotents (not matrix inversion).
Quartics: symbolic 4x4 permutation determinant (not interpolation).
Integer roots: coefficient-derived Cauchy bound (not rational-root divisors).
Irreducibility: all monic finite-field divisors up to half-degree (not Frobenius).
Fixed resultants: Sylvester matrix and rational elimination (not Bareiss).
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, permutations
from math import gcd
import argparse, hashlib, json
from pathlib import Path


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p or [0]

def add(p,q):
    a=[0]*max(len(p),len(q))
    for i,v in enumerate(p):a[i]+=v
    for i,v in enumerate(q):a[i]+=v
    return trim(a)

def scale(p,c):return trim([c*v for v in p])
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    a=[0]*(len(p)+len(q)-1)
    for i,v in enumerate(p):
        for j,w in enumerate(q):a[i+j]+=v*w
    return trim(a)

def divrem(p,q):
    p=list(map(F,trim(p)));q=list(map(F,trim(q)))
    assert q!=[0]
    a=[F(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k=len(p)-len(q);c=p[-1]/q[-1];a[k]+=c
        p=sub(p,[0]*k+scale(q,c))
    return trim(a),trim(p)

def exactdiv(p,q):
    a,r=divrem(p,q);assert r==[0];return a

def mod(p,q):return divrem(p,q)[1]
def at(p,t):
    a=0
    for c in reversed(p):a=a*t+c
    return a

def integer(p):
    assert all(F(c).denominator==1 for c in p)
    return [int(c) for c in p]

def inverse(p,m):
    a,b=p,m;s,t=[1],[0]
    while b!=[0]:
        q,r=divrem(a,b);a,b=b,r;s,t=t,sub(s,mul(q,t))
    assert len(a)==1 and a[0]!=0
    v=mod(scale(s,1/F(a[0])),m)
    assert mod(mul(p,v),m)==[1]
    return v

@lru_cache(None)
def phi(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:a=exactdiv(a,list(phi(d)))
    return tuple(integer(a))

def det(a):
    a=[list(map(F,r)) for r in a];n=len(a);ans=F(1)
    for c in range(n):
        k=next((i for i in range(c,n) if a[i][c]),None)
        if k is None:return F(0)
        if k!=c:a[c],a[k]=a[k],a[c];ans=-ans
        v=a[c][c];ans*=v
        for i in range(c+1,n):
            ratio=a[i][c]/v
            for j in range(c+1,n):a[i][j]-=ratio*a[c][j]
            a[i][c]=0
    return ans

def resultant(f,g):
    f=trim(f);g=trim(g);m=len(f)-1;n=len(g)-1
    if m==0:return f[0]**n
    if n==0:return g[0]**m
    rows=[]
    for k in range(n):rows.append([0]*k+f[::-1]+[0]*(n-1-k))
    for k in range(m):rows.append([0]*k+g[::-1]+[0]*(m-1-k))
    v=det(rows);assert v.denominator==1;return int(v)

def A(n,f):return resultant(list(phi(n)),f)
def Bs(n,f):return resultant([-1]+[0]*(n-1)+[1],f)

def permutation_sign(p):
    return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))

def quartic(P,r):
    # P(x)*(x+a)+r(x), in Q[a][x]. Multiplication by f in Q[x]/Phi_5.
    g=add(mul(P,[0,1]),r);h=list(phi(5));matrix=[]
    columns=[]
    for j in range(4):
        u=mod([0]*j+g,h);v=mod([0]*j+P,h)
        u=u+[0]*(4-len(u));v=v+[0]*(4-len(v))
        columns.append([trim([u[i],v[i]]) for i in range(4)])
    matrix=[[columns[j][i] for j in range(4)] for i in range(4)]
    out=[0]
    for pi in permutations(range(4)):
        term=[permutation_sign(pi)]
        for i in range(4):term=mul(term,matrix[i][pi[i]])
        out=add(out,term)
    out=integer(sub(out,[1]));assert len(out)==5 and out[-1]==5
    return out

def all_integer_roots(q):
    # Every complex root obeys |z| <= 1+max_i<d |q_i/q_d|.
    B=1+max(abs(F(c,q[-1])) for c in q[:-1])
    L=B.numerator//B.denominator
    return [t for t in range(-L,L+1) if at(q,t)==0],L

def rem_modp(f,g,p):
    f=trim([v%p for v in f]);g=trim([v%p for v in g])
    while f!=[0] and len(f)>=len(g):
        c=f[-1]*pow(g[-1],-1,p)%p;k=len(f)-len(g)
        for i,v in enumerate(g):f[k+i]=(f[k+i]-c*v)%p
        f=trim(f)
    return f

def trial_irreducible(f,p):
    assert f[-1]%p!=0;checks=[];cert=hashlib.sha256()
    for d in range(1,(len(f)-1)//2+1):
        count=0
        for coefficients in product(range(p),repeat=d):
            q=list(coefficients)+[1];r=rem_modp(f,q,p);assert r!=[0]
            cert.update(json.dumps([q,r],separators=(',',':')).encode()+b'\n');count+=1
        checks.append({'degree':d,'monic_divisors_tested':count})
    return {'prime':p,'divisor_counts':checks,'transcript_sha256':cert.hexdigest(),'irreducible':True}

def root_formula(m):
    n=m;Q=1;t=2
    while t*t<=n:
        pp=1
        while n%t==0:pp*=t;n//=t
        Q=max(Q,pp);t+=1
    Q=max(Q,n)
    return m//Q-1

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--author-json');parser.add_argument('--root-limit',type=int,default=80);args=parser.parse_args()
    S=[1,2,3,4,6];mods=[list(phi(n)) for n in S];P=[1]
    for g in mods:P=mul(P,g)
    assert P==[-1,0,-1,0,0,0,1,0,1]
    bases=[]
    for m in mods:
        quotient=exactdiv(P,m);bases.append(mod(mul(quotient,inverse(quotient,m)),P))
    options=[[[1],[-1]],[[1],[-1]],[[1],[-1],[0,1],[0,-1],[1,1],[-1,-1]],[[1],[-1],[0,1],[0,-1]],[[1],[-1],[0,1],[0,-1],[-1,1],[1,-1]]]
    for n,values in zip(S,options):
        assert all(abs(A(n,r))==1 for r in values)
        if n>2:
            # Completing the square proves both integer coefficients are in {-1,0,1}.
            generated={tuple(trim([b,a])) for a,b in product(range(-1,2),repeat=2) if A(n,trim([b,a]))==1}
            assert generated==set(map(tuple,values))
    residues=set();denominators={};tuple_count=0
    for values in product(*options):
        r=[0]
        for b,v in zip(bases,values):r=add(r,mul(b,v))
        r=mod(r,P);tuple_count+=1
        for m,v in zip(mods,values):assert mod(r,m)==v
        den=1
        for c in r:den=den*F(c).denominator//gcd(den,F(c).denominator)
        denominators[str(den)]=denominators.get(str(den),0)+1
        if den==1:residues.add(tuple(integer(r)))
    R=sorted(residues);assert tuple_count==576 and len(R)==24
    powers=[]
    for j in range(12):powers.append(integer(mod([0]*j+[1],P)))
    assert len(set(map(tuple,powers)))==12
    assert set(R)==set(tuple(scale(v,s)) for v in powers for s in [-1,1])
    d7=[list(r) for r in R if len(r)==8 and r[-1]==1]
    assert len(d7)==3 and all(f[0]==0 for f in d7)
    d8=[]
    for r in R:
        f=add(P,r)
        if A(5,f)==1:d8.append({'f':f,'norms_Res_Phi_f':[A(n,f) for n in range(1,9)]})
    assert len(d8)==7
    d8last=[c for c in d8 if c['norms_Res_Phi_f'][6]==1]
    assert len(d8last)==3
    assert [v['norms_Res_Phi_f'][7] for v in d8last].count(9)==2
    assert sum(v['f'][0]==0 for v in d8last)==1
    quartics=[];d9=[]
    for r in R:
        q=quartic(P,list(r));roots,bound=all_integer_roots(q)
        quartics.append({'residue':list(r),'quartic':q,'integer_roots':roots,'cauchy_integer_bound':bound})
        for t in [-bound,-3,-1,0,1,2,7,bound]:assert at(q,t)==A(5,add(mul(P,[t,1]),r))-1
        for t in roots:
            f=add(mul(P,[t,1]),r);assert len(f)==10 and f[-1]==1 and A(5,f)==1
            d9.append({'residue':list(r),'a':t,'f':f,'C7':A(7,f)})
    assert len(d9)==15
    d9last=[c for c in d9 if c['C7']==1]
    assert len(d9last)==3 and all(c['f'][0]==0 for c in d9last)
    assert set(tuple(c['f']) for c in d9last)==set(tuple([0]+c['f']) for c in d8last)
    witness_input=[([-1,-1,-1,0,1,1,1,1],2,5),([-1,-1,-1,0,0,1,1,1,1],2,7),([-1,-1,-1,-1,0,1,1,1,1,1],5,6)]
    witnesses=[];signed_count=0
    for f,p,E in witness_input:
        norms=[A(n,f) for n in range(1,E+2)]
        assert all(abs(v)==1 for v in norms[:-1]) and abs(norms[-1])!=1
        certificate=trial_irreducible(f,p)
        # Check both resultant orders and cyclic factorization, including n=1,2 signs.
        cyclic=[];norm_order=[]
        for n in range(1,E+2):
            lhs=Bs(n,f);rhs=1
            for j in range(1,n+1):
                if n%j==0:rhs*=A(j,f)
            assert lhs==rhs
            swapped=resultant(f,list(phi(n)))
            assert swapped==(-1)**((len(f)-1)*(len(phi(n))-1))*norms[n-1]
            assert resultant(f,[-1]+[0]*(n-1)+[1])==(-1)**(n*(len(f)-1))*lhs
            cyclic.append(lhs);norm_order.append(swapped);signed_count+=1
        witnesses.append({'f':f,'prime':p,'E0':E,'norms_Res_Phi_f':norms,'norms_Res_f_Phi':norm_order,'cyclic_Res_xn_minus1_f':cyclic,'irreducibility':certificate})
    assert A(1,[-1,1])==0  # alpha=1, E0=0.
    assert all(abs(Bs(n,[0,1]))==1 for n in range(1,13))  # excluded alpha=0.
    assert A(6,[-1,1])==1 and Bs(6,[-1,1])==0  # ROUTES.md counterexample.
    roots_of_unity=[]
    for m in range(2,args.root_limit+1):
        f=list(phi(m));E=root_formula(m);vals=[Bs(n,f) for n in range(1,E+2)]
        assert all(abs(c)==1 for c in vals[:-1]) and abs(vals[-1])!=1 and E<len(f)-1
        roots_of_unity.append({'order':m,'degree':len(f)-1,'E0':E,'first_nonunit_absnorm':abs(vals[-1])})
    substitution=[];f=[-1,-1,0,1,1,1]
    for k in range(1,9):
        g=[0]*(5*k+1)
        for i,c in enumerate(f):g[i*k]=c
        n=1
        while True:
            direct=Bs(n,g);h=gcd(n,k);expected=Bs(n//h,f)**h
            assert direct==expected
            if abs(direct)!=1:break
            n+=1
        substitution.append({'k':k,'degree':5*k,'prefix':n-1,'first_failed_n':n})
    data={'P':P,'crt_tuple_count':tuple_count,'crt_denominator_histogram':denominators,'crt_idempotents':[[str(c) for c in b] for b in bases],'integral_residue_count':len(R),'integral_residues':[list(r) for r in R],'d7_all_candidates_for_E_ge_6':d7,'d8_C5_survivors':d8,'d8_C7_survivors':d8last,'d9_quartic_certificates':quartics,'d9_C5_survivors':d9,'d9_C7_survivors':d9last,'witnesses':witnesses,'signed_resultant_controls':signed_count,'root_of_unity_controls':roots_of_unity,'substitution_controls':substitution,'proved_scoped_values':{'e(7)':5,'e(8)':7,'e(9)':6},'status':'unsolved','route2_counterexample':{'f':[-1,1],'j':6,'A_j':1,'B_j':0,'common_factor_over_every_prime':[-1,1]}}
    if args.author_json:
        author=json.load(open(args.author_json));comparisons=[]
        for key in ['P','crt_tuple_count','integral_residue_count','proved_scoped_values','status','substitution_controls']:
            assert data[key]==author[key],key;comparisons.append(key)
        assert sorted(map(tuple,d7))==sorted(map(tuple,author['d7_all_candidates_for_E_ge_6']));comparisons.append('d7_all_candidates_for_E_ge_6')
        for key,id_key,fields in [('d8_C5_survivors','f',['f','norms_Res_Phi_f']),('d9_C5_survivors','f',['f','residue','a','C7']),('d9_quartic_certificates','residue',['residue','quartic','integer_roots']),('witnesses','f',['f','prime','E0','norms_Res_Phi_f'])]:
            aa={tuple(c[id_key]):c for c in author[key]};bb={tuple(c[id_key]):c for c in data[key]}
            assert aa.keys()==bb.keys(),key
            for k in aa:
                for field in fields:assert aa[k][field]==bb[k][field],(key,k,field)
            comparisons.append(key)
        data['author_data_comparison']={'all_mathematical_fields_match':True,'matched_fields':comparisons,'author_results_sha256':hashlib.sha256(Path(args.author_json).read_bytes()).hexdigest()}
    print(json.dumps(data,indent=2,sort_keys=True))

if __name__=='__main__':main()
