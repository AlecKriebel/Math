#!/usr/bin/env python3
"""Fresh finite falsification controls for 23157237; no claim of PDE proof.

Requires SymPy 1.14.0. Uses exact rational/algebraic arithmetic, apart from
standard symbolic limits. Does not import the author's controls or outputs.
"""
import hashlib
import itertools
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import sympy as s

assert s.__version__ == '1.14.0'
counts = Counter()
details = {}

def check(test, family):
    if not bool(test):
        raise AssertionError(family)
    counts[family] += 1

def eq(a, b, family):
    if isinstance(a, s.MatrixBase) or isinstance(b, s.MatrixBase):
        a, b = s.Matrix(a), s.Matrix(b)
        check(a.shape == b.shape, family)
        for z in a-b:
            check(s.simplify(z) == 0, family)
    else:
        check(s.simplify(a-b) == 0, family)

R = s.Rational

# Singular finite features with a repeated positive eigenvalue, a negative
# eigenvalue, a zero eigenvalue, and an empirical eigenvalue greater than one.
u = s.Matrix([1,2,3,4,5])
Q = s.eye(5) - 2*u*u.T/(u.dot(u))
V0 = s.zeros(5,6)
V0[0,0] = V0[0,1] = 1
for k in range(1,5):
    V0[k,k+1] = 1
V = Q*V0
G = V.T*V
Ghalf = s.diag(s.ones(2)/s.sqrt(2),s.eye(4))
kap = [R(1,4),R(1,4),-R(1,8),0,2]
C = s.diag(kap[0]/2,kap[0]/2,*kap[1:])
T = V*C*V.T
H = Ghalf*C*Ghalf
eq(Q.T*Q,s.eye(5),'singular_feature_geometry')
eq(Ghalf*Ghalf,G,'singular_feature_geometry')
check(G.rank()==5,'singular_feature_geometry')
eq(T,Q*s.diag(*kap)*Q.T,'singular_feature_geometry')
t = s.symbols('t')
nodes = [-R(1,8),0,R(1,4),2]
gv = [0,0,R(1,16),4]
# h/log(2) is rational at these positive powers of two.
hv = [0,0,-R(1,8),4]
pg = s.interpolate(list(zip(nodes,gv)),t)
ph = s.interpolate(list(zip(nodes,hv)),t)
def matpoly(poly,M):
    out=s.zeros(M.rows)
    for (power,),coeff in s.Poly(poly,t).terms():
        out += coeff*M**power
    return s.simplify(out)
gT,hT,gH,hH=[matpoly(p,M) for p,M in [(pg,T),(ph,T),(pg,H),(ph,H)]]
eq(gT,Q*s.diag(*[k*k if k>0 else 0 for k in kap])*Q.T,'spectral_functions')
eq(hT,Q*s.diag(-R(1,8),-R(1,8),0,0,4)*Q.T,'spectral_functions')
D=s.Matrix(5,6,lambda i,j: R(((i+2)*(j+3))%11-5,i+j+2))
v=s.Matrix([R(1,2),-2,R(2,3),4,-R(3,5),1])
B=D*C*V.T
e=v.T*C*V.T
A=B*gT*B.T
r=B*hT*e.T
eq(A,D*C*Ghalf*gH*Ghalf*C*D.T,'singular_gram_functional_identity')
eq(r,D*C*Ghalf*hH*Ghalf*C*v,'singular_gram_functional_identity')
A_modes=s.zeros(5)
r_modes=s.zeros(5,1)
for k in [0,1,4]:
    phi=Q[:,k]
    jet=B*phi/kap[k]
    val=(e*phi)[0]/kap[k]
    log2kap=-2 if k<2 else 1
    A_modes+=kap[k]**4*jet*jet.T
    r_modes+=kap[k]**4*log2kap*val*jet
