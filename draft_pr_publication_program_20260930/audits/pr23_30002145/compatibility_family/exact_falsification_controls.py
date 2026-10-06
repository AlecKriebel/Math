#!/usr/bin/env python3
"""New exact audit controls; finite checks supplement FIRST_PASS.md, not a theorem proof."""
import json
import sys
import sympy as s

checks = []

def record(name, **details):
    checks.append(dict(name=name, pass_=True, **details))

def zero(M):
    assert all(s.simplify(z) == 0 for z in M), M

def strain(u, x):
    D = u.jacobian(x)
    return (D + D.T)/2

def product(a, b):
    return (a*b.T+b*a.T)/2

def compatibility(E, x):
    d = len(x)
    return [s.diff(E[i,j],x[k],x[l])+s.diff(E[k,l],x[i],x[j])
            -s.diff(E[k,j],x[i],x[l])-s.diff(E[i,l],x[k],x[j])
            for i in range(d) for j in range(d) for k in range(d) for l in range(d)]

def quadratic(a,b,v,x):
    A,B,V = x.dot(a),x.dot(b),x.dot(v)
    return a*B*V+b*A*V-v*A*B

# Exact oblique change of variables, including signed scales and a truly oblique plane.
x = s.Matrix(s.symbols('x0:3', real=True))
a,b = s.Matrix([2,1,0]),s.Matrix([-3,4,0])
q = s.Matrix.hstack(a,b)
dual = q*(q.T*q).inv()
B = s.Matrix.hstack(dual[:,0],dual[:,1],s.Matrix([0,0,1]))
zero(B.T*a-s.Matrix([1,0,0])); zero(B.T*b-s.Matrix([0,1,0]))
y = s.Matrix(s.symbols('y0:3', real=True))
v = s.Matrix([0,0,-7])
A,C,V = x.dot(a),x.dot(b),x.dot(v)
u = a*(s.sin(C)+C*V)+b*(A**4+A*V)-v*A*C
lam = s.cos(C)+4*A**3+2*V
zero(strain(u,x)-product(a,b)*lam)
uy = u.subs(dict(zip(x,B*y)), simultaneous=True)
w = B.T*uy
zero(strain(w,y)-B.T*strain(u,x).subs(dict(zip(x,B*y)), simultaneous=True)*B)
canonical = s.Matrix([s.sin(y[1])+y[1]*y.dot(v),y[0]**4+y[0]*y.dot(v),0])-v*y[0]*y[1]
zero(w-canonical)
R = s.Matrix([[0,2,3],[-2,0,-5],[-3,5,0]])
zero(B.inv().T*R*B.inv()+(B.inv().T*R*B.inv()).T)
record('oblique_congruence_and_skew_covariance', determinant=str(B.det()),
       a=list(a),b=list(b),v=list(v))

# Universal symbolic quadratic identity, and necessity of each cancellation term.
aa,bb,vv = (s.Matrix(s.symbols(prefix+'0:3')) for prefix in ('a','b','v'))
zero(strain(quadratic(aa,bb,vv,x),x)-2*x.dot(vv)*product(aa,bb))
vlong = 5*a-2*b+v
zero(quadratic(a,b,vlong,x)-quadratic(a,b,v,x)-5*b*A**2+2*a*C**2)
record('longitudinal_transverse_vector_absorption')
e1,e2,e3 = (s.eye(3)[:,i] for i in range(3))
blocks = [e1*x[1]*x[2], e2*x[0]*x[2], -e3*x[0]*x[1]]
for omitted in range(3):
    mutated = sum((term for j,term in enumerate(blocks) if j!=omitted),s.zeros(3,1))
    M = strain(mutated,x)
    # Orthogonal projection on the complement of the allowed fixed line.
    P = product(e1,e2)
    residual = M-P*sum(M[i,j]*P[i,j] for i in range(3) for j in range(3))/sum(z*z for z in P)
    assert any(s.expand(z)!=0 for z in residual)
    record('quadratic_cancellation_negative_control', omitted_block=omitted)

# Finite polynomial completeness from displacement equations, materially different
# from Hessian-rank checks: solve ALL displacement coefficient constraints and
# compare their nullspace with a spanning family of actual normal-form fields.
def monomials(x,degree):
    from itertools import product as cartesian
    return [s.prod(x[i]**p[i] for i in range(len(x)))
            for p in cartesian(range(degree+1),repeat=len(x)) if sum(p)<=degree]

def polynomial_span(d,degree,kind,oblique=False):
    xx = s.Matrix(s.symbols('z0:'+str(d)))
    mons = monomials(xx,degree)
    coeffs = s.symbols('c0:'+str(d*len(mons)))
    generic = s.Matrix([sum(coeffs[i*len(mons)+j]*m for j,m in enumerate(mons)) for i in range(d)])
    basis = s.eye(d)
    av,bv = basis[:,0],basis[:,1] if d>1 else basis[:,0]
    if oblique:
        av,bv = s.Matrix([2,1,0]),s.Matrix([-3,4,0])
    P = product(av,bv) if kind=='independent' else av*av.T
    E = strain(generic,xx)
    lamE = sum(E[i,j]*P[i,j] for i in range(d) for j in range(d))/sum(z*z for z in P)
    residual = E-lamE*P
    eqs=[]
    for q in residual:
        eqs.extend(s.Poly(s.expand(q),*xx).coeffs())
    constraint,_ = s.linear_eq_to_matrix(eqs,coeffs)
    fields=[]
    if kind=='independent':
        fields += [av*xx.dot(bv)**k for k in range(degree+1)]
        fields += [bv*xx.dot(av)**k for k in range(degree+1)]
        if degree>=2:
            for tvec in s.Matrix.vstack(av.T,bv.T).nullspace():
                fields.append(quadratic(av,bv,tvec,xx))
    else:
        fields += [av*xx[0]**k for k in range(degree+1)]
        for j in range(1,d):
            for k in range(degree+1):
                pp = xx[0]**k
                fields.append(av*xx[j]*s.diff(pp,xx[0])-basis[:,j]*pp)
    fields += [basis[:,i] for i in range(d)]
    fields += [(basis[:,i]*xx[j]-basis[:,j]*xx[i]) for i in range(d) for j in range(i+1,d)]
    vectors=[]
    for field in fields:
        vectors.append(s.Matrix([s.Poly(s.expand(field[i]),*xx).coeff_monomial(m) for i in range(d) for m in mons]))
    template = s.Matrix.hstack(*vectors)
    zero(constraint*template)
    nullity = len(coeffs)-constraint.rank()
    assert template.rank()==nullity
    record('displacement_polynomial_completeness',dimension=d,degree=degree,
           case=kind,oblique=oblique,unknowns=len(coeffs),solution_dimension=nullity,
           template_rank=template.rank())

