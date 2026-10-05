#!/usr/bin/env python3
"""Independent exact reconstruction; does not import or execute author code.
Same 957 coverage controls, with extra Fourier, symbol, and integral identities.
"""
import json
from collections import Counter
import sympy as s

coverage=Counter(); extra=Counter()
def zero(name, value, supplemental=False):
    values=list(value) if isinstance(value,s.MatrixBase) else [value]
    if not all(s.cancel(s.expand(x))==0 for x in values):
        # Non-rational powers can arise only in the explicit mass scaling test.
        if not all(s.simplify(x)==0 for x in values):
            raise AssertionError((name,value))
    (extra if supplemental else coverage)[name]+=1

def yes(name, condition, supplemental=False):
    if not bool(condition): raise AssertionError(name)
    (extra if supplemental else coverage)[name]+=1

r,a,p,d,m,k,t=s.symbols('r a p d m k t',positive=True)
rho=a*a+r*r
# Derive the two Clifford coefficients using radial A(r)I+iB(r)X.
# D_0[A I+i B X] = (d B+r B')I-i(A'/r)X.
logg=-p*r/rho
scalar=d+r*logg+2*m*a-p*a*a/rho
xcoef=-a*logg/r-p*a/rho
zero('generic_clifford_residual',scalar-(d-p+2*m*a))
zero('generic_clifford_residual',xcoef)
zero('generic_clifford_residual',scalar.subs(a,(p-d)/(2*m)))
b=d+2*m*a
zero('threshold_branch',(d+r*(-b*r/rho)+2*m*a-b*a*a/rho))
# Differentiate the log of the norm functional from scratch.
logJ=p*s.log(d+2*m*a)+(d-p)*s.log(a)
slope=s.diff(logJ,a)
a0=(p-d)/(2*m)
zero('width_optimization',slope-d*(2*m*a-p+d)/(a*(d+2*m*a)))
zero('width_optimization',slope.subs(a,a0))
zero('width_optimization',s.diff(logJ,a,2).subs(a,a0)-4*m*m*d/(p*(p-d)))
zero('mass_scaling',s.expand_power_base((m*a)**(d-p),force=True)*m**(p-d)-a**(d-p))
q=2*p/(p-1)
zero('pohozaev_coefficients',d*(q-2)/(2*q)-d/(2*p))
zero('pohozaev_coefficients',2*m*a0/p-(p-d)/p)

# Use t=r^2: no direct differentiation of the author's h_n expression.
wt=(a*a+t)/(p*a)
A=k-p*t/(a*a+t) # r h'/h

def radial_value(n, aa=a, pp=p):
    ww=(aa*aa+t)/(pp*aa)
    kk=abs(n) if n.is_number else k
    aa_log=kk-pp*t/(aa*aa+t)
    return -2*s.diff(ww,t)*aa_log-2*ww*s.diff(aa_log,t)-ww*aa_log**2/t+n*n*ww/t+2*n*s.diff(ww,t)+(pp-2)/aa-1/ww

w=rho/(p*a)
for sign in (1,-1):
    n=sign*k
    constant=2*k/a if sign>0 else 2*k*(p-2)/(p*a)
    zero('generic_angular_eigenidentity',radial_value(n)-constant)
    # Gauge f=h g. Compare coefficients of g^2 and g g'; h^2 divides out.
    g,gp=s.symbols('g gp',real=True)
    ell=k/r-p*r/rho
    B=w*(r*ell-n)
    left=r*w*((ell-n/r)*g+gp)**2+r*((p-2)/a-1/w-constant)*g*g-r*w*gp*gp
    boundary=(s.diff(B,r)+2*ell*B)*g*g+2*B*g*gp
    zero('generic_groundstate_factorization',left-boundary)
zero('angular_gap',(2*(p-2)/(p*a)).subs(a,(p-2)/(2*m))-4*m/p)
zero('weighted_modulus_obstruction',w/r-s.diff(w,r)-(a*a-r*r)/(p*a*r))

for dd in range(2,11):
    for epsilon in map(s.Rational,('1/5','1/2','1','3')):
        pp=dd+epsilon
        for mm in map(s.Rational,('1/2','1','3/2')):
            aa=epsilon/(2*mm)
            yes('admissibility_rational_cases',aa>0 and pp>1+s.Rational(dd,2))
            # Beta integral gives upper-spin mass / nonlinear mass = a/p.
            zero('virial_rational_cases',2*mm*aa/pp-(pp-dd)/pp)
            for factor in map(s.Rational,('1/3','1','3')):
                value=slope.subs({a:factor*aa,d:dd,p:pp,m:mm})
                yes('width_derivative_signs',s.sign(value)==s.sign(factor-1))
for nn in range(-12,13):
    for pp in map(s.Rational,('5/2','3','17/4','8')):
        mm=s.Rational(3,2);aa=(pp-2)/(2*mm)
        n=s.Integer(nn)
        cc=2*nn/aa if nn>=0 else -2*nn*(pp-2)/(pp*aa)
        zero('finite_angular_modes',radial_value(n,aa,pp)-cc)
        if nn: yes('finite_angular_gap',cc>=4*mm/pp)

# Alternative recursive Clifford representation: prepend sigma_x at each lift.
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def clifford(slots):
    if slots==1:return [X,Y,Z]
    old=clifford(slots-1); Id=s.eye(old[0].rows)
    return [s.kronecker_product(X,G) for G in old]+[s.kronecker_product(Y,Id),s.kronecker_product(Z,Id)]