eq(A,A_modes,'fourth_power_normal_equations')
eq(r,r_modes,'fourth_power_normal_equations')
rot=s.eye(5)
rot[0,0]=rot[1,1]=R(3,5)
rot[0,1]=-R(4,5);rot[1,0]=R(4,5)
A_rot=s.zeros(5);r_rot=s.zeros(5,1)
for k in [0,1,4]:
    phi=(Q*rot)[:,k]
    jet=B*phi/kap[k]; val=(e*phi)[0]/kap[k]
    A_rot+=kap[k]**4*jet*jet.T
    r_rot+=kap[k]**4*(-2 if k<2 else 1)*val*jet
eq(A,A_rot,'repeated_eigenspace_rotation')
eq(r,r_rot,'repeated_eigenspace_rotation')
Cp=s.zeros(6)
for k in range(5):
    Cp[k,k+1]=Cp[k+1,k]=R(1,10)
Tp=V*Cp*V.T;Hp=Ghalf*Cp*Ghalf
for k in range(8):
    eq(V.T*Tp**k*V,Ghalf*Hp**k*Ghalf,'actual_path_polynomial_identity')
details['singular_gram']={'feature_rank':5,'feature_count':6,'spectrum':[str(k) for k in kap],
                         'repeated_space_rotation':'3/5,4/5','path_polynomial_degrees':'0..7'}

