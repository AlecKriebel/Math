#!/usr/bin/env python3
"""Exact finite algebra controls. These do not certify the analytic theorems."""
import json
import sympy as S

counts = {}

def check(group, expression):
    if isinstance(expression, S.MatrixBase):
        ok = all(S.simplify(x) == 0 for x in expression)
    else:
        ok = S.simplify(expression) == 0
    if not ok:
        raise AssertionError((group, expression))
    counts[group] = counts.get(group, 0) + 1

r, mu, p, d, m, k = S.symbols('r mu p d m k', positive=True)
s = mu**2 + r**2
w = s/(p*mu)
V = 1/w

# The two scalar coefficients of the all-dimensional Clifford residual.
check('generic_clifford_residual', d-p*r**2/s+2*m*mu-V*mu-(d-p+2*m*mu))
check('generic_clifford_residual', p*mu/s-V)
check('generic_clifford_residual', (d-p+2*m*mu).subs(mu,(p-d)/(2*m)))

# Arbitrary threshold width, with exponent b=d+2m*mu.
b = d+2*m*mu
check('threshold_branch', d-b+2*m*mu)
log_derivative = 2*m*p/(d+2*m*mu)+(d-p)/mu
check('width_optimization', log_derivative-d*(2*m*mu-(p-d))/(mu*(d+2*m*mu)))
check('width_optimization', log_derivative.subs(mu,(p-d)/(2*m)))
check('width_optimization', S.diff(log_derivative,mu).subs(mu,(p-d)/(2*m))-4*m**2*d/(p*(p-d)))
check('mass_scaling', (m*mu)**(d-p)*m**(p-d)-mu**(d-p))

q=2*p/(p-1)
check('pohozaev_coefficients', d*(q/2-1)/q-d/(2*p))
check('pohozaev_coefficients', (2*m*mu/p).subs(mu,(p-d)/(2*m))-(p-d)/p)

# Exact factorization in arbitrary signed angular mode k.
f, fp, fpp = S.symbols('f fp fpp', real=True)
for sign in [1,-1]:
    n=sign*k
    ell=k/r-p*r/s  # h_n'/h_n
    c = 2*k/mu if sign == 1 else 2*k*(p-2)/(p*mu)
    expression=-(S.diff(r*w,r)*ell+r*w*(S.diff(ell,r)+ell**2))/r+n*n*w/r**2+n*S.diff(w,r)/r+2*m-V
    check('generic_angular_eigenidentity', expression.subs(m,(p-2)/(2*mu))-c)
    lhs=r*w*(fp-n*f/r)**2+r*(2*m-V)*f**2
    rhs=r*w*(fp-ell*f)**2+c*r*f**2
    B=r*w*ell-n*w
    boundary_derivative=S.diff(B,r)*f**2+2*B*f*fp
    check('generic_groundstate_factorization',(lhs-rhs-boundary_derivative).subs(m,(p-2)/(2*mu)))

check('angular_gap', (2*(p-2)/(p*mu)).subs(mu,(p-2)/(2*m))-4*m/p)
check('weighted_modulus_obstruction', w/r-S.diff(w,r)-(mu**2/r-r)/(p*mu))

# Finite rational instances are separate guards against parameter substitutions.
for dv in range(2,11):
    for eps in [S.Rational(1,5), S.Rational(1,2), S.Integer(1), S.Integer(3)]:
        pv=dv+eps
        for mv in [S.Rational(1,2),S.Integer(1),S.Rational(3,2)]:
            muv=(pv-dv)/(2*mv)
            assert muv>0 and 2*(pv-1)>dv
            counts['admissibility_rational_cases']=counts.get('admissibility_rational_cases',0)+1
            check('virial_rational_cases',2*mv*muv/pv-(pv-dv)/pv)
            for t in [S.Rational(1,3),S.Integer(1),S.Integer(3)]:
                derivative=log_derivative.subs({d:dv,p:pv,m:mv,mu:t*muv})
                assert S.sign(derivative)==S.sign(t-1)
                counts['width_derivative_signs']=counts.get('width_derivative_signs',0)+1

for nv in range(-12,13):
    for pv in [S.Rational(5,2),S.Integer(3),S.Rational(17,4),S.Integer(8)]:
        mv=S.Rational(3,2);muv=(pv-2)/(2*mv)
        ell=abs(nv)/r-pv*r/(muv**2+r**2)
        ww=(muv**2+r**2)/(pv*muv)
        expr=-(S.diff(r*ww,r)*ell+r*ww*(S.diff(ell,r)+ell**2))/r+nv**2*ww/r**2+nv*S.diff(ww,r)/r+2*mv-1/ww
        cv=2*nv/muv if nv>=0 else 2*abs(nv)*(pv-2)/(pv*muv)
        check('finite_angular_modes',expr-cv)
        if nv:
            assert cv>=4*mv/pv
            counts['finite_angular_gap']=counts.get('finite_angular_gap',0)+1

# Construct minimal Clifford matrices independently of the radial reduction.
I=S.I
sx=S.Matrix([[0,1],[1,0]])
sy=S.Matrix([[0,-I],[I,0]])
sz=S.diag(1,-1)
def kron(items):
    out=S.ones(1,1)
    for item in items:
        out=S.kronecker_product(out,item)
    return out

for dv in range(2,7):
    slots=(dv+1)//2
    generators=[]
    for j in range(slots):
        generators.append(kron([sz]*j+[sx]+[S.eye(2)]*(slots-j-1)))
        generators.append(kron([sz]*j+[sy]+[S.eye(2)]*(slots-j-1)))
    if dv+1>len(generators):
        generators.append(kron([sz]*slots))
    alpha=generators[:dv];beta=generators[dv];Id=S.eye(2**slots)
    for j,a in enumerate(generators[:dv+1]):
        check('clifford_hermiticity',a-a.conjugate().T)
        for j2,a2 in enumerate(generators[:dv+1]):
            check('clifford_anticommutation',a*a2+a2*a-(2*Id if j==j2 else S.zeros(Id.rows)))
    e0=S.zeros(Id.rows,1);e0[0]=1
    xi=(Id+beta)*e0
    xi=xi/S.sqrt((xi.conjugate().T*xi)[0])
    check('positive_mass_spinor',beta*xi-xi)
    for pv in [dv+1,dv+3]:
        mv=S.Rational(3,2);muv=S.Rational(pv-dv)/(2*mv)
        for shift in [0,1]:
            xx=[S.Rational(j+shift+1,j+2) for j in range(dv)]
            X=sum((a*x for a,x in zip(alpha,xx)),S.zeros(Id.rows))
            ss=muv**2+sum(x*x for x in xx)
            vv=pv*muv/ss
            spin=(muv*Id+I*X)*xi
            derivative=sum((-I*a*(-pv*x/ss*(muv*Id+I*X)+I*a)*xi for a,x in zip(alpha,xx)),S.zeros(Id.rows,1))
            residual=derivative+(mv*beta+mv*Id-vv*Id)*spin
            check('matrix_threshold_residual',residual)
            check('matrix_spinor_density',(spin.conjugate().T*spin)[0]-ss)

out={
    'status':'PASS',
    'arithmetic':'exact symbolic and rational, SymPy',
    'total_assertions':sum(counts.values()),
    'groups':counts,
    'scope':'Finite algebra controls only; analytic arguments are in PROOF.md.',
    'original_problem_solved':False,
}
print(json.dumps(out,indent=2,sort_keys=True))
