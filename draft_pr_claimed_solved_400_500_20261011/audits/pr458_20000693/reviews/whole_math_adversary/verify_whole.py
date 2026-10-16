#!/usr/bin/env python3
"""Explicit guards for local sharp/full identities. No L-function high moments."""
import argparse, json, math, sys
from fractions import Fraction as F

parser=argparse.ArgumentParser()
parser.add_argument('--mutant',default='')
args=parser.parse_args()
checks=0

def require(c,label):
    global checks
    checks+=1
    if not c: raise RuntimeError(label)

def ga(a=0,b=0):return F(a),F(b)
def add(z,w):return z[0]+w[0],z[1]+w[1]
def scale(z,a):return z[0]*a,z[1]*a
def mul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def power(z,n):
    v=ga(1)
    for _ in range(n):v=mul(v,z)
    return v
def norm(z):return z[0]*z[0]+z[1]*z[1]

def coeff(rows,N,K=None,delete=True,wrong_sign=False):
    # rows = (primitive local phase, weight, original-modulus deletion flag)
    c=[ga(1)]
    for n in range(1,N+1):
        s=ga()
        for j in range(1,n+1):
            h=ga()
            for z,a,d in rows:
                v=int(K is None or j<=K)
                if K is None: v=0 if d else 1
                elif delete and d: v+=1 if wrong_sign else -1
                h=add(h,scale(power(z,j),a*v))
            s=add(s,mul(h,c[n-j]))
        c.append(scale(s,F(1,n)))
    return c

def major(A,N):
    d=[F(1)]
    for n in range(1,N+1):d.append(d[-1]*(A+n-1)/n)
    return d

def partial_norm(c,p):return sum((norm(v)/p**n for n,v in enumerate(c)),F(0))

profiles=[
 [(ga(1),F(1),False)],
 [(ga(1),F(1),False),(ga(1),F(1),True)],
 [(ga(0,1),F(1,4),False),(ga(0,-1),F(7,4),False)],
 [(ga(-1),F(1,2),False),(ga(1),F(3,2),False),(ga(0,1),F(1,3),False)],
 [(ga(0,1),F(3,4),True),(ga(0,-1),F(1,4),False),(ga(),F(1,2),True)],
 [(ga(1),F(0),True)],
 []]
N=20
local_cases=0
for rows in profiles:
    A=sum((a for z,a,d in rows),F(0))
    full=coeff(rows,N)
    kept=[row for row in rows if row[1]]
    require(full==coeff(kept,N),'zero-weight omission')
    require(full[0]==ga(1),'constant coefficient')
    expected=ga()
    for z,a,d in rows:
        if not d:expected=add(expected,scale(z,a))
    require(full[1]==expected,'actual local first coefficient')
    for n,d in enumerate(major(A,N)):
        require(norm(full[n])<=d*d,'full coefficient majorant')
    for K in [1,2,4,8,20]:
        sharp=coeff(rows,N,K=K)
        require(sharp[1]==full[1],'sharp/full same first coefficient')
        for n in range(min(K,N)+1):
            require(sharp[n]==full[n],'coefficients through included prime powers')
        bound=major(A if not any(d for z,a,d in rows) else 2*A,N)
        for n,d in enumerate(bound):require(norm(sharp[n])<=d*d,'sharp coefficient majorant')
        for p in [2,3,5,7,11,97]:
            tail_bound=sum((d*d/F(2)**(n-2) for n,d in enumerate(bound) if n>=2),F(0))
            sf=partial_norm(full,p);ss=partial_norm(sharp,p)
            require(sf>=1 and ss>=1,'positive local norms')
            require(abs(sf-ss)*p*p<=2*tail_bound,'finite coefficient p^-2 bound')
            local_cases+=1

