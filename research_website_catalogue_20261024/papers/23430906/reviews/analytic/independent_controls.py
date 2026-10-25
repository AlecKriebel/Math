"""Independent exact arithmetic controls, created before reading submitted code.
Uses Python standard library only. No external assets, state mutations, or installs.
Finite algebra is evidence for the accompanying universal analytic derivation.
"""
from fractions import Fraction as Q
import json, math, hashlib

def derivative(p): return [Q(i)*p[i] for i in range(1,len(p))] or [Q(0)]
def mul(p,q):
    r=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q): r[i+j]+=a*b
    return r

def val(p,x):
    s=Q(0)
    for a in reversed(p): s=s*x+a
    return s

def integ(p,a=Q(0),b=Q(1)):
    return sum(c*(b**(i+1)-a**(i+1))/Q(i+1) for i,c in enumerate(p))

def check(b,msg):
    if not b: raise RuntimeError(msg)

phi=[Q(0)]*4+[Q(1),Q(-4),Q(6),Q(-4),Q(1)]
f=derivative(phi); g=phi
f3=derivative(derivative(derivative(f)))
g3=derivative(derivative(derivative(g)))
a=integ(mul(f,f))
Lf=2*val(phi,Q(1,2)); Lg=integ(phi)
check(a==Q(4,45045),'wrong area pairing')
check(Lf==Q(1,128),'wrong Lf')
check(Lg==Q(1,630),'wrong Lg')
for r in (f,g):
    for d in range(3):
        check(val(r,Q(0))==val(r,Q(1))==0,'bad zero-extension trace')
        r=derivative(r)
check(f3==list(map(Q,[24,-480,2160,-3360,1680])),'bad f triple derivative')
check(g3==list(map(Q,[0,24,-240,720,-840,336])),'bad g triple derivative')
# Derive g''' factorization, rather than integrating a submitted absolute value routine.
# g'''=24*x*(1-x)*(1-2*x)*(1-7*x+7*x*x).
factor=[Q(24)]
for p in ([0,1],[1,-1],[1,-2],[1,-7,7]): factor=mul(factor,list(map(Q,p)))
check(factor==g3,'g triple derivative factorization failed')
# Let z be the smaller root of 1-7z+7z²=0. Evaluate a polynomial
# at z in Q[z]/(7z²-7z+1), and integrate exact sign intervals.
def addpair(a,b): return (a[0]+b[0],a[1]+b[1])
def mulpair(a,b):
    # z²=z-1/7
    return (a[0]*b[0]-a[1]*b[1]/7,a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def atz(p):
    s=(Q(0),Q(0))
    for c in reversed(p): s=addpair(mulpair(s,(Q(0),Q(1))),(c,Q(0)))
    return s
primitive=[Q(0)]+[c/Q(i+1) for i,c in enumerate(g3)]
Gz=atz(primitive); Ghalf=val(primitive,Q(1,2)); G0=val(primitive,Q(0))
# g''' positive on (0,z), negative on (z,1/2); antisymmetric thereafter.
Ng_pair=(4*Gz[0]-2*G0-2*Ghalf,4*Gz[1])
check(Ng_pair==(Q(113,196),Q(0)),'Ng claimed exact value failed')
# Negative controls: coarse increment coercivity cannot replace this proof.
coercivity=[{'H':H,'n':n,'all_ones_variance_over_n':n**(2*H-1)}
            for H in (.26,.4) for n in (1,16,256,65536)]
# Brownian control from its RKHS derivative norm, independent of Fourier code:
# D_(1/2)=2*pi; norm(u_r)^2=integral (r')², and n disjoint supports
# give a diagonal Gram. This must not accidentally imply a bound stronger than optimum.
Ef=integ(mul(derivative(f),derivative(f)))
Eg=integ(mul(derivative(g),derivative(g)))
cb=float(a)/math.sqrt(float(Ef*Eg))
check(0<cb<.5,'Brownian local witness contradicts exact optimum')
# Exact correction variance at H=1/2: rho(0)=1; rho(r)=0 for all r>=1.
# At H=1, rho(r)=1 and Q_m variance=T^4/4 (no convergence); at H=1/4
# diagonal contribution to E Q_m² is T/4 independent of m.
for r in range(1,20):
    check(Q((r+1)+(r-1)-2*r,2)==0,'Brownian rho')
    check(Q((r+1)**2+(r-1)**2-2*r*r,2)==1,'linear rho')
# Exact determinant test showing PSD trace bound allows negative off-diagonals
# and noncommuting A,C; both A,C <=2I here, trace(AC)=11/4 <= n*4=8.
A=[[Q(1),Q(-1,2)],[Q(-1,2),Q(1)]]
C=[[Q(1),Q(1,4)],[Q(1,4),Q(2)]]
# use M_C=9/4 (row-sum upper bound), M_A=3/2
trAC=sum(A[j][k]*C[k][j] for j in range(2) for k in range(2))
check(trAC==Q(11,4),'signed trace control')
check(trAC <= 2*Q(3,2)*Q(9,4),'trace control bound')
check(sum(A[0][k]*C[k][1] for k in range(2)) != sum(C[0][k]*A[k][1] for k in range(2)), 'noncommutation negative control')
# Absolute 3rd derivative bound for f, exact by coefficient triangle inequality,
# supplied as a conservative independent integrability control, not substituted
# into the published constant.
Nf_bound=sum(abs(c)/Q(i+1) for i,c in enumerate(f3))
result={'status':'PASS_EXACT_FINITE_CONTROLS','a':str(a),'Lf':str(Lf),'Lg':str(Lg),
 'Ng':str(Ng_pair[0]),'Ng_derivation_root':'7z^2-7z+1=0; z<1/2',
 'f3':[str(c) for c in f3],'g3':[str(c) for c in g3],
 'brownian_exact_gram_Ef':str(Ef),'brownian_exact_gram_Eg':str(Eg),
 'brownian_disjoint_witness_constant':cb,'brownian_optimal_constant':.5,
 'Nf_conservative_L1_upper_bound':str(Nf_bound),
 'signed_noncommuting_trace':str(trAC),'coercivity_negative_control':coercivity,
 'limits':{'H_one_quarter_Qm_diagonal':'T/4','H_one_Qm_variance':'T^4/4'},
 'scope':'Exact algebraic and finite controls only. Universal claim established by separate written analysis.'}
print(json.dumps(result,indent=2))
