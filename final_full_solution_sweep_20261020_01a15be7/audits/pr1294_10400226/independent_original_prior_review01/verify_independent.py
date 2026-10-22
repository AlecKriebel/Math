"""Fresh exact finite diagnostics; no claimant/source-author program imported.

The universal prime-existence argument is written in REPORT.md and uses
Dirichlet. This bounded computation checks arithmetic, matrices and falsifiers.
Every guard survives -O/-OO. No floating point is used.
"""
from fractions import Fraction as Q
from itertools import permutations
from math import gcd, isqrt
from collections import Counter
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def factor(n):
    out={};d=2
    while d*d<=n:
        while n%d==0:
            out[d]=out.get(d,0)+1;n//=d
        d+=1
    if n>1:
        out[n]=out.get(n,0)+1
    return out


def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))


def jacobi(a,b):
    need(b>0 and b%2==1,'positive odd Jacobi denominator')
    a%=b;ans=1
    while a:
        while a%2==0:
            a//=2
            if b%8 in (3,5):ans=-ans
        a,b=b,a
        if a%4==b%4==3:ans=-ans
        a%=b
    return ans if b==1 else 0


def legendre(a,p):
    x=pow(a%p,(p-1)//2,p)
    return -1 if x==p-1 else x


def crt(pairs):
    x=0;mod=1
    for a,m in pairs:
        need(m>0 and gcd(mod,m)==1,'CRT requires coprime positive moduli')
        if m==1:continue
        x+=mod*(((a-x)*pow(mod,-1,m))%m);mod*=m;x%=mod
    return x,mod


def four(b,c,y):
    need(all(type(x) is int for x in (b,c,y)) and y%2==0,'integral even y')
    return [[1,1,0,0],[0,b,y//2,0],[0,y//2,c,1],[0,0,0,1]]


def two(h):
    need(type(h) is int and h>0 and h%4==1,'W needs positive h=1 mod4')
    return [[-1,1],[0,(h-1)//4]]


def direct(V,W):
    n=len(V);m=len(W)
    return [r+[0]*m for r in V]+[[0]*n+r for r in W]


def symmetric(V):
    return [[V[i][j]+V[j][i] for j in range(len(V))] for i in range(len(V))]


def det(A):
    # Independent Leibniz expansion, adequate for dimensions at most six.
    n=len(A);total=0
    for pp in permutations(range(n)):
        v=1
        for i,j in enumerate(pp):v*=A[i][j]
        if sum(pp[i]>pp[j] for i in range(n) for j in range(i+1,n))%2:v=-v
        total+=v
    return total


def inertia(A):
    # Exact rational congruence elimination, including zero diagonal pivots.
    M=[[Q(x) for x in row] for row in A];positive=negative=zero=0
    while M:
        n=len(M);need(all(M[i][j]==M[j][i] for i in range(n) for j in range(n)),
                       'inertia needs symmetric matrix')
        k=next((i for i in range(n) if M[i][i]),None)
        if k is not None:
            order=[k]+[i for i in range(n) if i!=k];M=[[M[i][j] for j in order] for i in order]
            d=M[0][0]
            positive+=d>0;negative+=d<0
            M=[[M[i][j]-M[i][0]*M[0][j]/d for j in range(1,n)] for i in range(1,n)]
            continue
        pair=next(((i,j) for i in range(n) for j in range(i+1,n) if M[i][j]),None)
        if pair is None:
            zero+=n;break
        i,j=pair;order=[i,j]+[k for k in range(n) if k not in pair]
        M=[[M[i][j] for j in order] for i in order];a=M[0][1]
        positive+=1;negative+=1
        M=[[M[i][j]-(M[i][0]*M[1][j]+M[i][1]*M[0][j])/a
            for j in range(2,n)] for i in range(2,n)]
    return [positive,negative,zero]


def verify(V,n,signature=4,canonical=True):
    d=len(V)
    need(d in (4,6) and all(len(r)==d for r in V),'matrix size')
    need(all(type(x) is int for row in V for x in row),'Seifert entries integral')
    A=[[V[i][j]-V[j][i] for j in range(d)] for i in range(d)]
    need(det(A)==1,'unimodular alternating part')
    if canonical:
        need(all(A[i][j]==(1 if i%2==0 and j==i+1 else -1 if j%2==0 and i==j+1 else 0)
                 for i in range(d) for j in range(d)),'exact J blocks')
    S=symmetric(V);signed=det(S);ii=inertia(S)
    need(abs(signed)==n,'absolute determinant')
    need(ii[0]-ii[1]==signature and ii[2]==0,'exact signature')
    leading=[det([row[:k] for row in S[:k]]) for k in range(1,d+1)]
    if d==4 and signature==4:need(all(x>0 for x in leading),'positive leading minors')
    return {'signed_determinant':signed,'inertia':ii,'leading_minors':leading}


def nonsquare(n):
    f=factor(n);s=1;m=1
    for p,e in f.items():s*=p**(e//2);m*=p**(e%2)
    need(m>1 and m%4==1 and s*s*m==n,'squarefree reduction')
    r=min(factor(m));u=next(a for a in range(1,r) if legendre(a,r)==-1)
    t,mod=crt([(3,4),(u,r),(1,m//r)])
    need(mod==4*m and gcd(t,mod)==1 and jacobi(t,m)==-1,'reduced negative-character CRT')
    ell=t;skipped=[]
    while True:
        if prime(ell):
            if s%ell==0:skipped.append(ell)
            else:break
        ell+=mod
    need(ell%4==3 and n%ell!=0,'admissible prime and exclusion')
    need(legendre(n,ell)==jacobi(m,ell)==jacobi(ell,m)==jacobi(t,m)==-1,
         'reciprocity with positive sign at m=1 mod4')
    need(legendre(-n,ell)==1,'negative n square residue')
    x=pow((-n)%ell,(ell+1)//4,ell)
    need(x*x%ell==(-n)%ell and x!=0,'verified prime square root')
    y0=x*pow(2,-1,ell)%ell;y=y0 if y0%2==0 else y0+ell
    need(y%2==0 and y>=0 and (n+4*y*y)%ell==0,'parity-adjusted y')
    h=(n+4*y*y)//ell
    need(h>=3 and h%4==3,'positive quotient in required class')
    b=(ell+1)//4;c=(h+1)//4
    V=four(b,c,y)
    return V,{'branch':'nonsquare','n':n,'s':s,'m':m,'r':r,'u':u,'t':t,'modulus':mod,
              'ell':ell,'skipped_prime_divisors_of_s':skipped,'b':b,'c':c,'y':y}


def construct(n):
    need(type(n) is int and n>1 and n%4==1,'original n>1 congruent1 mod4')
    if isqrt(n)**2!=n:return nonsquare(n)
    ps=factor(n)
    ell=next((p for p in ps if p%4==3),None)
    if ell is not None:
        h=n//ell;need(h>=3 and h%4==3,'divisor branch quotient')
        return four((ell+1)//4,(h+1)//4,0),{'branch':'square_factor3','n':n,'ell':ell,'h':h}
    p=min(ps);need(p%4==1 and p>=5,'remaining square prime')
    V,rr=nonsquare(p);h=n//p
    return direct(V,two(h)),{'branch':'remaining_square','n':n,'p':p,'h':h,'prime_block':rr}


def main():
    ns=sorted(set(range(5,2002,4))|{245,6125,33049,33049**2,(13*17)**2,3**8,5**8})
    result=[];counts=Counter();alternate=0;skips=[]
    for n in ns:
        V,r=construct(n);r['checked']=verify(V,n);counts[r['branch']]+=1
        if r['branch']=='nonsquare' and r['skipped_prime_divisors_of_s']:skips.append(n)
        # Every available divisor branch is checked independently of primary case.
        for ell in factor(n):
            if ell%4==3:
                h=n//ell;verify(four((ell+1)//4,(h+1)//4,0),n);alternate+=1
        if n in (5,9,25,245,33049,33049**2):r['matrix']=V
        result.append(r)
    need(245 in skips,'explicitly exercise excluded first progression prime')
    # Directly verify the printed worked example, without matching search choices.
    example=verify(four(5,437,6),33049)
    need(example['leading_minors']==[2,19,16534,33049],'printed example principal minors')
    V,_=construct(25);need(verify(V,25)['signed_determinant']==-25,'square branch signed determinant')
    mirror=[[-V[j][i] for j in range(6)] for i in range(6)]
    verify(mirror,25,signature=-4)
    # Opposite intersection-form sign convention via unimodular basis reversal.
    signs=[1,-1]*3;changed=[[signs[i]*V[i][j]*signs[j] for j in range(6)] for i in range(6)]
    verify(changed,25,canonical=False)
    need(inertia([[0,1],[1,0]])==[1,1,0] and inertia([[0,0],[0,0]])==[0,0,2],
         'zero-pivot and degenerate inertia controls')
    need(jacobi(2,15)==1 and all(x*x%15!=2 for x in range(15)),
         'Jacobi1 over composite denominator is not a square-root certificate')
    bad=[]
    def reject(name,fn):
        try:fn()
        except ValueError:bad.append(name)
        else:raise ValueError('corruption accepted: '+name)
    for n in (1,0,-3,3,13.0,True):reject('bad_input_'+str(n),lambda n=n:construct(n))
    reject('odd_y',lambda:four(1,2,1))
    reject('W_wrong_class',lambda:two(3))
    reject('CRT_non_coprime',lambda:crt([(1,4),(3,6)]))
    reject('composite_Jacobi_square_root',lambda:need(any(x*x%15==2 for x in range(15)),'false composite root'))
    reject('skip_exclusion_omitted',lambda:need(245%7!=0,'first prime7 divides s7 for n245'))
    reject('positive_signed_square_det',lambda:need(det(symmetric(V))==25,'signed determinant is negative'))
    reject('universal_genus2_by_this_construction',lambda:need(len(V)==4,'remaining square uses6dimensions'))
    wrong=[r[:] for r in V];wrong[0][1]+=1
    reject('changed_skew_entry',lambda:verify(wrong,25))
    reject('wrong_signature_sign',lambda:verify(mirror,25))
    reject('false_positive_definiteness',lambda:need(inertia(symmetric(four(1,1,2)))==[4,0,0],'negative determinant example'))
    indefinite=symmetric(four(0,-1,0))
    need(det(indefinite)==5 and inertia(indefinite)==[2,2,0],
         'positive determinant alone does not suffice without b>=1')
    reject('b_guard_omitted',lambda:need(inertia(indefinite)==[4,0,0],'b>=1 is essential'))
    # Audit Jacobi's arithmetic routine against independently factored Legendre products.
    symbol_checks=0
    for denominator in range(1,202,2):
        for a in range(denominator):
            expected=1
            for p,e in factor(denominator).items():expected*=legendre(a,p)**e
            need(jacobi(a,denominator)==expected,'Jacobi product check');symbol_checks+=1
    print(json.dumps({'status':'PASS','bounded_inputs':len(ns),'case_counts':dict(counts),
        'results':result,'alternate_divisor_checks':alternate,'skip_cases':skips,
        'printed_example':example,'Jacobi_product_checks':symbol_checks,
        'negative_controls_rejected':bad,'guards_survive_optimization':True,
        'author_code_executed':False,'floating_point_used':False,
        'finite_search_not_universal_proof':True},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