for kind in ('independent','parallel'):
    polynomial_span(2,4,kind)
    polynomial_span(3,3,kind)
polynomial_span(3,3,'independent',oblique=True)

# Integrating compatible strains yields a local potential; Hessian identity also
# supplies an independent check that the difference of potentials is rigid.
h1,h2 = y[1]**3+y[1],y[0]**2-4*y[0]
coefficient = h1+h2-10*y[2]
potential = e1*(y[1]**4/4+y[1]**2/2-5*y[1]*y[2])+e2*(y[0]**3/3-2*y[0]**2-5*y[0]*y[2])+5*e3*y[0]*y[1]
E = product(e1,e2)*coefficient
zero(strain(potential,y)-E); assert all(s.expand(q)==0 for q in compatibility(E,y))
for i in range(3):
    for j in range(3):
        for k in range(3):
            assert s.expand(s.diff(potential[i],y[j],y[k])-s.diff(E[i,k],y[j])-s.diff(E[i,j],y[k])+s.diff(E[j,k],y[i]))==0
record('compatible_strain_local_potential_hessian_identity')

bad_coefficients = [y[0]*y[1],y[0]*y[2],y[1]*y[2],y[2]**2]
for f in bad_coefficients:
    assert any(s.expand(q)!=0 for q in compatibility(product(e1,e2)*f,y))
record('forbidden_independent_coefficient_controls',coefficients=[str(q) for q in bad_coefficients])
for f in [y[1]**2,y[1]*y[2],y[2]**2]:
    assert any(s.expand(q)!=0 for q in compatibility((e1*e1.T)*f,y))
record('forbidden_parallel_transverse_controls')

# Signed singular measures checked distributionally using exact delta identities.
step = s.Heaviside(y[1])-s.Heaviside(y[1]-1)
signed_u = e1*step
signed_lam = s.DiracDelta(y[1])-s.DiracDelta(y[1]-1)
zero(strain(signed_u,y)-product(e1,e2)*signed_lam)
record('independent_signed_singular_profiles')
parallel_u = e1*y[1]*s.sign(y[0])-e2*s.Abs(y[0])
zero(strain(parallel_u,y)-e1*e1.T*(2*y[1]*s.DiracDelta(y[0])))
record('parallel_signed_singular_transverse_measure')

# Scaling/sign/degeneracy controls. Literal unequal parallel a!=+/-b is NOT an
# independence criterion; a direct counterexample is preserved as a source caveat.
for scale in [s.Rational(3,2),-7]:
    av,bv = scale*e1,(s.Integer(-2)/scale)*e1
    P = product(av,bv)
    pu = s.Matrix([y[0]**3+y[1]*3*y[0]**2,-y[0]**3,0])
    density = 3*y[0]**2+6*y[0]*y[1]
    zero(strain(pu,y)-P*(density/(-2)))
record('parallel_arbitrary_nonzero_scaling_and_signs')
example = s.Matrix([4*y[0]**3*y[1],-y[0]**4,0])
litP = product(e1,2*e1)
litdensity = 6*y[0]**2*y[1]
zero(strain(example,y)-litP*litdensity)
assert s.diff(litdensity,y[0],y[1])!=0
record('literal_source_a_not_plusminus_b_counterexample')
rigid = R*y+s.Matrix([2,-3,5]); zero(strain(rigid,y))
assert any(z!=0 for z in strain(s.Matrix([y[0]**2,0,0]),y))
scalar = s.sin(y[0])+y[0]**5
assert s.simplify(s.diff(scalar,y[0])-(-6)*(s.diff(scalar,y[0])/(-6)))==0
record('zero_kernel_and_dimension_one_controls')

# Exact witness used in FIRST_PASS's smooth nonconvex-domain obstruction.
t=s.Symbol('t',real=True)
bump_core=s.exp(-1/(1-t*t))
db=s.diff(bump_core,t)
assert db.subs(t,0)==0
assert s.simplify(db.subs(t,s.Rational(1,2))+s.Rational(16,9)*s.exp(-s.Rational(4,3)))==0
record('nonconvex_domain_profile_obstruction_witness',
       derivative_at_zero='0', derivative_at_half=str(s.simplify(db.subs(t,s.Rational(1,2)))))

print(json.dumps({'pass':True,'python':sys.version.split()[0],'sympy':s.__version__,
                  'number_of_checks':len(checks),'checks':checks,
                  'limits':'Finite exact falsification controls; necessity is proved in FIRST_PASS.md. Distributional identities are formal exact checks supplemented by the measure argument there.'},indent=2,default=str))
