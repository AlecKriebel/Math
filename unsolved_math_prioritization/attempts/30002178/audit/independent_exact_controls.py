#!/usr/bin/env python3
"""Independent exact audit; standard library only. Never imports author code.
Usage: python independent_exact_controls.py AUTHOR_FREEZE.zip --output result.json
All output comparisons are against the frozen RESULTS.json read from the ZIP.
"""
import argparse, hashlib, json, math, zipfile
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product

CHECKS = 0
SCALE = 10**60

def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

def trimmed(a):
    a = list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def divide(a,b):
    a=trimmed(a); b=trimmed(b)
    q=[F(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a != [0]:
        k=len(a)-len(b); c=F(a[-1],b[-1]); q[k]=c
        for j,d in enumerate(b): a[k+j]-=c*d
        a=trimmed(a)
    return trimmed(q),a

@lru_cache(None)
def cyclo(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            a,r=divide(a,cyclo(d))
            require(r==[0], 'exact recursive cyclotomic division')
    require(all(F(c).denominator==1 for c in a),'cyclotomic coefficients integral')
    return tuple(int(c) for c in a)

@lru_cache(None)
def basis(n,a):
    v=[0]*(a%n)+[1]
    _,r=divide(v,cyclo(n))
    return tuple(int(c) for c in r)+tuple([0]*(len(cyclo(n))-1-len(r)))

def remainder(n,ex):
    bs=[basis(n,a) for a in ex]
    return tuple(map(sum,zip(*bs)))

def mu(n):
    result=1; p=2
    while p*p<=n:
        if n%p==0:
            n//=p; result=-result
            if n%p==0: return 0
            while n%p==0:n//=p
        p+=1
    return -result if n>1 else result

@lru_cache(None)
def ramanujan(n,k):
    g=math.gcd(n,k)
    return sum(d*mu(n//d) for d in range(1,g+1) if g%d==0)

def trace_square(n,ex):
    return sum(ramanujan(n,a-b) for a in ex for b in ex)

def atan_interval(q,terms):
    s=F(0)
    for j in range(terms):s+=F((-1)**j,(2*j+1)*q**(2*j+1))
    next_term=F((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(s,s+next_term),max(s,s+next_term)

# Independent identity: pi=8 atan(1/3)+4 atan(1/7).
# tan(2 atan(1/3))=3/4; adding atan(1/7) gives tangent 1.
a,b=atan_interval(3,100);c,d=atan_interval(7,80)
PI_LO=8*a+4*c; PI_HI=8*b+4*d
require(3<PI_LO<PI_HI<F(22,7),'independent pi enclosure')
# Round the certified interval outward to avoid huge Taylor denominators.
PS=10**80
_lo=PI_LO*PS;_hi=PI_HI*PS
PI_LO=F(_lo.numerator//_lo.denominator,PS)
PI_HI=F(-(-_hi.numerator//_hi.denominator),PS)

def floor(q):return q.numerator//q.denominator

def outward(center,error):
    return floor((center-error)*SCALE),-floor(-(center+error)*SCALE)

@lru_cache(None)
def root_rectangle(n,k):
    k%=n
    if k==0:return (SCALE,SCALE,0,0)
    if 2*k==n:return (-SCALE,-SCALE,0,0)
    if k>n//2:
        rl,rh,il,ih=root_rectangle(n,n-k)
        return rl,rh,-ih,-il
    t=F(k,n)*(PI_LO+PI_HI)
    uncertainty=F(k,n)*(PI_HI-PI_LO)
    cos=sum(((-1)**j*t**(2*j)/math.factorial(2*j) for j in range(41)),F(0))
    sin=sum(((-1)**j*t**(2*j+1)/math.factorial(2*j+1) for j in range(41)),F(0))
    rl,rh=outward(cos,F(4**82,math.factorial(82))+uncertainty)
    il,ih=outward(sin,F(4**83,math.factorial(83))+uncertainty)
    return rl,rh,il,ih

def squared_interval(a,b):
    return (0 if a<=0<=b else min(a*a,b*b)),max(a*a,b*b)

def squared_modulus(n,ex):
    coords=[root_rectangle(n,k) for k in ex]
    rl,rh,il,ih=map(sum,zip(*coords))
    a,b=squared_interval(rl,rh);c,d=squared_interval(il,ih)
    return F(a+c,SCALE*SCALE),F(b+d,SCALE*SCALE)

def matrix_for(n,ex):
    dim=len(cyclo(n))-1
    cols=[remainder(n,tuple(a+j for a in ex)) for j in range(dim)]
    return [list(map(F,row)) for row in zip(*cols)]

def determinant(mat):
    a=[row[:] for row in mat];d=F(1);n=len(a)
    for j in range(n):
        pivot=next((k for k in range(j,n) if a[k][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];d=-d
        v=a[j][j];d*=v
        for k in range(j+1,n):
            ratio=a[k][j]/v
            for l in range(j,n):a[k][l]-=ratio*a[j][l]
    return d

def inverse_trace(mat):
    n=len(mat);a=[row[:]+[F(i==j) for j in range(n)] for i,row in enumerate(mat)]
    for j in range(n):
        pivot=next(k for k in range(j,n) if a[k][j])
        a[j],a[pivot]=a[pivot],a[j]
        v=a[j][j];a[j]=[c/v for c in a[j]]
        for k in range(n):
            if k!=j:
                v=a[k][j];a[k]=[u-v*w for u,w in zip(a[k],a[j])]
    return sum(a[i][n+i] for i in range(n))

def direct_counts(p,ex,indices):
    indices=tuple(indices);counts=[0]*p
    for choices in product(ex,repeat=len(indices)):
        counts[sum(a*j for a,j in zip(choices,indices))%p]+=1
    return counts

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):c[i+j]+=u*v
    return trimmed(c)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('archive');ap.add_argument('--output',required=True);args=ap.parse_args()
    raw=open(args.archive,'rb').read()
    require(len(raw)==29040,'frozen archive bytes')
    require(hashlib.sha256(raw).hexdigest()=='24f88fd09d1f753306be377bcb96e17a0dd85d2ccb674975873a6046ddcbe02d','frozen archive hash')
    with zipfile.ZipFile(args.archive) as z:
        author=json.loads(z.read('RESULTS.json'))
        require(hashlib.sha256(z.read('MANIFEST.json')).hexdigest()=='12236b07d02cdc19409631ce6b56ae41d6509876a3c7fa200e2aafda1df329b6','frozen manifest hash')
    lookup={(r['m'],r['N']):r for r in author['minimum_enclosures']}
    cases=zeroes=0;rows=[]
    for m in range(1,6):
        for n in range(2,25 if m<5 else 19):
            count=zcount=0;minlo=minhi=None
            bound={1:F(1),2:F(2,n),3:F(2,3*n),4:F(2,n*n)}.get(m)
            for tail in combinations_with_replacement(range(n),m-1):
                ex=(0,)+tail; count+=1;cases+=1
                tr=trace_square(n,ex);r=remainder(n,ex)
                require(tr>=0,'nonnegative conjugate-square trace')
                require((tr==0)==(not any(r)),'Ramanujan versus independent cyclotomic zero classification')
                lo,hi=squared_modulus(n,ex)
                if tr==0:
                    zeroes+=1;zcount+=1
                    require(lo==0,'exact zero in rectangle enclosure')
                else:
                    require(lo>0,'nonzero independently separated')
                    if bound is not None:require(lo>=bound*bound,'independent small-m analytic bound')
                    minlo=lo if minlo is None else min(minlo,lo)
                    minhi=hi if minhi is None else min(minhi,hi)
            rec=lookup[(m,n)];alo,ahi=map(F,rec['minimum_squared_modulus_interval'])
            require(rec['normalized_multisets']==count,'row multiset count')
            require(rec['exact_zeros']==zcount,'row zero count')
            require(alo<=minlo<=minhi<=ahi,'independent minimum enclosure lies in author enclosure')
            wlo,whi=squared_modulus(n,rec['upper_bound_witness'])
            require(whi<=ahi and wlo>=minlo,'author upper witness independently certified')
            rows.append({'m':m,'N':n,'multisets':count,'zeroes':zcount,'minimum_squared_enclosure':[str(minlo),str(minhi)]})
    require(cases==author['normalized_multisets']==46803,'full finite case total')
    require(zeroes==author['exact_zero_multisets'],'total exact zero count')
    count_cases=[]
    for p in [3,5,7,11]:
        for ex in [(0,), (0,0), (0,1), (0,0,1), (0,1,2), (0,0,1,3)]:
            m=len(ex)
            if m>=p:continue
            mat=matrix_for(p,ex);D=determinant(mat)
            require(D>0 and D.denominator==1,'positive integral multiplication-matrix norm')
            R=direct_counts(p,ex,range(1,p));Q=direct_counts(p,ex,range(2,p-1))
            require(p*R[0]==m**(p-1)+(p-1)*D,'direct-count R identity')
            require(sum(R)==m**(p-1) and sum(Q)==m**(p-3),'direct-count totals retain multiplicity')
            b_ex=tuple(a-b for a in ex for b in ex)
            B=matrix_for(p,b_ex);T=inverse_trace(B)
            require(p*Q[0]==m**(p-3)+D*T,'direct-count Q and matrix inverse trace identity')
            H=sum(ex.count(a)**2 for a in set(ex))
            require(sum(B[i][i] for i in range(p-1))==p*H-m*m,'matrix trace verifies Fourier energy')
            # Rational lower interval confirms both published norm-derived bounds.
            lo,_=squared_modulus(p,ex)
            if all(B[i][j]==(B[0][0] if i==j else 0) for i in range(p-1) for j in range(p-1)):
                lo=B[0][0]  # exact rational squared modulus, including equality cases
            require(lo>=F(1,m**(p-3)),'paired norm squared lower bound')
            if p>=5:
                k=(p-3)//2
                require(lo>=F(p-3,p*H-m*m)**k,'prime energy squared lower bound')
            else:require(lo>=1,'p=3 squared modulus bound')
            count_cases.append({'p':p,'exponents':ex,'norm':int(D),'inverse_trace':str(T),'r0':R[0],'q0':Q[0]})
    require(len(count_cases)==21,'author counting case coverage')
    polynomials=[]
    for r in range(1,9):polynomials.append([(-1)**i*math.comb(r,i) for i in range(r+1)])
    polynomials += [[1,0,0,0,0,1],[1,0,0,-2,0,0,0,1],[1,-1,1,-1],[2,0,0,0,0,-3,0,0,1]]
    taylor=[]
    for cs in polynomials:
        A=len(cs)-1;L=sum(map(abs,cs));s=sum(c!=0 for c in cs)
        shifted=[sum(cs[j]*math.comb(j,k) for j in range(k,A+1)) for k in range(A+1)]
        q=next(k for k,c in enumerate(shifted) if c)
        Q=cs[:]
        for _ in range(q):Q,rem=divide(Q,[-1,1]);require(rem==[0],'independent exact Taylor division')
        require(q<=s-1 and abs(shifted[q])>=1,'sparsity and integral leading Taylor coefficient')
        require(sum(map(abs,Q))<=L*A**q,'Taylor quotient height')
        require(sum(abs(i*c) for i,c in enumerate(Q))<=L*A**(q+1),'Taylor derivative l1 bound')
        # Choose an integer N with N>=4*pi*L*A^(q+1), using pi<22/7.
        n=(88*L*A**(q+1)+6)//7
        require(F(n)>=4*PI_HI*L*A**(q+1),'certified Taylor threshold')
        # Signed root sum: retain integer coefficients, no numerical zero test.
        ex=[]
        for j,c in enumerate(Q):ex.extend([2*j+(n if c<0 else 0)]*abs(int(c)))
        qlo,qhi=squared_modulus(2*n,ex)
        chordlo,chordhi=squared_modulus(2*n,(0,n+2))
        require(qlo>=F(1,4),'quotient local modulus at least one half')
        require(chordlo>=F(4,n)**2,'local chord lower bound')
        require(qlo*chordlo**q>=F(1,4)*F(4,n)**(2*q),'quantitative local Taylor bound from exact factorization')
        taylor.append({'coefficients':cs,'q':q,'support':s,'coefficient_mass':L,'threshold_conductor':n})
    negatives=[]
    def negative(label,condition):require(condition,label);negatives.append({'claim_rejected':label,'witness_pass':True})
    negative('include zero sums in a positive lower bound',trace_square(3,(0,1,2))==0)
    negative('replace multisets by sets',trace_square(4,(0,1,2,3))==0 and trace_square(4,(0,0,1,3))>0)
    negative('absorb a minus sign in an odd conductor',(-1)**3!=1)
    negative('identify support size with positive summand count',len(polynomials[3])==5 and sum(map(abs,polynomials[3]))==16)
    negative('replace a common conductor by maximum separate order',math.lcm(4,6)==12>6)
    negative('drop primeness from m<p nonvanishing',len((0,3))<6 and trace_square(6,(0,3))==0)
    negative('use number of terms as cyclotomic field degree',len(cyclo(17))-1==16>2)
    negative('omit multiplicity from Fourier energy',trace_square(5,(0,0))==16 and 5*2-4==6)
    negative('infer total nonvanishing from nonzero subsums',trace_square(4,(0,1))>0 and trace_square(4,(2,3))>0 and trace_square(4,(0,1,2,3))==0)
    negative('rotation uniformly shortens exponent spread',min(max((a-r)%101 for a in (0,33,67)) for r in range(101))==67)
    negative('identify sparse support with coefficient mass in Taylor constants',sum(map(abs,polynomials[7]))==256 and len(polynomials[7])==9)
    negative('apply local Taylor threshold to arbitrary spread',101<4*PI_LO*3*67)
    negative('infer an individual lower bound from product and mean alone',F(1,2**20)*2**20==1 and (F(1,2**20)+20*2)/21<2)
    negative('an exceptional-set bound excludes every exceptional point',1<=math.isqrt(101))
    negative('one chosen prime is every prescribed prime',5!=7)
    negative('strict lower sign follows from equal non-strict bound without exponent slack',not (F(1,10)>F(1,10)))
    negative('E(8)=2 is compatible with the chord-product construction',F(2*PI_HI,1000)**3<F(1,1000**2))
    result={'status':'PASS','scope':'finite exact corroboration; not an infinite-target proof','standard_library_only':True,'imports_author_code':False,
      'archive_sha256':hashlib.sha256(raw).hexdigest(),'checks':CHECKS,'multisets':cases,'exact_zero_multisets':zeroes,
      'method':'Ramanujan trace zero tests; independent recursive cyclotomic division; root-coordinate rational rectangles; direct product enumeration; multiplication matrices',
      'counting_cases':count_cases,'taylor_cases':taylor,'negative_controls':negatives,'rows':rows,'pi_interval':[str(PI_LO),str(PI_HI)]}
    with open(args.output,'w') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','pi_interval','counting_cases','taylor_cases','negative_controls')},indent=2))

if __name__=='__main__':main()