# Local differential identities: nonconstant positive definite tensor,
# positive varying density, and arbitrary polynomial test functions.
for d in range(2,6):
    x=s.symbols('x0:'+str(d))
    w=s.Matrix([x[i]+i+1 for i in range(d)])
    S=s.eye(d)+w*w.T
    mu=3+sum(z*z for z in x)
    f=sum((i+1)*x[i]**3 for i in range(d))+s.prod(z+1 for z in x)
    divS=s.Matrix([sum(s.diff(S[i,j],x[i]) for i in range(d)) for j in range(d)])
    pairs=list(itertools.combinations(range(d),2))
    def jet(f):
        return s.Matrix([s.diff(f,z,2) for z in x]+[2*s.diff(f,x[i],x[j]) for i,j in pairs]+[s.diff(f,z) for z in x])
    theta=s.Matrix([S[i,i] for i in range(d)]+[S[i,j] for i,j in pairs]+list(divS))
    divflux=sum(s.diff(sum(S[i,j]*s.diff(f,x[j]) for j in range(d)),x[i]) for i in range(d))
    eq(jet(f).dot(theta),divflux,'tensor_jet_and_divergence')
    Sigma=2*S/mu; beta=divS/mu
    ito=sum(Sigma[i,j]*s.diff(f,x[i],x[j])/2 for i in range(d) for j in range(d))+sum(beta[i]*s.diff(f,x[i]) for i in range(d))
    eq(ito,divflux/mu,'tensor_ito_factor_two')
    a=[R(i+1,i+2) for i in range(d)]
    z=[x[i]-a[i] for i in range(d)]
    basis=[y*y/2 for y in z]+[z[i]*z[j]/2 for i,j in pairs]+z
    J=s.Matrix.hstack(*[jet(b).subs(dict(zip(x,a))) for b in basis])
    eq(J,s.eye(d*(d+1)//2+d),'full_local_jet_excitation')
    check(S.subs(dict(zip(x,a))).is_positive_definite,'tensor_positive_definiteness')
S=s.Matrix([[2,1],[1,3]]); n=s.Matrix([1,0]);z=s.Matrix([1,-2])
eq((n.T*S*z)[0],0,'conormal_normal_distinction')
check(n.dot(z)!=0,'conormal_normal_distinction')
z=s.Matrix([0,1]);eq(n.dot(z),0,'conormal_normal_distinction')
check((n.T*S*z)[0]!=0,'conormal_normal_distinction')
alpha=[28,-112,210,-224,140,-48,7]
for k in range(7):
    eq(sum(alpha[a-1]*(-a)**k for a in range(1,8)),1,'extension_moments')
check(sum(alpha[a-1]*(-a)**7 for a in range(1,8))!=1,'extension_order_boundary')
check(any(a<0 for a in alpha),'extension_signed_boundary')
for i in range(7):
    for j in range(7):
        eq(sum(alpha[a-1]*alpha[b-1]*(-a)**i*(-b)**j for a in range(1,8) for b in range(1,8)),1,'tensor_product_extension_moments')

# Four-state reversible chains with nonuniform invariant measure. The covariance
# expression is independently compared to direct sums over state paths.
pi=s.Matrix([[R(1,10),R(2,10),R(3,10),R(4,10)]])
Pi=s.ones(4,1)*pi
observables=[s.Matrix(4,4,lambda i,j:(i+1)+(j+1)),
             s.Matrix(4,4,lambda i,j:(i+1)*(j+2)-3*i),
             s.Matrix(4,4,lambda i,j:(-1)**(i+j)*(i-j)),
             s.ones(4)*7]
for rho in [0,R(1,3),R(9,10)]:
    P=rho*s.eye(4)+(1-rho)*Pi
    eq(pi*P,pi,'four_state_stationarity')
    eq(s.diag(*list(pi))*P,P.T*s.diag(*list(pi)),'four_state_reversibility')
    for F in observables:
        mean=sum(pi[i]*P[i,j]*F[i,j] for i in range(4) for j in range(4))
        Z=F-s.ones(4)*mean
        var=sum(pi[i]*P[i,j]*Z[i,j]**2 for i in range(4) for j in range(4))
        r=s.Matrix([sum(pi[i]*P[i,j]*Z[i,j] for i in range(4))/pi[j] for j in range(4)])
        st=s.Matrix([sum(P[i,j]*Z[i,j] for j in range(4)) for i in range(4)])
        eq((pi*r)[0],0,'pair_centering')
        eq((pi*st)[0],0,'pair_centering')
        covs={}
        for a in range(1,6):
            M=P**(a-1)
            c=sum(pi[i]*P[i,j]*M[j,k]*P[k,l]*Z[i,j]*Z[k,l]
                  for i,j,k,l in itertools.product(range(4),repeat=4))
            eq(c,(r.T*s.diag(*list(pi))*M*st)[0],'overlapping_pair_covariance')
            check(abs(c)<=rho**(a-1)*var,'overlapping_pair_decay_bound')
            covs[a]=c
        for N in [1,2,3]:
            # All N+1 states, using the probability of each entire path.
            path_var=0
            for path in itertools.product(range(4),repeat=N+1):
                prob=pi[path[0]]
                for k in range(N):
                    prob*=P[path[k],path[k+1]]
                avg=sum(Z[path[k],path[k+1]] for k in range(N))/N
                path_var+=prob*avg**2
            formula=(N*var+2*sum((N-a)*covs[a] for a in range(1,N)))/N**2
            eq(path_var,formula,'enumerated_pair_average_variance')
            bound=(1+2/(1-rho))*max(abs(v) for v in F)**2/N
            check(path_var<=bound,'pair_average_variance_bound')
        if rho==0 and F==observables[0]:
            check(covs[1]>0,'iid_overlap_negative_control')
            check(covs[1]>rho*var,'iid_overlap_negative_control')
            details['iid_adjacent_pair_covariance']=str(covs[1])

# The raw logarithm is not continuous near the zero spectral accumulation
# point. Weighted functional calculus is continuous there. Rotation drift
# aliasing is an intentionally outside-model negative control.
z=s.symbols('z',positive=True)
eq(s.limit(z**2*s.log(z),z,0,dir='+'),0,'weighted_log_zero_limit')
for k in range(1,25):
    k1=s.exp(-k*k);k2=s.exp(-2*k*k)
    eq(s.log(k1)-s.log(k2),k*k,'raw_log_instability')
    check(0<k1-k2<s.exp(-k*k),'raw_log_instability')
for ell in range(-12,13):
    eq(s.exp(2*s.pi*s.I*ell),1,'nonreversible_rotation_alias')
details['outside_model_control']='Angular drift b versus b+2*pi/Delta on a circle has identical fixed-lag Fourier factors. This is nonreversible and outside the known Euclidean-domain theorem.'
details['limits']='Finite controls verify identities and designed boundary failures only. They do not prove infinite-dimensional regularity, almost-sure convergence, or numerical implementation.'
payload={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
         'python':sys.version,'sympy':s.__version__,'assertions':sum(counts.values()),
         'families':len(counts),'counts':dict(counts),'details':details,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_control_results.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