# In-range sharp counterexample: X=3 at prime2 includes only k=1.
require(2<=3 and 4>3,'X3 sharp prime-power range')
sharp=coeff(profiles[0],N,K=1)
require(all(v==ga(F(1,math.factorial(n))) for n,v in enumerate(sharp)),'exp(z) coefficients')
partial=partial_norm(sharp,2)
next_term=F(1,2**(N+1)*math.factorial(N+1)**2)
r=F(1,2*(N+2)**2)
upper=partial+next_term/(1-r)
require(upper<F(13,8)<2,'rigorous rational sharp mean enclosure')
claim=upper==2 if args.mutant=='sharp_full_equality' else upper<2
require(claim,'finite sharp factor differs from full Euler norm')

# Finite bad prime converges coefficientwise only with deletions retained.
full=coeff(profiles[1],N)
sharp=coeff(profiles[1],N,K=N,delete=args.mutant!='dropped_deletion',wrong_sign=args.mutant=='wrong_deletion_sign')
require(sharp==full,'finite bad-prime deletion bridge')

# Exact common-phase benchmark; separate phase products are unequal.
x=F(1,2);one=1/(1-x);two=(1+x)/(1-x)**3
require(two==12 and one==2,'one/two-factor exact local norms')
mean=one*one if args.mutant=='independent_prime_phases' else two
require(mean==12,'same-prime factors share phase')
ratio=F(1) if args.mutant=='ignored_finite_ratio' else one/two
require(ratio==F(1,6),'zeta principal-mod2 local ratio')

same_E=2 if args.mutant=='modulus_grouping' else F(1+1)**2
require(same_E==4,'same primitive classes aggregate')
conj_E=4 if args.mutant=='conjugate_grouping' else F(1)**2+F(1)**2
require(conj_E==2,'nonreal primitive conjugates distinct')

# Exact CUE Toeplitz determinant from Laurent polynomial for integer weight.
def determinant(mat):
    if not mat:return F(1)
    b=[list(row) for row in mat];v=F(1)
    for col in range(len(b)):
        pivot=next((r for r in range(col,len(b)) if b[r][col]),None)
        if pivot is None:return F(0)
        if pivot!=col:b[col],b[pivot]=b[pivot],b[col];v=-v
        q=b[col][col];v*=q
        for j in range(col,len(b)):b[col][j]/=q
        for i in range(col+1,len(b)):
            t=b[i][col]
            for j in range(col,len(b)):b[i][j]-=t*b[col][j]
    return v

def finite_C(N,m):
    v=F(1)
    for j in range(1,N+1):v*=F(math.factorial(j-1)*math.factorial(j+2*m-1),math.factorial(j+m-1)**2)
    return v

def barnes_int(n):
    v=1
    for j in range(1,n-1):v*=math.factorial(j)
    return v

matrix_cases=0
for m in range(5):
    for size in range(9):
        def fourier(k):return F((-1)**abs(k)*math.comb(2*m,m+k)) if abs(k)<=m else F(0)
        d=determinant([[fourier(i-j) for j in range(size)] for i in range(size)])
        product=finite_C(size,m)
        require(d==product,'integer finite CUE determinant identity')
        G=F(barnes_int(1+m)**2,barnes_int(1+2*m))
        quotient=G*F(barnes_int(size+1)*barnes_int(size+1+2*m),barnes_int(size+1+m)**2)
        require(product==quotient,'finite CUE Barnes recurrence')
        matrix_cases+=1
Gtwo=F(barnes_int(3)**2,barnes_int(5))
require((F(1,6) if args.mutant=='wrong_barnes' else Gtwo)==F(1,12),'weight-two Barnes constant')
coefficient=Gtwo/F(6)
require((coefficient*math.factorial(4) if args.mutant=='extra_gamma' else coefficient)==F(1,72),'no extra Gamma(E+1)')

print(json.dumps({'status':'PASS','guards':checks,'local_row_K_prime_cases':local_cases,'coefficient_degree':N,'matrix_integer_cases':matrix_cases,'X3_p2_sharp_mean_interval':{'lower':str(partial),'upper':str(upper)},'full_p2_mean':'2','rigorous_interval_is_exact_rational':True,'general_L_moment_theorem_proved':False,'joint_T_X_interchange_certified':False,'priority_certified':False},indent=2)+'\n')