for dd in range(2,7):
    gens=clifford((dd+1)//2)[:dd+1]
    Id=s.eye(gens[0].rows);alpha=gens[:dd];beta=gens[dd]
    for G in gens:
        zero('clifford_hermiticity',G-G.adjoint())
        for H in gens:zero('clifford_anticommutation',G*H+H*G-(2*Id if G==H else s.zeros(Id.rows)))
    # Pick a nonzero column of the positive spectral projection, not assumed e_0.
    projection=(Id+beta)/2
    xi=next(projection[:,j] for j in range(Id.rows) if projection[:,j]!=s.zeros(Id.rows,1))
    xi=xi/s.sqrt((xi.adjoint()*xi)[0])
    zero('positive_mass_spinor',beta*xi-xi)
    xs=s.symbols('x:'+str(dd),real=True)
    XX=sum((alpha[j]*xs[j] for j in range(dd)),s.zeros(Id.rows))
    for pp in (dd+1,dd+3):
        mm=s.Rational(3,2);aa=s.Rational(pp-dd,3)
        rr=aa*aa+sum(z*z for z in xs)
        # Differentiate the matrix polynomial and power separately before evaluation.
        polynomial=(aa*Id+s.I*XX)*xi
        differentiated=sum((-s.I*alpha[j]*(s.diff(polynomial,xs[j])-pp*xs[j]*polynomial/rr) for j in range(dd)),s.zeros(Id.rows,1))
        full=differentiated+(mm*(beta+Id)-pp*aa/rr*Id)*polynomial
        density=(polynomial.adjoint()*polynomial)[0]-rr
        for shift in (0,1):
            values={xs[j]:s.Rational(j+shift+1,j+2) for j in range(dd)}
            zero('matrix_threshold_residual',full.subs(values))
            zero('matrix_spinor_density',density.subs(values))
    momentum=s.symbols('z:'+str(dd),real=True)
    symbol=sum((alpha[j]*momentum[j] for j in range(dd)),m*beta)
    zero('free_mass_symbol',symbol*symbol-(sum(z*z for z in momentum)+m*m)*Id,True)

# Supplement: norm and mass splitting from independent beta recursion.
# ∫r^(d-1)(a²+r²)^(-p) dr=(a^(d-2p)/2)B(d/2,p-d/2).
zero('beta_scaling_exponent',p+(d-2*p)-(d-p),True)
zero('beta_upper_mass_ratio',a*a/(p*a)-a/p,True)
zero('beta_lower_mass_ratio',s.Rational(1,2)*d/(p-d/s.Integer(2)-1)-d/(2*p-d-2),True)
# Formal adjoint in polar variables with r dr dtheta:
# P sends upper n to lower n+1; P* sends lower j to upper j-1.
n=s.symbols('n',integer=True);f=s.Function('f')(r)
Pmode=s.diff(f,r)-n*f/r
LfromP=-s.diff(w*Pmode,r)-(n+1)*w*Pmode/r+((p-2)/a-1/w)*f
Lexpanded=-s.diff(r*w*s.diff(f,r),r)/r+(n*n*w/r**2+n*s.diff(w,r)/r+(p-2)/a-1/w)*f
zero('polar_adjoint_and_index_shift',LfromP-Lexpanded,True)
# Exact sharpness witness via beta integrals after setting a=1; n=-1.
# ∫r h^2=1/[2(p-1)(p-2)] and c=2(p-2)/p.
zero('sharpness_beta_ratio',(1/(p*(p-1)))/(1/(2*(p-1)*(p-2)))-2*(p-2)/p,True)
# Tail L2 and weighted-gradient exponents for k=0 and k=1.
for kk in (0,1):
    yes('sharp_witness_integrability',s.simplify((2*kk+1-2*p).subs(p,2+s.symbols('e',positive=True)))<-1,True)

# Exact radial integrals check the L2 and nonlinear mass relation independently.
for dd in range(2,11):
    for pp in (dd+1,dd+3):
        mm=s.Rational(5,4);aa=s.Rational(2*(pp-dd),5)
        j0=aa**(dd-2*pp)*s.gamma(s.Rational(dd,2))*s.gamma(pp-s.Rational(dd,2))/(2*s.gamma(pp))
        I=(pp*aa)**pp*j0
        U=(pp*aa)**(pp-1)*aa**2*j0
        zero('integrated_virial',2*mm*U-(1-s.Rational(dd,pp))*I,True)
# The Schur sharp witness gives v~r^(2-p), so full-spinor L2 needs p>3.
for pp in map(s.Rational,('5/2','3','7/2','4')):
    yes('sharp_witness_full_spinor_threshold',(5-2*pp<-1)==(pp>3),True)
fsharp=r*rho**(-p/2)
vsharp=(s.diff(fsharp,r)+fsharp/r)*rho/(p*a)
zero('sharp_lower_component',s.powsimp(vsharp+(rho**(-p/2))*((p-2)*r*r-2*a*a)/(p*a)),True)

assert sum(coverage.values())==957,(sum(coverage.values()),coverage)
result={'status':'PASS','original_problem_solved':False,'reconstructed_author_controls':sum(coverage.values()),'coverage_groups':dict(sorted(coverage.items())),'supplemental_controls':sum(extra.values()),'supplemental_groups':dict(sorted(extra.items())),'independence':'This independent checker never imports or executes the author checker; recursive Clifford representation and squared-radius radial operator. Same parameter grid for coverage comparison.','scope':'Exact algebra only. Infinite-mode, closure, domain, and source arguments are reviewed separately in AUDIT.md.'}
print(json.dumps(result,indent=2,sort_keys=True))
