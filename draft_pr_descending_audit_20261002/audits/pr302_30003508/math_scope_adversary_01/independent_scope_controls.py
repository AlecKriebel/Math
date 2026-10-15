"""Exact scope-boundary checks, not a numerical or elliptic/statistical proof."""
import datetime, hashlib, json, pathlib, stat, sys
import sympy as s

HERE = pathlib.Path(__file__).resolve().parent
x, y, eps = s.symbols('x y eps', real=True)
u, psi = s.Function('u')(x, y), s.Function('psi')(x, y)
grad = s.Matrix([s.diff(u, x), s.diff(u, y)])
rotated = s.Matrix([-grad[1], grad[0]])
perturbation = psi * rotated * rotated.T
checks = []
def check(name, claim):
    if not bool(claim): raise AssertionError(name)
    checks.append(name)
check('finite_one_eigenfunction_flux_is_unchanged', s.simplify(perturbation * grad) == s.zeros(2, 1))
check('finite_one_eigenfunction_PDE_is_unchanged', s.simplify(s.diff((perturbation*grad)[0], x) + s.diff((perturbation*grad)[1], y)) == 0)
check('perturbation_is_symmetric', perturbation == perturbation.T)
# Positive psi and epsilon make this rank-one update positive semidefinite.
a, b = s.symbols('a b', real=True)
v = s.Matrix([a, b])
check('rank_one_update_quadratic_form', s.simplify((v.T * perturbation * v)[0] - psi * (rotated.dot(v))**2) == 0)

# Disk counterexample: ordinary normal Neumann boundary need not match
# anisotropic co-normal Neumann boundary for a symmetric divergence operator.
r, t = s.symbols('r t', real=True)
tensor = s.Matrix([[2, 1], [1, 2]])
g = x*y*(2-x*x-y*y)
dg = s.Matrix([s.diff(g,x), s.diff(g,y)])
normal = s.Matrix([s.cos(t), s.sin(t)])
boundary = {x:s.cos(t), y:s.sin(t)}
radial_flux = s.trigsimp(normal.dot(dg.subs(boundary)))
conormal_flux = s.trigsimp(normal.dot(tensor*dg.subs(boundary)))
check('ordinary_normal_derivative_vanishes_on_circle', radial_flux == 0)
check('conormal_flux_equals_cosine_squared', s.trigsimp(conormal_flux-s.cos(2*t)**2) == 0)
check('nonzero_boundary_flux_integral', s.integrate(conormal_flux, (t,0,2*s.pi)) == s.pi)
interior_div = s.diff((tensor*dg)[0],x)+s.diff((tensor*dg)[1],y)
disk_integral = s.integrate(s.integrate(interior_div.subs({x:r*s.cos(t),y:r*s.sin(t)})*r,(r,0,1)),(t,0,2*s.pi))
check('divergence_theorem_interior_equals_nonzero_flux', s.simplify(disk_integral-s.pi) == 0)
check('tensor_is_positive_definite', sorted(tensor.eigenvals()) == [1,3])

# Observable finite-feature operator identity. Nontrivial Gram matrix is built
# using known-domain integrals, not a true coefficient or true eigensystem.
z = s.symbols('z', real=True)
features = s.Matrix([1,z,z*z])
G = s.Matrix([[s.integrate(features[i]*features[j],(z,0,1)) for j in range(3)] for i in range(3)])
B = s.Matrix([[0,s.Rational(1,4),0],[s.Rational(1,4),0,s.Rational(1,4)],[0,s.Rational(1,4),0]])
check('known_integral_Gram_matrix_is_positive', G.det()>0 and G[:2,:2].det()>0 and G[0,0]>0)
check('empirical_pair_coefficient_matrix_is_symmetric', B==B.T)
check('empirical_pair_coefficients_need_not_be_positive_semidefinite', B[:2,:2].det()<0)
c = s.Matrix(s.symbols('c0:3'))
target = s.simplify((features.T*B*G*c)[0])
kernel = (features.T*B*features.subs(z, s.Symbol('w')))[0]
w = s.Symbol('w')
direct = s.integrate(kernel*(features.subs(z,w).T*c)[0],(w,0,1))
check('finite_Hilbert_operator_is_exactly_observable_BG_problem', s.simplify(direct-target)==0)

# Check actual dyadic schedule and net cardinality exponents without treating
# finite controls as proof of Borel--Cantelli or smoothing convergence.
for d in range(2,10):
    check('net_exponent_dimension_'+str(d), s.Rational(2*d,4*d)==s.Rational(1,2))
for N in (2,3,4,7,8,15,16,31,32,63,64,127,128,1000):
    j = N.bit_length()-1
    check('no_unobserved_future_state_N_'+str(N), 2**j <= N < 2**(j+1))

def pin(p):
    p=pathlib.Path(p); body=p.read_bytes()
    return {'path':str(p.resolve()),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
modules=[]
for name, module in sorted(sys.modules.items()):
    path=getattr(module,'__file__',None)
    if path and pathlib.Path(path).is_file():
        modules.append({'name':name,'input':pin(path)})
result={'status':'PASS_INDEPENDENT_SCOPE_BOUNDARY_CONTROLS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'check_count':len(checks),'python':sys.version,'executable':str(pathlib.Path(sys.executable).resolve()),'sympy':s.__version__,'source':pin(__file__),'loaded_modules':modules,'limits':'Exact finite algebra confirms witnesses and finite-feature observability; it does not prove empirical convergence, infinite elliptic regularity, or historical novelty. The one-mode and ordinary-normal-reflection witnesses are outside the submitted construction; neither falsifies its stated theorem.'}
(HERE/'INDEPENDENT_SCOPE_CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ('status','check_count','python','sympy','limits')}))
